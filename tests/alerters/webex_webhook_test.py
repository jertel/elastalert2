import json
import logging
from unittest import mock

import pytest
from requests import RequestException

from elastalert.alerters.webex_webhook import WebexWebhookAlerter
from elastalert.loaders import FileRulesLoader
from elastalert.util import EAException


def test_webex_webhook_text(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test Webex Webhook Rule',
        'type': 'any',
        'webex_webhook_msgtype': 'text',
        'webex_webhook_id': 'xxxxxxx',
        'alert': [],
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = WebexWebhookAlerter(rule)
    match = {
        '@timestamp': '2024-01-30T00:00:00',
        'somefield': 'foobar'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'text': 'Test Webex Webhook Rule\n\n@timestamp: 2024-01-30T00:00:00\nsomefield: foobar\n'
    }

    mock_post_request.assert_called_once_with(
        'https://webexapis.com/v1/webhooks/incoming/xxxxxxx',
        data=mock.ANY,
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json;charset=utf-8'
        }
    )

    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data
    assert ('elastalert', logging.INFO, 'Trigger sent to webex_webhook') == caplog.record_tuples[0]


def test_webex_webhook_ea_exception():
    with pytest.raises(EAException) as ea:
        rule = {
            'name': 'Test Webex Webhook Rule',
            'type': 'any',
            'webex_webhook_msgtype': 'text',
            'webex_webhook_id': 'xxxxxxx',
            'alert': [],
        }
        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = WebexWebhookAlerter(rule)
        match = {
            '@timestamp': '2024-01-30T00:00:00',
            'somefield': 'foobar'
        }
        mock_run = mock.MagicMock(side_effect=RequestException)
        with mock.patch('requests.post', mock_run), pytest.raises(RequestException):
            alert.alert([match])
    assert 'Error posting to webex_webhook: ' in str(ea)


def test_webex_webhook_getinfo():
    rule = {
        'name': 'Test Webex Webhook Rule',
        'type': 'any',
        'webex_webhook_msgtype': 'text',
        'webex_webhook_id': 'xxxxxxx',
        'alert': [],
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = WebexWebhookAlerter(rule)

    expected_data = {
        'type': 'webex_webhook',
        'webex_webhook_msgtype': 'text',
        'webex_webhook_url': 'https://webexapis.com/v1/webhooks/incoming/xxxxxxx'
    }
    actual_data = alert.get_info()
    assert expected_data == actual_data


@pytest.mark.parametrize('webex_webhook_id, webex_webhook_msgtype, expected_data', [
    ('', '', 'Missing required option(s): webex_webhook_id, webex_webhook_msgtype'),
    ('xxxxxxx', 'yyyyyy',
     {
        'type': 'webex_webhook',
        'webex_webhook_msgtype': 'yyyyyy',
        'webex_webhook_url': 'https://webexapis.com/v1/webhooks/incoming/xxxxxxx'
     }),
])
def test_webex_webhook_required_error(webex_webhook_id, webex_webhook_msgtype, expected_data):
    try:
        rule = {
            'name': 'Test Webex Webhook Rule',
            'type': 'any',
            'alert': [],
        }

        if webex_webhook_id:
            rule['webex_webhook_id'] = webex_webhook_id

        if webex_webhook_msgtype:
            rule['webex_webhook_msgtype'] = webex_webhook_msgtype

        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = WebexWebhookAlerter(rule)

        actual_data = alert.get_info()
        assert expected_data == actual_data
    except Exception as ea:
        assert expected_data in str(ea)
