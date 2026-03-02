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
        'name': 'Test SMSEagle Alerter With SMS Type',
        'type': 'any',
        'smseagle_url': 'http://smseagle_url',
        'smseagle_token': '123abc456def789',
        'smseagle_message_type': 'sms',
        'smseagle_to': ['111222333'],
        'alert': []
    }

    rule['url'] = rule['smseagle_url'] + '/api/v2/messages/sms'

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SMSEagleAlerter(rule)

    match = {
        '@timestamp': '2025-01-30T00:00:00',
        'somefield': 'foobar'
    }
    mock_response = mock.Mock()
    mock_response.status_code = 200
    with mock.patch('requests.post', return_value=mock_response) as mock_post_request:
        alert.alert([match])

    expected_data = {
        'to': ['111222333'],
        'text': 'Test SMSEagle Alerter With SMS Type\n\n@timestamp: 2025-01-30T00:00:00\nsomefield: foobar\n'
    }

    mock_post_request.assert_called_once_with(
        rule['url'],
        json=mock.ANY,
        headers={'content-type': 'application/json', 'access-token': rule['smseagle_token']}
    )

    assert expected_data == mock_post_request.call_args_list[0][1]['json']
    assert ('elastalert', logging.INFO, "Alert 'Test SMSEagle Alerter With SMS Type' sent to SMSEagle") == caplog.record_tuples[0]


def test_smseagle_queue_ring_call(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test SMSEagle Alerter With Ring Type',
        'type': 'any',
        'smseagle_url': 'http://smseagle_url',
        'smseagle_token': '123abc456def789',
        'smseagle_message_type': 'ring',
        'smseagle_to': ['111222333'],
        'alert': []
    }

    rule['url'] = rule['smseagle_url'] + '/api/v2/calls/ring'

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SMSEagleAlerter(rule)

    match = {
        '@timestamp': '2025-01-30T00:00:00',
        'somefield': 'foobar'
    }
    mock_response = mock.Mock()
    mock_response.status_code = 200
    with mock.patch('requests.post', return_value=mock_response) as mock_post_request:
        alert.alert([match])

    expected_data = {
        'to': ['111222333'],
        'duration': 10,
        'text': 'Test SMSEagle Alerter With Ring Type\n\n@timestamp: 2025-01-30T00:00:00\nsomefield: foobar\n'
    }

    mock_post_request.assert_called_once_with(
        rule['url'],
        json=mock.ANY,
        headers={'content-type': 'application/json', 'access-token': rule['smseagle_token']}
    )

    assert expected_data == mock_post_request.call_args_list[0][1]['json']
    assert ('elastalert', logging.INFO, "Alert 'Test SMSEagle Alerter With Ring Type' sent to SMSEagle") == caplog.record_tuples[0]


def test_smseagle_queue_tts_call(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test SMSEagle Alerter With TTS Type',
        'type': 'any',
        'smseagle_url': 'http://smseagle_url',
        'smseagle_token': '123abc456def789',
        'smseagle_message_type': 'tts',
        'smseagle_to': ['111222333'],
        'alert': []
    }

    rule['url'] = rule['smseagle_url'] + '/api/v2/calls/tts'

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SMSEagleAlerter(rule)

    match = {
        '@timestamp': '2025-01-30T00:00:00',
        'somefield': 'foobar'
    }
    mock_response = mock.Mock()
    mock_response.status_code = 200
    with mock.patch('requests.post', return_value=mock_response) as mock_post_request:
        alert.alert([match])

    expected_data = {
        'to': ['111222333'],
        'text': 'Test SMSEagle Alerter With TTS Type\n\n@timestamp: 2025-01-30T00:00:00\nsomefield: foobar\n',
        'duration': 10
    }

    mock_post_request.assert_called_once_with(
        rule['url'],
        json=mock.ANY,
        headers={'content-type': 'application/json', 'access-token': rule['smseagle_token']}
    )

    assert expected_data == mock_post_request.call_args_list[0][1]['json']
    assert ('elastalert', logging.INFO, "Alert 'Test SMSEagle Alerter With TTS Type' sent to SMSEagle") == caplog.record_tuples[0]


def test_smseagle_queue_tts_advanced_call(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test SMSEagle Alerter With TTS Advanced Type',
        'type': 'any',
        'smseagle_url': 'http://smseagle_url',
        'smseagle_token': '123abc456def789',
        'smseagle_message_type': 'tts_adv',
        'smseagle_to': ['111222333'],
        'alert': []
    }

    rule['url'] = rule['smseagle_url'] + '/api/v2/calls/tts_advanced'

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SMSEagleAlerter(rule)

    match = {
        '@timestamp': '2025-01-30T00:00:00',
        'somefield': 'foobar'
    }
    mock_response = mock.Mock()
    mock_response.status_code = 200
    with mock.patch('requests.post', return_value=mock_response) as mock_post_request:
        alert.alert([match])

    expected_data = {
        'to': ['111222333'],
        'text': 'Test SMSEagle Alerter With TTS Advanced Type\n\n@timestamp: 2025-01-30T00:00:00\nsomefield: foobar\n',
        'duration': 10,
        'voice_id': 1
    }

    mock_post_request.assert_called_once_with(
        rule['url'],
        json=mock.ANY,
        headers={'content-type': 'application/json', 'access-token': rule['smseagle_token']}
    )

    assert expected_data == mock_post_request.call_args_list[0][1]['json']
    assert ('elastalert', logging.INFO, "Alert 'Test SMSEagle Alerter With TTS Advanced Type' sent to SMSEagle") == caplog.record_tuples[0]


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
        'name': 'Test SMSEagle Alerter Without Payload',
        'type': 'any',
        'smseagle_url': 'http://smseagle_url',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SMSEagleAlerter(rule)

    expected_data = {
        'type': 'smseagle',
        'smseagle_url': 'http://smseagle_url'
    }
    actual_data = alert.get_info()
    assert expected_data == actual_data


@pytest.mark.parametrize('smseagle_url, expected_data', [
    ('',  'Missing required option(s): smseagle_url'),
    ('http://smseagle_url',
        {
            'type': 'smseagle',
            'smseagle_url': 'http://smseagle_url'
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
