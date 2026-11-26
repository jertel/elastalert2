import datetime
import json
import logging
import math
import pytest
import requests

from unittest import mock

from jsonschema.exceptions import ValidationError
from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import ConnectTimeout, ReadTimeout, SSLError

from elastalert.alerters.smstunnel import SMSTunnelAlerter
from elastalert.loaders import FileRulesLoader
from elastalert.util import dt_to_ts, EAException, ts_now

API_KEY = 'test-api-key-0123456789abcdef'
NUMBER = '+12025550199'
URL = 'https://smstunnel.io/api/v1/sms/send'


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
    # Set after load_modules, so that the tests can watch load_alerts check the options
    rule['alert'] = list(alert)
    return rule


def make_alerter(alert_time=None, **options):
    alert = SMSTunnelAlerter(make_rule(**options))
    alert.pipeline = {'alert_time': alert_time if alert_time is not None else ts_now()}
    return alert


def make_response(status_code=200, body=None):
    response = requests.Response()
    response.status_code = status_code
    response.url = URL
    content = {'success': True, 'messageId': 'abc'} if body is None else body
    response._content = content if isinstance(content, bytes) else json.dumps(content).encode()
    return response


def make_match():
    return {'@timestamp': '2026-11-21T10:00:00', 'somefield': 'foobarbaz'}


def schema_rule(**options):
    rule = {
        'name': 'Test SMSTunnel Rule',
        'type': 'any',
        'index': 'test',
        'alert': ['smstunnel'],
        'smstunnel_api_key': API_KEY,
        'smstunnel_to': NUMBER
    }
    rule.update(options)
    return rule


def test_smstunnel_send(caplog):
    caplog.set_level(logging.INFO)
    alert = make_alerter()
    with mock.patch('requests.post', return_value=make_response()) as mock_post:
        alert.alert([make_match()])

    mock_post.assert_called_once_with(
        URL,
        json={
            'to': NUMBER,
            'message': 'Test SMSTunnel Rule\n\n@timestamp: 2026-11-21T10:00:00\nsomefield: foobarbaz'
        },
        headers={
            'Content-Type': 'application/json',
            'X-API-Key': API_KEY,
            'Idempotency-Key': mock.ANY
        },
        proxies=None,
        timeout=10,
        allow_redirects=False
    )
    assert ('elastalert', logging.INFO, "Alert 'Test SMSTunnel Rule' sent to SMSTunnel") == caplog.record_tuples[0]


def test_smstunnel_send_with_device_id():
    alert = make_alerter(smstunnel_device_id='671fe0d9c3b2a1f0e9d8c7b6')
    with mock.patch('requests.post', return_value=make_response()) as mock_post:
        alert.alert([make_match()])
    assert mock_post.call_args[1]['json']['deviceId'] == '671fe0d9c3b2a1f0e9d8c7b6'


def test_smstunnel_proxy():
    alert = make_alerter(smstunnel_proxy='proxy.example.com:3128')
    with mock.patch('requests.post', return_value=make_response()) as mock_post:
        alert.alert([make_match()])
    assert mock_post.call_args[1]['proxies'] == {'https': 'proxy.example.com:3128'}


def test_smstunnel_timeout():
    alert = make_alerter(smstunnel_timeout=30)
    with mock.patch('requests.post', return_value=make_response()) as mock_post:
        alert.alert([make_match()])
    assert mock_post.call_args[1]['timeout'] == 30


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


@pytest.mark.parametrize('max_length, length, cropped', [
    (160, 160, False),
    (160, 161, True),
    (70, 500, True),
])
def test_smstunnel_max_length(max_length, length, cropped):
    alert = make_alerter(smstunnel_max_length=max_length, alert_text='x' * length, alert_text_type='alert_text_only')
    with mock.patch('requests.post', return_value=make_response()) as mock_post:
        alert.alert([make_match()])

    message = mock_post.call_args[1]['json']['message']
    assert len(message) <= max_length
    assert message.endswith('(message cropped due to SMS limit)') == cropped


def test_smstunnel_max_length_shorter_than_the_crop_note():
    alert = make_alerter(smstunnel_max_length=10, alert_text='x' * 50, alert_text_type='alert_text_only')
    with mock.patch('requests.post', return_value=make_response()) as mock_post:
        alert.alert([make_match()])
    assert mock_post.call_args[1]['json']['message'] == 'x' * 10


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
    assert API_KEY not in keys[0] and NUMBER[1:] not in keys[0]


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


