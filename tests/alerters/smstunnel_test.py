import datetime
import logging
import math
import pytest

from unittest import mock

from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import ConnectTimeout, ReadTimeout, SSLError

from elastalert.alerters.smstunnel import SMSTunnelAlerter
from elastalert.loaders import FileRulesLoader
from elastalert.util import dt_to_ts, EAException, ts_now

API_KEY = 'test-api-key-0123456789abcdef'
NUMBER = '+12025550199'
SECRET_TEXT = 'do-not-log-this-text'


def make_rule(alert=(), **options):
    rule = {
        'name': 'Test SMSTunnel Rule',
        'type': 'any',
        'smstunnel_api_key': API_KEY,
        'smstunnel_to': NUMBER,
        'alert': []
    }
    rule.update(options)
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    # Set after load_modules, so that the tests can watch load_alerts refuse a bad option
    rule['alert'] = list(alert)
    return rule


def make_alerter(alert_time=None, **options):
    alert = SMSTunnelAlerter(make_rule(**options))
    alert.pipeline = {'alert_time': alert_time if alert_time is not None else ts_now()}
    return alert


def make_response(status_code=200, body=None):
    response = mock.Mock()
    response.status_code = status_code
    response.json.return_value = {'success': True, 'messageId': 'abc'} if body is None else body
    return response


def make_match():
    return {'@timestamp': '2026-11-21T10:00:00', 'somefield': SECRET_TEXT}


def assert_nothing_private(text):
    assert API_KEY not in text
    assert NUMBER not in text
    assert NUMBER[1:] not in text
    assert SECRET_TEXT not in text


def test_smstunnel_send(caplog):
    caplog.set_level(logging.INFO)
    alert = make_alerter()
    with mock.patch('requests.post', return_value=make_response()) as mock_post:
        alert.alert([make_match()])

    mock_post.assert_called_once_with(
        'https://smstunnel.io/api/v1/sms/send',
        json={
            'to': NUMBER,
            'message': 'Test SMSTunnel Rule\n\n@timestamp: 2026-11-21T10:00:00\nsomefield: %s' % SECRET_TEXT
        },
        headers={
            'Content-Type': 'application/json',
            'X-API-Key': API_KEY,
            'Idempotency-Key': mock.ANY
        },
        timeout=10,
        allow_redirects=False
    )
    assert ('elastalert', logging.INFO, "Alert 'Test SMSTunnel Rule' sent to SMSTunnel") == caplog.record_tuples[0]
    assert_nothing_private(caplog.text)


def test_smstunnel_send_with_device_id():
    alert = make_alerter(smstunnel_device_id='671fe0d9c3b2a1f0e9d8c7b6')
    with mock.patch('requests.post', return_value=make_response()) as mock_post:
        alert.alert([make_match()])
    assert mock_post.call_args[1]['json']['deviceId'] == '671fe0d9c3b2a1f0e9d8c7b6'


def test_smstunnel_send_without_pipeline_has_no_idempotency_key():
    alert = SMSTunnelAlerter(make_rule())
    with mock.patch('requests.post', return_value=make_response()) as mock_post:
        alert.alert([make_match()])
    assert 'Idempotency-Key' not in mock_post.call_args[1]['headers']


@pytest.mark.parametrize('length, cropped', [
    (1599, False),
    (1600, False),
    (1601, True),
    (50000, True),
])
def test_smstunnel_crops_long_text(length, cropped):
    alert = make_alerter(alert_text='x' * length, alert_text_type='alert_text_only')
    with mock.patch('requests.post', return_value=make_response()) as mock_post:
        alert.alert([make_match()])

    message = mock_post.call_args[1]['json']['message']
    assert len(message) <= 1600
    assert message.endswith('(message cropped due to SMS limit)') == cropped
    if not cropped:
        assert message == 'x' * length


@pytest.mark.parametrize('text', [
    '\U0001F6A8' * 2000,  # two UTF-16 units each
    'x' + '\U0001F6A8' * 2000,  # the cut falls in the middle of an emoji
    'ș' * 2000,  # outside the GSM alphabet
    '{' * 2000,  # two septets each in the GSM alphabet
])
def test_smstunnel_crop_fits_the_sms_parts_of_one_phone(text):
    alert = make_alerter(alert_text=text, alert_text_type='alert_text_only')
    with mock.patch('requests.post', return_value=make_response()) as mock_post:
        alert.alert([make_match()])

    message = mock_post.call_args[1]['json']['message']
    units = len(message.encode('utf-16-le')) // 2  # raises on a character cut in half
    assert 1590 <= units <= 1600
    assert math.ceil(units / 67) <= 24
    assert message.endswith('(message cropped due to SMS limit)')


