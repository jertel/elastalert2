import logging
import pytest

from unittest import mock
from requests import RequestException

from elastalert.alerters.line import LineMessageAPIAlerter
from elastalert.loaders import FileRulesLoader
from elastalert.util import EAException


def test_line_message(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test LineMessage Rule',
        'type': 'any',
        'line_channel_access_token': 'xxxxx',
        'line_to': 'U1234567890',
        'alert': []
    }

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = LineMessageAPIAlerter(rule)

    match = {
        '@timestamp': '2021-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }

    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_payload = {
        "to": "U1234567890",
        "messages": [
            {
                "type": "text",
                "text": (
                    "Test LineMessage Rule\n\n"
                    "@timestamp: 2021-01-01T00:00:00\n"
                    "somefield: foobarbaz\n"
                )
            }
        ]
    }

    mock_post_request.assert_called_once()
    call = mock_post_request.call_args_list[0][1]

    assert call["headers"] == {
        "Content-Type": "application/json",
        "Authorization": "Bearer xxxxx"
    }

    # JSON comparison
    import json
    assert json.loads(call["data"]) == expected_payload

    assert ("elastalert", logging.INFO, "Alert sent to LINE Messaging API") \
           in caplog.record_tuples


def test_line_message_ea_exception():
    with pytest.raises(EAException) as ea:
        rule = {
            'name': 'Test LineMessage Rule',
            'type': 'any',
            'line_channel_access_token': 'xxxxx',
            'line_to': 'U12345',
            'alert': []
        }

        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = LineMessageAPIAlerter(rule)

        match = {
            '@timestamp': '2021-01-01T00:00:00',
            'somefield': 'foobarbaz'
        }

        mock_run = mock.MagicMock(side_effect=RequestException)
        with mock.patch('requests.post', mock_run):
            alert.alert([match])

    assert 'Error posting to LINE Messaging API: ' in str(ea)


def test_line_message_getinfo():
    rule = {
        'name': 'Test LineMessage Rule',
        'type': 'any',
        'line_channel_access_token': 'xxxxx',
        'line_to': 'U12345',
        'alert': []
    }

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = LineMessageAPIAlerter(rule)

    expected_info = {
        "type": "line",
        "line_to": "U12345",
        "line_channel_access_token": "xxxxx"
    }

    assert alert.get_info() == expected_info


@pytest.mark.parametrize('token,to_value,expected_data', [
    ('', '', 'Missing required option(s): line_channel_access_token, line_to'),
    ('xxxxx', '', 'Missing required option(s): line_to'),
    ('', 'U999', 'Missing required option(s): line_channel_access_token'),
    ('xxxxx', 'U999', {
        "type": "line",
        "line_to": "U999",
        "line_channel_access_token": "xxxxx"
    }),
])
def test_line_message_required(token, to_value, expected_data):
    rule = {
        'name': 'Test LineMessage Rule',
        'type': 'any',
        'alert': []
    }

    if token:
        rule['line_channel_access_token'] = token
    if to_value:
        rule['line_to'] = to_value

    try:
        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = LineMessageAPIAlerter(rule)

        assert alert.get_info() == expected_data
    except Exception as e:
        assert expected_data in str(e)


def test_line_message_matchs():
    rule = {
        'name': 'Test LineMessage Rule',
        'type': 'any',
        'line_channel_access_token': 'xxxxx',
        'line_to': 'U1234567890',
        'alert': []
    }

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = LineMessageAPIAlerter(rule)

    match = {
        '@timestamp': '2021-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }

    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match, match])

    expected_text = (
        "Test LineMessage Rule\n\n"
        "@timestamp: 2021-01-01T00:00:00\n"
        "somefield: foobarbaz\n\n"
        "----------------------------------------\n"
        "Test LineMessage Rule\n\n"
        "@timestamp: 2021-01-01T00:00:00\n"
        "somefield: foobarbaz\n\n"
        "----------------------------------------\n"
    )

    import json
    call = mock_post_request.call_args_list[0][1]
    payload = json.loads(call["data"])

    assert payload == {
        "to": "U1234567890",
        "messages": [
            {"type": "text", "text": expected_text}
        ]
    }
