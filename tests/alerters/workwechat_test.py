import json
import logging
from unittest import mock

import pytest
from requests import RequestException

from elastalert.alerters.workwechat import WorkWechatAlerter
from elastalert.loaders import FileRulesLoader
from elastalert.util import EAException


def test_work_wechat_text(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test WorkWechat Rule',
        'type': 'any',
        'work_wechat_bot_id': 'xxxxxxx',
        'work_wechat_msgtype': 'text',
        'alert': [],
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = WorkWechatAlerter(rule)
    match = {
        '@timestamp': '2024-01-30T00:00:00',
        'somefield': 'foobar'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'msgtype': 'text',
        'text': {
            'content': 'Test WorkWechat Rule\n\n@timestamp: 2024-01-30T00:00:00\nsomefield: foobar\n'
        }
    }

    mock_post_request.assert_called_once_with(
        'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxx',
        data=mock.ANY,
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json;charset=utf-8'
        }
    )

    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data
    assert ('elastalert', logging.INFO, 'Trigger sent to workwechat') == caplog.record_tuples[0]


def test_work_wechat_ea_exception():
    with pytest.raises(EAException) as ea:
        rule = {
            'name': 'Test WorkWechat Rule',
            'type': 'any',
            'work_wechat_bot_id': 'xxxxxxx',
            'work_wechat_msgtype': 'text',
            'alert': [],
        }
        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = WorkWechatAlerter(rule)
        match = {
            '@timestamp': '2024-01-30T00:00:00',
            'somefield': 'foobar'
        }
        mock_run = mock.MagicMock(side_effect=RequestException)
        with mock.patch('requests.post', mock_run), pytest.raises(RequestException):
            alert.alert([match])
    assert 'Error posting to workwechat: ' in str(ea)


def test_work_wechat_getinfo():
    rule = {
        'name': 'Test WorkWechat Rule',
        'type': 'any',
        'work_wechat_bot_id': 'xxxxxxx',
        'work_wechat_msgtype': 'text',
        'alert': [],
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = WorkWechatAlerter(rule)

    expected_data = {
        'type': 'workwechat',
        'work_wechat_webhook_url': 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxx'
    }
    actual_data = alert.get_info()
    assert expected_data == actual_data


@pytest.mark.parametrize('work_wechat_bot_id, work_wechat_msgtype, expected_data', [
    ('', '', 'Missing required option(s): work_wechat_bot_id, work_wechat_msgtype'),
    ('xxxxxxx', 'yyyyyy',
     {
         'type': 'workwechat',
         'work_wechat_webhook_url': 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxx'
     }),
])
def test_work_wechat_required_error(work_wechat_bot_id, work_wechat_msgtype, expected_data):
    try:
        rule = {
            'name': 'Test WorkWechat Rule',
            'type': 'any',
            'alert': [],
        }

        if work_wechat_bot_id:
            rule['work_wechat_bot_id'] = work_wechat_bot_id

        if work_wechat_msgtype:
            rule['work_wechat_msgtype'] = work_wechat_msgtype

        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = WorkWechatAlerter(rule)

        actual_data = alert.get_info()
        assert expected_data == actual_data
    except Exception as ea:
        assert expected_data in str(ea)