def test_smstunnel_does_not_crop_emoji_that_fit():
    text = '\U0001F6A8' * 800
    alert = make_alerter(alert_text=text, alert_text_type='alert_text_only')
    with mock.patch('requests.post', return_value=make_response()) as mock_post:
        alert.alert([make_match()])
    assert mock_post.call_args[1]['json']['message'] == text


def test_smstunnel_system_error_notification_leaves_out_the_rule():
    alert = make_alerter()
    failed_rule = {'name': 'failed', 'smstunnel_api_key': API_KEY, 'smstunnel_to': NUMBER, 'es_password': 'hunter2'}
    details = {'timestamp': ts_now(), 'message': 'Uncaught exception running rule failed', 'rule': failed_rule}
    with mock.patch('requests.post', return_value=make_response()) as mock_post:
        alert.alert([details])

    message = mock_post.call_args[1]['json']['message']
    assert 'Uncaught exception running rule failed' in message
    assert API_KEY not in message
    assert NUMBER not in message
    assert 'hunter2' not in message


def test_smstunnel_keeps_a_rule_field_of_a_document():
    alert = make_alerter()
    match = {'@timestamp': '2026-11-21T10:00:00', 'message': 'blocked', 'rule': {'id': 'R-100'}}
    with mock.patch('requests.post', return_value=make_response()) as mock_post:
        alert.alert([match])
    assert 'R-100' in mock_post.call_args[1]['json']['message']


def test_smstunnel_idempotency_key_survives_the_retry():
    first_time = ts_now()
    with mock.patch('requests.post', return_value=make_response()) as mock_post:
        make_alerter(alert_time=first_time).alert([make_match()])
        # ElastAlert reads the alert back from Elasticsearch, with its time as a string
        make_alerter(alert_time=dt_to_ts(first_time)).alert([make_match()])
        make_alerter(alert_time=first_time.isoformat()).alert([make_match()])

    keys = [call[1]['headers']['Idempotency-Key'] for call in mock_post.call_args_list]
    assert len(set(keys)) == 1
    assert 16 <= len(keys[0]) <= 255
    assert keys[0].isascii() and keys[0].isprintable()
    assert_nothing_private(keys[0])


@pytest.mark.parametrize('other', [
    {'alert_time': 1},
    {'smstunnel_to': '+12025550198'},
    {'smstunnel_device_id': '671fe0d9c3b2a1f0e9d8c7b6'},
    {'name': 'Another rule'},
])
def test_smstunnel_idempotency_key_differs_between_alerts(other):
    alert_time = ts_now()
    options = dict(other)
    other_time = alert_time + datetime.timedelta(seconds=options.pop('alert_time', 0))
    with mock.patch('requests.post', return_value=make_response()) as mock_post:
        make_alerter(alert_time=alert_time).alert([make_match()])
        make_alerter(alert_time=other_time, **options).alert([make_match()])

    keys = [call[1]['headers']['Idempotency-Key'] for call in mock_post.call_args_list]
    assert keys[0] != keys[1]


@pytest.mark.parametrize('aggregation_key', ['host', 'nested.host', 'missing'])
def test_smstunnel_idempotency_key_of_aggregated_alerts(aggregation_key):
    # A cron aggregation gives the alerts of every aggregation_key value the same alert_time
    alert_time = ts_now()
    with mock.patch('requests.post', return_value=make_response()) as mock_post:
        for host in ['a', 'b', 'a']:
            match = {'@timestamp': '2026-11-21T10:00:00', 'host': host, 'nested': {'host': host}}
            make_alerter(alert_time=alert_time, aggregation_key=aggregation_key).alert([match])

    keys = [call[1]['headers']['Idempotency-Key'] for call in mock_post.call_args_list]
    assert keys[0] == keys[2]
    assert (keys[0] != keys[1]) == (aggregation_key != 'missing')