def test_smstunnel_sends_an_old_alert():
    # ElastAlert retries an unsent alert for alert_time_limit (2 days by default), and every retry is sent
    old = dt_to_ts(ts_now() - datetime.timedelta(days=1, hours=1))
    alert = make_alerter(alert_time=old)
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

    # The next pass of send_pending_alerts sends it again, with the time read back from the index
    pending = {'_id': 'ABCD', '_index': 'wb', '_source': dict(written)}
    ea.writeback_es.search.side_effect = [{'hits': {'hits': [pending]}}, {'hits': {'hits': []}}]
    with mock.patch('requests.post', return_value=make_response()) as mock_post:
        ea.send_pending_alerts()
    assert mock_post.call_count == 1
    assert mock_post.call_args[1]['headers']['Idempotency-Key'] == first_key
    assert ea.writeback_es.index.call_args[1]['body']['alert_sent'] is True


@pytest.mark.parametrize('error', [ConnectTimeout, ReadTimeout, RequestsConnectionError, SSLError])
def test_smstunnel_network_error_is_reported_in_full(error):
    alert = make_alerter()
    cause = error('Unable to connect to proxy proxy.example.com:3128')
    with mock.patch('requests.post', side_effect=cause) as mock_post, pytest.raises(EAException) as ea:
        alert.alert([make_match()])

    assert mock_post.call_count == 1
    assert str(ea.value) == 'Error posting SMSTunnel alert: Unable to connect to proxy proxy.example.com:3128. Details: '


@pytest.mark.parametrize('status_code, body', [
    (401, {'statusCode': 401, 'message': 'Invalid or expired API key'}),
    (403, {'code': 'PERMISSION_REQUIRED', 'message': 'This key may not send texts'}),
    (409, {'code': 'IDEMPOTENCY_KEY_IN_PROGRESS'}),
    (429, {'statusCode': 429, 'message': 'Too Many Requests'}),
    (500, {'statusCode': 500, 'message': 'Internal server error'}),
])
def test_smstunnel_refused_by_the_api(status_code, body):
    alert = make_alerter()
    with mock.patch('requests.post', return_value=make_response(status_code, body)) as mock_post, \
            pytest.raises(EAException) as ea:
        alert.alert([make_match()])

    assert mock_post.call_count == 1
    assert str(ea.value).startswith('Error posting SMSTunnel alert: %s ' % status_code)
    assert str(ea.value).endswith('Details: %s' % json.dumps(body))


def test_smstunnel_answer_that_is_not_json():
    alert = make_alerter()
    with mock.patch('requests.post', return_value=make_response(502, b'<html>Bad Gateway</html>')), \
            pytest.raises(EAException) as ea:
        alert.alert([make_match()])
    assert str(ea.value).startswith('Error posting SMSTunnel alert: 502 Server Error')
    assert str(ea.value).endswith('Details: <html>Bad Gateway</html>')


def test_smstunnel_does_not_follow_a_redirect():
    alert = make_alerter()
    with mock.patch('requests.post', return_value=make_response(302, b'')), pytest.raises(EAException) as ea:
        alert.alert([make_match()])
    assert str(ea.value) == 'Error posting SMSTunnel alert: the API did not confirm the text (HTTP 302). Details: '


@pytest.mark.parametrize('body', [{'success': False}, {}, ['success'], 'success', b'not json'])
def test_smstunnel_answer_without_confirmation(body):
    alert = make_alerter()
    with mock.patch('requests.post', return_value=make_response(200, body)), pytest.raises(EAException) as ea:
        alert.alert([make_match()])
    assert 'the API did not confirm the text (HTTP 200)' in str(ea.value)


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
    FileRulesLoader({}).rule_schema.validate(schema_rule(
        smstunnel_device_id='671fe0d9c3b2a1f0e9d8c7b6',
        smstunnel_proxy='proxy.example.com:3128',
        smstunnel_timeout=30,
        smstunnel_max_length=160
    ))


@pytest.mark.parametrize('option, value', [
    ('smstunnel_to', [NUMBER]),
    ('smstunnel_to', int(NUMBER[1:])),
    ('smstunnel_api_key', 12345),
    ('smstunnel_timeout', 'ten'),
    ('smstunnel_max_length', 0),
    ('smstunnel_proxy', 3128),
])
def test_smstunnel_options_refused_by_the_rule_schema(option, value):
    with pytest.raises(ValidationError):
        FileRulesLoader({}).rule_schema.validate(schema_rule(**{option: value}))


def test_smstunnel_getinfo():
    assert make_alerter().get_info() == {'type': 'smstunnel'}
