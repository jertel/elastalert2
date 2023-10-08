import json
import logging
from unittest import mock

import pytest
from requests import RequestException

from elastalert.alerters.lark import LarkAlerter
from elastalert.loaders import FileRulesLoader
from elastalert.util import EAException


def test_lark_text(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test Lark Rule',
        'type': 'any',
        'lark_bot_id': 'xxxxxxx',
        'lark_msgtype': 'text',
        'alert': [],
        'alert_subject': 'Test Lark'
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = LarkAlerter(rule)
    match = {
        '@timestamp': '2021-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'msg_type': 'text',
        'content': {
            'title': 'Test Lark',
            'text': 'Test Lark Rule\n\n@timestamp: 2021-01-01T00:00:00\nsomefield: foobarbaz\n'
        }
    }

    mock_post_request.assert_called_once_with(
        'https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxx',
        data=mock.ANY,
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json;charset=utf-8'
        }
    )

    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data
    assert ('elastalert', logging.INFO, 'Trigger sent to lark') == caplog.record_tuples[0]


def test_lark_ea_exception():
    with pytest.raises(EAException) as ea:
        rule = {
            'name': 'Test Lark Rule',
            'type': 'any',
            'lark_bot_id': 'xxxxxxx',
            'lark_msgtype': 'action_card',
            'lark_single_title': 'elastalert',
            'lark_single_url': 'http://xxxxx2',
            'lark_btn_orientation': '1',
            'lark_btns': [
                {
                    'title': 'test1',
                    'actionURL': 'https://xxxxx0/'
                },
                {
                    'title': 'test2',
                    'actionURL': 'https://xxxxx1/'
                }
            ],
            'lark_proxy': 'http://proxy.url',
            'lark_proxy_login': 'admin',
            'lark_proxy_pass': 'password',
            'alert': [],
            'alert_subject': 'Test Lark'
        }
        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = LarkAlerter(rule)
        match = {
            '@timestamp': '2021-01-01T00:00:00',
            'somefield': 'foobarbaz'
        }
        mock_run = mock.MagicMock(side_effect=RequestException)
        with mock.patch('requests.post', mock_run), pytest.raises(RequestException):
            alert.alert([match])
    assert 'Error posting to lark: ' in str(ea)


def test_lark_getinfo():
    rule = {
        'name': 'Test Lark Rule',
        'type': 'any',
        'lark_bot_id': 'xxxxxxx',
        'alert': [],
        'alert_subject': 'Test Lark'
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = LarkAlerter(rule)

    expected_data = {
        'type': 'lark',
        "lark_webhook_url": 'https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxx'
    }
    actual_data = alert.get_info()
    assert expected_data == actual_data


@pytest.mark.parametrize('lark_bot_id, expected_data', [
    ('', 'Missing required option(s): lark_bot_id'),
    ('xxxxxxx',
     {
         'type': 'lark',
         "lark_webhook_url": 'https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxx'
     }),
])
def test_lark_required_error(lark_bot_id, expected_data):
    try:
        rule = {
            'name': 'Test Lark Rule',
            'type': 'any',
            'alert': [],
            'alert_subject': 'Test Lark'
        }

        if lark_bot_id:
            rule['lark_bot_id'] = lark_bot_id

        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = LarkAlerter(rule)

        actual_data = alert.get_info()
        assert expected_data == actual_data
    except Exception as ea:
        assert expected_data in str(ea)