def test_smstunnel_idempotency_key_with_an_unreadable_aggregation_key():
    alert = make_alerter(aggregation_key='hosts[5]')
    match = {'@timestamp': '2026-11-21T10:00:00', 'hosts': ['a']}
    with mock.patch('requests.post', return_value=make_response()) as mock_post:
        alert.alert([match])
    assert mock_post.call_args[1]['headers']['Idempotency-Key'].startswith('elastalert-')


def test_smstunnel_refuses_an_alert_past_the_idempotency_window():
    old = dt_to_ts(ts_now() - datetime.timedelta(hours=23, minutes=1))
    alert = make_alerter(alert_time=old)
    with mock.patch('requests.post') as mock_post, pytest.raises(EAException) as ea:
        alert.alert([make_match()])
    assert 'older than 23 hours' in str(ea.value)
    assert mock_post.call_count == 0


def test_smstunnel_sends_an_alert_inside_the_idempotency_window():
    recent = dt_to_ts(ts_now() - datetime.timedelta(hours=22, minutes=59))
    alert = make_alerter(alert_time=recent)
    with mock.patch('requests.post', return_value=make_response()) as mock_post:
        alert.alert([make_match()])
    assert mock_post.call_count == 1


def test_smstunnel_failed_alert_retried_by_elastalert_keeps_its_key(ea):
    alerter = SMSTunnelAlerter(make_rule(name=ea.rules[0]['name']))
    ea.rules[0]['alert'] = [alerter]
    ea.rules[0].pop('aggregation')
    match = make_match()

    # The first attempt loses its answer: ElastAlert records the alert as not sent
    with mock.patch('requests.post', side_effect=ReadTimeout()) as mock_post:
        ea.send_alert([match], ea.rules[0])
    first_key = mock_post.call_args[1]['headers']['Idempotency-Key']
    assert mock_post.call_count == 1
    written = ea.writeback_es.index.call_args[1]['body']
    assert written['alert_sent'] is False
    assert_nothing_private(written['alert_exception'])

    # The next pass of send_pending_alerts sends it again, with the time read back from the index
    pending = {'_id': 'ABCD', '_index': 'wb', '_source': dict(written)}
    ea.writeback_es.search.side_effect = [{'hits': {'hits': [pending]}}, {'hits': {'hits': []}}]
    with mock.patch('requests.post', return_value=make_response()) as mock_post:
        ea.send_pending_alerts()
    assert mock_post.call_count == 1
    assert mock_post.call_args[1]['headers']['Idempotency-Key'] == first_key
    assert ea.writeback_es.index.call_args[1]['body']['alert_sent'] is True


@pytest.mark.parametrize('error', [ConnectTimeout, ReadTimeout, RequestsConnectionError, SSLError])
def test_smstunnel_lost_answer_raises_without_retrying(caplog, error):
    caplog.set_level(logging.DEBUG)
    alert = make_alerter()
    cause = error('POST with %s and %s to %s' % (API_KEY, SECRET_TEXT, NUMBER))
    with mock.patch('requests.post', side_effect=cause) as mock_post, pytest.raises(EAException) as ea:
        alert.alert([make_match()])

    assert mock_post.call_count == 1
    assert 'Error posting SMSTunnel alert: no answer from the API (%s)' % error.__name__ in str(ea.value)
    assert 'may already have been sent' in str(ea.value)
    assert ea.value.__suppress_context__
    assert_nothing_private(str(ea.value))
    assert_nothing_private(caplog.text)


@pytest.mark.parametrize('status_code, body, expected', [
    (401, {'statusCode': 401, 'message': 'Invalid or expired API key'}, 'HTTP 401'),
    (403, {'code': 'PERMISSION_REQUIRED', 'message': 'no'}, 'HTTP 403 (PERMISSION_REQUIRED)'),
    (409, {'code': 'IDEMPOTENCY_KEY_IN_PROGRESS'}, 'HTTP 409 (IDEMPOTENCY_KEY_IN_PROGRESS)'),
    (422, {'code': 'IDEMPOTENCY_KEY_REUSED'}, 'HTTP 422 (IDEMPOTENCY_KEY_REUSED)'),
    (429, {'statusCode': 429, 'message': 'Too Many Requests'}, 'HTTP 429'),
    (500, {'statusCode': 500, 'message': 'Internal server error'}, 'HTTP 500'),
    (302, {}, 'HTTP 302'),
    (400, {'code': 'not a code ' + NUMBER, 'message': 'Invalid number ' + NUMBER}, 'HTTP 400'),
])
def test_smstunnel_refused_by_the_api(caplog, status_code, body, expected):
    caplog.set_level(logging.DEBUG)
    alert = make_alerter()
    with mock.patch('requests.post', return_value=make_response(status_code, body)) as mock_post, \
            pytest.raises(EAException) as ea:
        alert.alert([make_match()])

    assert mock_post.call_count == 1
    assert str(ea.value) == 'Error posting SMSTunnel alert: %s' % expected
    assert_nothing_private(caplog.text)


