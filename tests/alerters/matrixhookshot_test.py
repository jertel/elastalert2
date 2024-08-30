import json
import logging
import pytest

from unittest import mock

from requests import RequestException

from elastalert.alerters.matrixhookshot import MatrixHookshotAlerter
from elastalert.loaders import FileRulesLoader
from elastalert.util import EAException


def test_matrixhookshot_uses_custom_title(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'matrixhookshot_webhook_url': 'http://please.dontgohere.matrixhookshot',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = MatrixHookshotAlerter(rule)
    match = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'text': 'Test Rule\n\n@timestamp: 2017-01-01T00:00:00\nsomefield: foobarbaz\n',
    }
    mock_post_request.assert_called_once_with(
        rule['matrixhookshot_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert ('elastalert', logging.INFO, "Alert 'Test Rule' sent to MatrixHookshot") == caplog.record_tuples[0]


def test_matrixhookshot_uses_custom_timeout():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'matrixhookshot_webhook_url': 'http://please.dontgohere.matrixhookshot',
        'alert': [],
        'matrixhookshot_timeout': 20
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = MatrixHookshotAlerter(rule)
    match = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'text': 'Test Rule\n\n@timestamp: 2017-01-01T00:00:00\nsomefield: foobarbaz\n'
    }
    mock_post_request.assert_called_once_with(
        rule['matrixhookshot_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=20
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_matrixhookshot_uses_rule_name_when_custom_title_is_not_provided():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'matrixhookshot_webhook_url': ['http://please.dontgohere.matrixhookshot'],
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = MatrixHookshotAlerter(rule)
    match = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'text': 'Test Rule\n\n@timestamp: 2017-01-01T00:00:00\nsomefield: foobarbaz\n',
    }
    mock_post_request.assert_called_once_with(
        rule['matrixhookshot_webhook_url'][0],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_matrixhookshot_proxy():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'matrixhookshot_webhook_url': 'http://please.dontgohere.matrixhookshot',
        'matrixhookshot_proxy': 'http://proxy.url',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = MatrixHookshotAlerter(rule)
    match = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'text': 'Test Rule\n\n@timestamp: 2017-01-01T00:00:00\nsomefield: foobarbaz\n',
    }
    mock_post_request.assert_called_once_with(
        rule['matrixhookshot_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies={'https': rule['matrixhookshot_proxy']},
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_matrixhookshot_username():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'matrixhookshot_webhook_url': 'http://please.dontgohere.matrixhookshot',
        'matrixhookshot_username': 'test elastalert',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = MatrixHookshotAlerter(rule)
    match = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'text': 'Test Rule\n\n@timestamp: 2017-01-01T00:00:00\nsomefield: foobarbaz\n',
        'username': 'test elastalert',
    }
    mock_post_request.assert_called_once_with(
        rule['matrixhookshot_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_matrixhookshot_text_html():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'matrixhookshot_webhook_url': 'http://please.dontgohere.matrixhookshot',
        'matrixhookshot_text': 'Hello',
        'matrixhookshot_html': '<b>Hello</b>',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = MatrixHookshotAlerter(rule)
    match = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'text': 'Hello',
        'html': '<b>Hello</b>',
    }
    mock_post_request.assert_called_once_with(
        rule['matrixhookshot_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


@pytest.mark.parametrize('ca_certs, ignore_ssl_errors, expect_verify', [
    ('', '', True),
    ('', True, False),
    ('', False, True),
    (True, '', True),
    (True, True, True),
    (True, False, True),
    (False, '', True),
    (False, True, False),
    (False, False, True)
])
def test_matrixhookshot_ca_certs(ca_certs, ignore_ssl_errors, expect_verify):
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'matrixhookshot_webhook_url': 'http://please.dontgohere.matrixhookshot',
        'alert': []
    }
    if ca_certs:
        rule['matrixhookshot_ca_certs'] = ca_certs

    if ignore_ssl_errors:
        rule['matrixhookshot_ignore_ssl_errors'] = ignore_ssl_errors

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = MatrixHookshotAlerter(rule)
    match = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'text': 'Test Rule\n\n@timestamp: 2017-01-01T00:00:00\nsomefield: foobarbaz\n',
    }
    mock_post_request.assert_called_once_with(
        rule['matrixhookshot_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=expect_verify,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_matrixhookshot_ea_exception():
    with pytest.raises(EAException) as ea:
        rule = {
            'name': 'Test Rule',
            'type': 'any',
            'matrixhookshot_webhook_url': 'http://please.dontgohere.matrixhookshot',
            'alert': []
        }
        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = MatrixHookshotAlerter(rule)
        match = {
            '@timestamp': '2017-01-01T00:00:00',
            'somefield': 'foobarbaz'
        }
        mock_run = mock.MagicMock(side_effect=RequestException)
        with mock.patch('requests.post', mock_run), pytest.raises(RequestException):
            alert.alert([match])
    assert 'Error posting to matrixhookshot: ' in str(ea)


def test_matrixhookshot_get_aggregation_summary_text__maximum_width():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'matrixhookshot_webhook_url': 'http://please.dontgohere.matrixhookshot',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = MatrixHookshotAlerter(rule)
    assert 75 == alert.get_aggregation_summary_text__maximum_width()


def test_matrixhookshot_getinfo():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'matrixhookshot_webhook_url': 'http://please.dontgohere.matrixhookshot',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = MatrixHookshotAlerter(rule)

    expected_data = {
        'type': 'matrixhookshot'
    }
    actual_data = alert.get_info()
    assert expected_data == actual_data


@pytest.mark.parametrize('matrixhookshot_webhook_url, expected_data', [
    ('',  'Missing required option(s): matrixhookshot_webhook_url'),
    ('http://please.dontgohere.matrixhookshot',
        {
            'type': 'matrixhookshot',
        }),
])
def test_matrixhookshot_required_error(matrixhookshot_webhook_url, expected_data):
    try:
        rule = {
            'name': 'Test Rule',
            'type': 'any',
            'alert': []
        }

        if matrixhookshot_webhook_url:
            rule['matrixhookshot_webhook_url'] = matrixhookshot_webhook_url

        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = MatrixHookshotAlerter(rule)

        actual_data = alert.get_info()
        assert expected_data == actual_data
    except Exception as ea:
        assert expected_data in str(ea)
