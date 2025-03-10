import json
import logging

from unittest import mock

from elastalert.alerters.yzj import YzjAlerter
from elastalert.loaders import FileRulesLoader


def test_yzj_text(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test YZJ Rule',
        'type': 'any',
        'yzj_token': 'xxxxxxx',
        'yzj_custom_loc': 'www.myloc.cn',
        'alert': [],
        'alert_subject': 'Test YZJ'
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = YzjAlerter(rule)
    match = {
        '@timestamp': '2021-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }

    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'content': 'Test YZJ Rule\n\n@timestamp: 2021-01-01T00:00:00\nsomefield: foobarbaz\n'
    }

    mock_post_request.assert_called_once_with(
        'https://www.myloc.cn/gateway/robot/webhook/send?yzjtype=0&yzjtoken=xxxxxxx',
        data=mock.ANY,
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json;charset=utf-8'
        },
        proxies=None
    )

    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data
    assert ('elastalert', logging.INFO, 'Trigger sent to YZJ') == caplog.record_tuples[0]
