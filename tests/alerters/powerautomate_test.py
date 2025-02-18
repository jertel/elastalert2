import json
import logging
from unittest import mock
import pytest

from elastalert.alerters.powerautomate import MsPowerAutomateAlerter
from elastalert.alerts import BasicMatchString
from elastalert.loaders import FileRulesLoader


def test_ms_power_automate(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'ms_power_automate_webhook_url': 'http://test.webhook.url',
        'ms_power_automate_alert_summary': 'Alert from ElastAlert',
        'alert_subject': 'Cool subject',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = MsPowerAutomateAlerter(rule)
    match = {
        '@timestamp': '2024-07-19T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": rule['ms_power_automate_alert_summary'],
                            "weight": "Bolder",
                            "wrap": True,
                            "size": "large"
                        },
                        {
                            "type": "TextBlock",
                            "text": BasicMatchString(rule, match).__str__(),
                            "spacing": "Large",
                            "wrap": True
                        }
                    ],
                    "actions": []
                }
            }
        ]
    }
    mock_post_request.assert_called_once_with(
        rule['ms_power_automate_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert ('elastalert', logging.INFO, 'Alert sent to Power Automate') == caplog.record_tuples[0]


def test_ms_power_automate_alert_facts():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'ms_power_automate_webhook_url': 'http://test.webhook.url',
        'ms_power_automate_alert_summary': 'Alert from ElastAlert',
        'ms_power_automate_alert_facts': [
            {
                'name': 'Host',
                'value': 'somefield'
            },
            {
                'name': 'Sensors',
                'value': '@timestamp'
            },
            {
                'name': 'Speed',
                'value': 'vehicle.speed'
            },
            {
                'name': 'Boolean',
                'value': 'boolean'
            },
            {
                'name': 'Blank',
                'value': 'blank'
            },
            {
                'name': 'Arbitrary Text Name',
                'value': 'Arbitrary Text Value'
            }
        ],
        'alert_subject': 'Cool subject',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = MsPowerAutomateAlerter(rule)
    match = {
        '@timestamp': '2024-07-19T00:00:00',
        'somefield': 'foobarbaz',
        'vehicle': {
            'speed': 0,
        },
        'boolean': False,
        'blank': ''
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": rule['ms_power_automate_alert_summary'],
                            "weight": "Bolder",
                            "wrap": True,
                            "size": "large"
                        },
                        {
                            "type": "TextBlock",
                            "text": BasicMatchString(rule, match).__str__(),
                            "spacing": "Large",
                            "wrap": True
                        },
                        {
                            "type": "FactSet",
                            "facts": [
                                {'title': 'Host', 'value': 'foobarbaz'},
                                {'title': 'Sensors', 'value': '2024-07-19T00:00:00'},
                                {'title': 'Speed', 'value': 0},
                                {'title': 'Boolean', 'value': False},
                                {'title': 'Blank', 'value': ''},
                                {'title': 'Arbitrary Text Name', 'value': 'Arbitrary Text Value'}
                            ],
                        }
                    ],
                    "actions": []
                }
            }
        ]
    }

    mock_post_request.assert_called_once_with(
        rule['ms_power_automate_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_ms_power_automate_proxy():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'ms_power_automate_webhook_url': 'http://test.webhook.url',
        'ms_power_automate_alert_summary': 'Alert from ElastAlert',
        'ms_power_automate_proxy': 'https://test.proxy.url',
        'alert_subject': 'Cool subject',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = MsPowerAutomateAlerter(rule)
    match = {
        '@timestamp': '2024-07-19T00:00:00',
        'somefield': 'foobarbaz',
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": rule['ms_power_automate_alert_summary'],
                            "weight": "Bolder",
                            "wrap": True,
                            "size": "large"
                        },
                        {
                            "type": "TextBlock",
                            "text": BasicMatchString(rule, match).__str__(),
                            "spacing": "Large",
                            "wrap": True
                        }
                    ],
                    "actions": []
                }
            }
        ]
    }

    mock_post_request.assert_called_once_with(
        rule['ms_power_automate_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies={'https': rule['ms_power_automate_proxy']},
        verify=True
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_ms_power_automate_kibana_discover_attach_url_when_generated():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'ms_power_automate_kibana_discover_attach_url': True,
        'ms_power_automate_webhook_url': 'http://test.webhook.url',
        'ms_power_automate_alert_summary': 'Alert from ElastAlert',
        'alert': [],
        'alert_subject': 'Cool subject',
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = MsPowerAutomateAlerter(rule)
    match = {
        '@timestamp': '2024-07-19T00:00:00',
        'kibana_discover_url': 'http://kibana#discover'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": rule['ms_power_automate_alert_summary'],
                            "weight": "Bolder",
                            "wrap": True,
                            "size": "large"
                        },
                        {
                            "type": "TextBlock",
                            "text": BasicMatchString(rule, match).__str__(),
                            "spacing": "Large",
                            "wrap": True
                        }
                    ],
                    "actions": [
                        {
                            "type": "Action.OpenUrl",
                            "title": "Discover in Kibana",
                            "url": match['kibana_discover_url'],
                            "style": "default"
                        }
                    ],
                }
            }
        ]
    }

    mock_post_request.assert_called_once_with(
        rule['ms_power_automate_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True
    )
    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data


def test_ms_power_automate_kibana_discover_color_when_positive():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'ms_power_automate_kibana_discover_attach_url': 'true',
        'ms_power_automate_kibana_discover_color': 'positive',
        'ms_power_automate_webhook_url': 'http://test.webhook.url',
        'ms_power_automate_alert_summary': 'Alert from ElastAlert',
        'alert': [],
        'alert_subject': 'Cool subject',
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = MsPowerAutomateAlerter(rule)
    match = {
        '@timestamp': '2024-07-19T00:00:00',
        'kibana_discover_url': 'http://kibana#discover'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": rule['ms_power_automate_alert_summary'],
                            "weight": "Bolder",
                            "wrap": True,
                            "size": "large"
                        },
                        {
                            "type": "TextBlock",
                            "text": BasicMatchString(rule, match).__str__(),
                            "spacing": "Large",
                            "wrap": True
                        }
                    ],
                    "actions": [
                        {
                            "type": "Action.OpenUrl",
                            "title": "Discover in Kibana",
                            "url": match['kibana_discover_url'],
                            "style": rule['ms_power_automate_kibana_discover_color']
                        }
                    ],
                }
            }
        ]
    }

    mock_post_request.assert_called_once_with(
        rule['ms_power_automate_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True
    )
    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data


def test_ms_power_automate_kibana_discover_color_when_destructive():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'ms_power_automate_kibana_discover_attach_url': 'true',
        'ms_power_automate_kibana_discover_color': 'destructive',
        'ms_power_automate_webhook_url': 'http://test.webhook.url',
        'ms_power_automate_alert_summary': 'Alert from ElastAlert',
        'alert': [],
        'alert_subject': 'Cool subject',
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = MsPowerAutomateAlerter(rule)
    match = {
        '@timestamp': '2024-07-19T00:00:00',
        'kibana_discover_url': 'http://kibana#discover'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": rule['ms_power_automate_alert_summary'],
                            "weight": "Bolder",
                            "wrap": True,
                            "size": "large"
                        },
                        {
                            "type": "TextBlock",
                            "text": BasicMatchString(rule, match).__str__(),
                            "spacing": "Large",
                            "wrap": True
                        }
                    ],
                    "actions": [
                        {
                            "type": "Action.OpenUrl",
                            "title": "Discover in Kibana",
                            "url": match['kibana_discover_url'],
                            "style": rule['ms_power_automate_kibana_discover_color']
                        }
                    ],
                }
            }
        ]
    }

    mock_post_request.assert_called_once_with(
        rule['ms_power_automate_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True
    )
    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data


def test_ms_power_automate_opensearch_discover_attach_url_when_generated():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'ms_power_automate_opensearch_discover_attach_url': True,
        'ms_power_automate_webhook_url': 'http://test.webhook.url',
        'ms_power_automate_alert_summary': 'Alert from ElastAlert',
        'alert': [],
        'alert_subject': 'Cool subject',
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = MsPowerAutomateAlerter(rule)
    match = {
        '@timestamp': '2024-07-19T00:00:00',
        'opensearch_discover_url': 'http://opensearch#discover'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": rule['ms_power_automate_alert_summary'],
                            "weight": "Bolder",
                            "wrap": True,
                            "size": "large"
                        },
                        {
                            "type": "TextBlock",
                            "text": BasicMatchString(rule, match).__str__(),
                            "spacing": "Large",
                            "wrap": True
                        }
                    ],
                    "actions": [
                        {
                            "type": "Action.OpenUrl",
                            "title": "Discover in opensearch",
                            "url": match['opensearch_discover_url'],
                            "style": "default"
                        }
                    ],
                }
            }
        ]
    }

    mock_post_request.assert_called_once_with(
        rule['ms_power_automate_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True
    )
    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data


def test_ms_power_automate_opensearch_discover_color_when_positive():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'ms_power_automate_opensearch_discover_attach_url': 'true',
        'ms_power_automate_opensearch_discover_color': 'positive',
        'ms_power_automate_webhook_url': 'http://test.webhook.url',
        'ms_power_automate_alert_summary': 'Alert from ElastAlert',
        'alert': [],
        'alert_subject': 'Cool subject',
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = MsPowerAutomateAlerter(rule)
    match = {
        '@timestamp': '2024-07-19T00:00:00',
        'opensearch_discover_url': 'http://opensearch#discover'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": rule['ms_power_automate_alert_summary'],
                            "weight": "Bolder",
                            "wrap": True,
                            "size": "large"
                        },
                        {
                            "type": "TextBlock",
                            "text": BasicMatchString(rule, match).__str__(),
                            "spacing": "Large",
                            "wrap": True
                        }
                    ],
                    "actions": [
                        {
                            "type": "Action.OpenUrl",
                            "title": "Discover in opensearch",
                            "url": match['opensearch_discover_url'],
                            "style": rule['ms_power_automate_opensearch_discover_color']
                        }
                    ],
                }
            }
        ]
    }

    mock_post_request.assert_called_once_with(
        rule['ms_power_automate_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True
    )
    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data


def test_ms_power_automate_opensearch_discover_color_when_destructive():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'ms_power_automate_opensearch_discover_attach_url': 'true',
        'ms_power_automate_opensearch_discover_color': 'destructive',
        'ms_power_automate_webhook_url': 'http://test.webhook.url',
        'ms_power_automate_alert_summary': 'Alert from ElastAlert',
        'alert': [],
        'alert_subject': 'Cool subject',
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = MsPowerAutomateAlerter(rule)
    match = {
        '@timestamp': '2024-07-19T00:00:00',
        'opensearch_discover_url': 'http://opensearch#discover'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": rule['ms_power_automate_alert_summary'],
                            "weight": "Bolder",
                            "wrap": True,
                            "size": "large"
                        },
                        {
                            "type": "TextBlock",
                            "text": BasicMatchString(rule, match).__str__(),
                            "spacing": "Large",
                            "wrap": True
                        }
                    ],
                    "actions": [
                        {
                            "type": "Action.OpenUrl",
                            "title": "Discover in opensearch",
                            "url": match['opensearch_discover_url'],
                            "style": rule['ms_power_automate_opensearch_discover_color']
                        }
                    ],
                }
            }
        ]
    }

    mock_post_request.assert_called_once_with(
        rule['ms_power_automate_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True
    )
    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data


def test_ms_power_automate_teams_card_width_full():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'ms_power_automate_kibana_discover_attach_url': True,
        'ms_power_automate_kibana_discover_color': 'destructive',
        'ms_power_automate_webhook_url': 'http://test.webhook.url',
        'ms_power_automate_alert_summary': 'Alert from ElastAlert',
        'ms_power_automate_teams_card_width_full': True,
        'alert': [],
        'alert_subject': 'Cool subject',
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = MsPowerAutomateAlerter(rule)
    match = {
        '@timestamp': '2024-07-19T00:00:00',
        'kibana_discover_url': 'http://kibana#discover'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": rule['ms_power_automate_alert_summary'],
                            "weight": "Bolder",
                            "wrap": True,
                            "size": "large"
                        },
                        {
                            "type": "TextBlock",
                            "text": BasicMatchString(rule, match).__str__(),
                            "spacing": "Large",
                            "wrap": True
                        }
                    ],
                    "actions": [
                        {
                            "type": "Action.OpenUrl",
                            "title": "Discover in Kibana",
                            "url": match['kibana_discover_url'],
                            "style": rule['ms_power_automate_kibana_discover_color']
                        }
                    ],
                    "msteams": {
                        "width": "Full"
                    }
                }
            }
        ]
    }

    mock_post_request.assert_called_once_with(
        rule['ms_power_automate_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True
    )
    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data


def test_ms_power_automate_kibana_discover_title():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'ms_power_automate_kibana_discover_attach_url': True,
        'ms_power_automate_kibana_discover_color': 'destructive',
        'ms_power_automate_kibana_discover_title': 'See more',
        'ms_power_automate_webhook_url': 'http://test.webhook.url',
        'ms_power_automate_alert_summary': 'Alert from ElastAlert',
        'alert': [],
        'alert_subject': 'Cool subject',
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = MsPowerAutomateAlerter(rule)
    match = {
        '@timestamp': '2024-07-19T00:00:00',
        'kibana_discover_url': 'http://kibana#discover'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": rule['ms_power_automate_alert_summary'],
                            "weight": "Bolder",
                            "wrap": True,
                            "size": "large"
                        },
                        {
                            "type": "TextBlock",
                            "text": BasicMatchString(rule, match).__str__(),
                            "spacing": "Large",
                            "wrap": True
                        }
                    ],
                    "actions": [
                        {
                            "type": "Action.OpenUrl",
                            "title": rule['ms_power_automate_kibana_discover_title'],
                            "url": match['kibana_discover_url'],
                            "style": rule['ms_power_automate_kibana_discover_color']
                        }
                    ],
                }
            }
        ]
    }

    mock_post_request.assert_called_once_with(
        rule['ms_power_automate_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True
    )
    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data


def test_ms_power_automate_summary_text_size_small():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'ms_power_automate_kibana_discover_attach_url': True,
        'ms_power_automate_kibana_discover_color': 'destructive',
        'ms_power_automate_kibana_discover_title': 'See more',
        'ms_power_automate_webhook_url': 'http://test.webhook.url',
        'ms_power_automate_alert_summary': 'Alert from ElastAlert',
        'ms_power_automate_summary_text_size': 'small',
        'alert': [],
        'alert_subject': 'Cool subject',
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = MsPowerAutomateAlerter(rule)
    match = {
        '@timestamp': '2024-07-19T00:00:00',
        'kibana_discover_url': 'http://kibana#discover'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": rule['ms_power_automate_alert_summary'],
                            "weight": "Bolder",
                            "wrap": True,
                            "size": rule['ms_power_automate_summary_text_size']
                        },
                        {
                            "type": "TextBlock",
                            "text": BasicMatchString(rule, match).__str__(),
                            "spacing": "Large",
                            "wrap": True
                        }
                    ],
                    "actions": [
                        {
                            "type": "Action.OpenUrl",
                            "title": rule['ms_power_automate_kibana_discover_title'],
                            "url": match['kibana_discover_url'],
                            "style": rule['ms_power_automate_kibana_discover_color']
                        }
                    ],
                }
            }
        ]
    }

    mock_post_request.assert_called_once_with(
        rule['ms_power_automate_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True
    )
    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data


def test_ms_power_automate_body_text_size_medium():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'ms_power_automate_kibana_discover_attach_url': True,
        'ms_power_automate_kibana_discover_color': 'destructive',
        'ms_power_automate_kibana_discover_title': 'See more',
        'ms_power_automate_webhook_url': 'http://test.webhook.url',
        'ms_power_automate_alert_summary': 'Alert from ElastAlert',
        'ms_power_automate_summary_text_size': 'small',
        'ms_power_automate_body_text_size': 'medium',
        'alert': [],
        'alert_subject': 'Cool subject',
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = MsPowerAutomateAlerter(rule)
    match = {
        '@timestamp': '2024-07-19T00:00:00',
        'kibana_discover_url': 'http://kibana#discover'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": rule['ms_power_automate_alert_summary'],
                            "weight": "Bolder",
                            "wrap": True,
                            "size": rule['ms_power_automate_summary_text_size'],
                        },
                        {
                            "type": "TextBlock",
                            "text": BasicMatchString(rule, match).__str__(),
                            "spacing": "Large",
                            "wrap": True,
                            "size": rule['ms_power_automate_body_text_size']
                        }
                    ],
                    "actions": [
                        {
                            "type": "Action.OpenUrl",
                            "title": rule['ms_power_automate_kibana_discover_title'],
                            "url": match['kibana_discover_url'],
                            "style": rule['ms_power_automate_kibana_discover_color']
                        }
                    ],
                }
            }
        ]
    }

    mock_post_request.assert_called_once_with(
        rule['ms_power_automate_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True
    )
    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data


@pytest.mark.parametrize('match_data, expected_data', [
    ({'webhook_url': 'webhook.com'}, ['webhook.com']),
    ({'webhook_url': 'webhook.com,webhook2.com'}, ['webhook.com', 'webhook2.com']),
    ({}, ['default.com'])
])
def test_ms_power_automate_webhook_url_from_field(match_data, expected_data):
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'ms_power_automate_webhook_url': 'default.com',
        'ms_power_automate_webhook_url_from_field': 'webhook_url',
        'alert': [],
        'alert_subject': 'Cool subject',
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = MsPowerAutomateAlerter(rule)
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match_data])

    for url in expected_data:
        mock_post_request.assert_any_call(
            url,
            data=mock.ANY,
            headers={'content-type': 'application/json'},
            proxies=None,
            verify=True
        )