def test_smstunnel_answer_that_is_not_json():
    alert = make_alerter()
    response = make_response(502)
    response.json.side_effect = ValueError('not json')
    with mock.patch('requests.post', return_value=response), pytest.raises(EAException) as ea:
        alert.alert([make_match()])
    assert str(ea.value) == 'Error posting SMSTunnel alert: HTTP 502'


@pytest.mark.parametrize('body', [{'success': False}, {}, ['success'], 'success'])
def test_smstunnel_answer_without_confirmation(body):
    alert = make_alerter()
    with mock.patch('requests.post', return_value=make_response(200, body)), pytest.raises(EAException) as ea:
        alert.alert([make_match()])
    assert 'did not confirm the text' in str(ea.value)


@pytest.mark.parametrize('number', [
    [NUMBER],
    [NUMBER, '+12025550198'],
    NUMBER + ',+12025550198',
    '+1 202 555 0199',
    NUMBER[1:],
    '00' + NUMBER[1:],
    '0755123456',
    int(NUMBER[1:]),
    '+0755123456',
    '+123456',
    '+1234567890123456',
    NUMBER + '\n',
    '+' + '١' * 11,
    '',
    None,
])
def test_smstunnel_refuses_a_bad_number_when_the_rule_loads(number):
    rule = make_rule(smstunnel_to=number, alert=['smstunnel'])
    rules_loader = FileRulesLoader({})
    with pytest.raises(EAException) as ea:
        rules_loader.load_alerts(rule, rule['alert'])
    assert 'smstunnel_to must be exactly one number in international format' in str(ea.value)
    if number:
        assert str(number) not in str(ea.value)


@pytest.mark.parametrize('api_key', ['', 'two words', 'line\nbreak', 'clé', 12345, None])
def test_smstunnel_refuses_a_bad_api_key_when_the_rule_loads(api_key):
    rule = make_rule(smstunnel_api_key=api_key, alert=['smstunnel'])
    rules_loader = FileRulesLoader({})
    with pytest.raises(EAException) as ea:
        rules_loader.load_alerts(rule, rule['alert'])
    assert 'smstunnel_api_key must be a single API key' in str(ea.value)


@pytest.mark.parametrize('missing', ['smstunnel_api_key', 'smstunnel_to'])
def test_smstunnel_required_options(missing):
    rule = make_rule(alert=['smstunnel'])
    rule.pop(missing)
    rules_loader = FileRulesLoader({})
    with pytest.raises(EAException) as ea:
        rules_loader.load_alerts(rule, rule['alert'])
    assert 'Missing required option(s): %s' % missing in str(ea.value)


def test_smstunnel_loads_by_name():
    rule = make_rule(alert=['smstunnel'])
    alerters = FileRulesLoader({}).load_alerts(rule, rule['alert'])
    assert len(alerters) == 1
    assert isinstance(alerters[0], SMSTunnelAlerter)


def test_smstunnel_loads_with_a_rule_reference():
    rule = make_rule(oncall_number=NUMBER, smstunnel_to='$oncall_number$', alert=['smstunnel'])
    alerters = FileRulesLoader({}).load_alerts(rule, rule['alert'])
    assert alerters[0].smstunnel_to == NUMBER


def test_smstunnel_options_pass_the_rule_schema():
    rules_loader = FileRulesLoader({})
    rule = {
        'name': 'Test SMSTunnel Rule',
        'type': 'any',
        'index': 'test',
        'alert': ['smstunnel'],
        'smstunnel_api_key': API_KEY,
        'smstunnel_to': NUMBER,
        'smstunnel_device_id': '671fe0d9c3b2a1f0e9d8c7b6'
    }
    rules_loader.rule_schema.validate(rule)


def test_smstunnel_getinfo_keeps_the_key_and_number_out():
    assert make_alerter().get_info() == {'type': 'smstunnel'}
