import json
import logging
import pytest

from unittest import mock

from requests import RequestException

from elastalert.alerters.smseagle import SMSEagleAlerter
from elastalert.loaders import FileRulesLoader
from elastalert.util import EAException


def test_smseagle_sms_with_payload(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test SMSEagle integration',
        'type': 'any',
        'alert': ["smseagle"],
        'smseagle_url': 'http://192.168.1.101',
        'smseagle_token': '123abc456def789',
        'smseagle_message_type': 'sms'
        'smseagle_to': ['111222333']
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SMSEagleAlerter(rule)
    
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
        rule['smseagle_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'}
    )
    
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert ('elastalert', logging.INFO, "Alert 'Test Rule' sent to SMSEagle") == caplog.record_tuples[0]
    

def test_http_alerter_with_payload_all_values():
    rule = {
        'name': 'Test SMSEagle Alerter With Payload',
        'type': 'any',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = HTTPPostAlerter(rule)
    match = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])
    expected_data = {
        'posted_name': 'foobarbaz',
        'name': 'somestaticname',
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    mock_post_request.assert_called_once_with(
        rule['smseagle_url'],
        data=mock.ANY,
        headers={'Content-Type': 'application/json', 'Accept': 'application/json;charset=utf-8'},
        proxies=None,
        timeout=10,
        verify=True
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])
    

def test_smseagle_alerter_without_payload():
    rule = {
        'name': 'Test SMSEagle Alerter Without Payload',
        'type': 'any',
        'smseagle_url': 'http://192.168.1.101',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = HTTPPostAlerter(rule)
    match = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])
    expected_data = {
        '@timestamp': '2017-01-01T00:00:00',
        'somefield': 'foobarbaz',
        'name': 'somestaticname'
    }
    mock_post_request.assert_called_once_with(
        rule['smseagle_url'],
        data=mock.ANY,
        headers={'Content-Type': 'application/json', 'Accept': 'application/json;charset=utf-8'},
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])
    

def test_smseagle_alerter_post_ea_exception():
    with pytest.raises(EAException) as ea:
        rule = {
            'name': 'Test SMSEagle Alerter Without Payload',
            'type': 'any',
            'smseagle_url': 'http://192.168.1.101',
            'alert': []
        }
        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = SMSEagleAlerter(rule)
        match = {
            '@timestamp': '2017-01-01T00:00:00',
            'somefield': 'foobarbaz'
        }
        mock_run = mock.MagicMock(side_effect=RequestException)
        with mock.patch('requests.post', mock_run), pytest.raises(RequestException):
            alert.alert([match])
    assert 'Error posting SMSEagle alert: ' in str(ea)
    

def test_smseagle_get_aggregation_summary_text__maximum_width():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'smseagle_url': 'http://192.168.1.101',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SMSEagleAlerter(rule)
    assert 75 == alert.get_aggregation_summary_text__maximum_width()
    

def test_smseagle_getinfo():
    rule = {
        'name': 'Test SMSEagle Alerter Without Payload',
        'type': 'any',
        'smseagle_url': 'http://192.168.1.101',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = HTTPPostAlerter(rule)

    expected_data = {
        'type': 'smseagle',
        'smseagle_url': ['http://192.168.1.101']
    }
    actual_data = alert.get_info()
    assert expected_data == actual_data
    

@pytest.mark.parametrize('smseagle_url, expected_data', [
    ('',  'Missing required option(s): smseagle_url'),
    ('http://192.168.1.101',
        {
            'type': 'smseagle',
            'smseagle_url': ['http://192.168.1.101']
        }),
])
def test_smseagle_required_error(smseagle_url, expected_data):
    try:
        rule = {
            'name': 'Test SMSEagle Alerter Without Payload',
            'type': 'any',
            'alert': []
        }

        if smseagle_url:
            rule['smseagle_url'] = smseagle_url

        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = SMSEagleAlerter(rule)

        actual_data = alert.get_info()
        assert expected_data == actual_data
    except Exception as ea:
        assert expected_data in str(ea)
