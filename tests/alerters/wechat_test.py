import json

import pytest

from elastalert.loaders import FileRulesLoader
from elastalert.alerters.wechat import WechatAlerter


def test_wechat_getinfo():
    rule = {
        'name': 'Test Wechat Alerter',
        'type': 'any',
        'wechat_corp_id': 'test_wechat_corp_id',
        'wechat_secret': 'test_wechat_secret',
        'wechat_agent_id': 'test_wechat_agent_id',
        'alert': [],
        'alert_subject': 'Test Wechat Alert'
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = WechatAlerter(rule)

    expected_data = {'type': 'wechat'}
    actual_data = alert.get_info()
    assert expected_data == actual_data


@pytest.mark.parametrize('wechat_corp_id, wechat_secret, wechat_agent_id, expected_data', [
    ('', '', '', 'Missing required option(s): wechat_corp_id, wechat_secret, wechat_agent_id'),
    ('xxxx1', '', '', 'Missing required option(s): wechat_corp_id, wechat_secret, wechat_agent_id'),
    ('', 'xxxx2', '', 'Missing required option(s): wechat_corp_id, wechat_secret, wechat_agent_id'),
    ('xxxx1', 'xxxx2', '', 'Missing required option(s): wechat_corp_id, wechat_secret, wechat_agent_id'),
    ('xxxx1', '', 'xxxx3', 'Missing required option(s): wechat_corp_id, wechat_secret, wechat_agent_id'),
    ('', 'xxxx2', 'xxxx3', 'Missing required option(s): wechat_corp_id, wechat_secret, wechat_agent_id'),
    ('xxxx1', 'xxxx2', 'xxxx3',
        {
            'type': 'wechat'
        }),
])
def test_wechat_required_error(wechat_corp_id, wechat_secret, wechat_agent_id, expected_data):
    try:
        rule = {
            'name': 'Test DingTalk Rule',
            'type': 'any',
            'alert': [],
            'alert_subject': 'Test DingTalk'
        }

        if wechat_corp_id != '':
            rule['wechat_corp_id'] = wechat_corp_id
        
        if wechat_secret != '':
            rule['wechat_secret']=wechat_secret

        if wechat_agent_id != '':
            rule['wechat_agent_id'] = wechat_agent_id

        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = WechatAlerter(rule)

        actual_data = alert.get_info()
        assert expected_data == actual_data
    except Exception as ea:
        assert expected_data in str(ea)