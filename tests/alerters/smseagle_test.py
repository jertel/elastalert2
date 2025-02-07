import json
import logging
import pytest

from unittest import mock

from requests import RequestException

from elastalert.alerters.smseagle import SMSEagleAlerter
from elastalert.loaders import FileRulesLoader
from elastalert.util import EAException


def test_smseagle_send_sms(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test SMSEagle',
        'type': 'any',
        'alert': ["smseagle"],        
        'smseagle_url': 'http://smseagle_url',
        'smseagle_token': '123abc456def789',
        'smseagle_message_type': 'sms',
        'smseagle_to': ['111222333']
    }
    
    rule['url'] = rule['smseagle_url'] + '/messages/sms'
    
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SMSEagleAlerter(rule)
    
    match = {
        '@timestamp': '2025-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'text': 'Test Rule\n\n@timestamp: 2025-01-01T00:00:00\nsomefield: foobarbaz\n'
    }
    
    mock_post_request.assert_called_once_with(
        rule['url'],
        data=mock.ANY,
        headers={'content-type': 'application/json', 'access-token': rule['smseagle_token']}
    )
    
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert ('elastalert', logging.INFO, "Alert 'Test Rule' sent to SMSEagle") == caplog.record_tuples[0]
    

def test_smseagle_alerter_post_ea_exception():
    with pytest.raises(EAException) as ea:
        rule = {
            'name': 'Test SMSEagle',
            'type': 'any',
            'smseagle_url': 'http://smseagle_url',
            'smseagle_token': '123abc456def789',
            'smseagle_message_type': 'sms',
            'smseagle_to': ['111222333'],
            'alert': []
        }
        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = SMSEagleAlerter(rule)
        match = {
            '@timestamp': '2025-01-01T00:00:00',
            'somefield': 'foobarbaz'
        }
        mock_run = mock.MagicMock(side_effect=RequestException)
        with mock.patch('requests.post', mock_run), pytest.raises(RequestException):
            alert.alert([match])
    assert 'Error posting SMSEagle alert: ' in str(ea)
    

def test_smseagle_getinfo():
    rule = {
        'name': 'Test SMSEagle',
        'type': 'any',
        'smseagle_url': 'http://smseagle_url',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SMSEagleAlerter(rule)

    expected_data = {
        'type': 'smseagle',
        'smseagle_url': ['http://smseagle_url']
    }
    actual_data = alert.get_info()
    assert expected_data == actual_data
    

@pytest.mark.parametrize('smseagle_url, expected_data', [
    ('',  'Missing required option(s): smseagle_url'),
    ('http://smseagle_url',
        {
            'type': 'smseagle',
            'smseagle_url': ['http://smseagle_url']
        }),
])
def test_smseagle_required_error(smseagle_url, expected_data):
    try:
        rule = {
            'name': 'Test SMSEagle',
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
