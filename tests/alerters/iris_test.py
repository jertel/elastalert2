import logging

from unittest import mock
from unittest.mock import patch
from datetime import datetime

from elastalert.alerters.iris import IrisAlerter
from elastalert.loaders import FileRulesLoader


def test_iris_make_alert_context_records(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test Context',
        'type': 'any',
        'iris_type': 'alert',
        'iris_host': '127.0.0.1',
        'iris_api_token': 'token 12345',
        'iris_customer_id': 1,
        'iris_alert_context': {'username': 'username', 'ip': 'src_ip', 'login_status': 'event_status'},
        'alert': []
    }

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IrisAlerter(rule)

    match = {
        '@timestamp': '2023-10-21 20:00:00.000', 'username': 'evil_user', 'src_ip': '172.20.1.1', 'dst_ip': '10.0.0.1',
        'event_type': 'login', 'event_status': 'success'
    }

    expected_data = {
        'username': 'evil_user',
        'ip': '172.20.1.1',
        'login_status': 'success'
    }

    actual_data = alert.make_alert_context_records([match])

    assert expected_data == actual_data


def test_iris_make_iocs_records(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test Context',
        'type': 'any',
        'iris_type': 'alert',
        'iris_host': '127.0.0.1',
        'iris_api_token': 'token 12345',
        'iris_customer_id': 1,
        'iris_iocs': [
            {
                'ioc_description': 'source address',
                'ioc_tags': 'ip, ipv4',
                'ioc_tlp_id': 1,
                'ioc_type_id': 76,
                'ioc_value': 'src_ip'
            },
            {
                'ioc_description': 'target username',
                'ioc_tags': 'login, username',
                'ioc_tlp_id': 3,
                'ioc_type_id': 3,
                'ioc_value': 'username'
            },
            {
                'ioc_description': 'empty ioc',
                'ioc_tags': 'ioc',
                'ioc_tlp_id': 3,
                'ioc_type_id': 3,
                'ioc_value': 'non_existent_data'
            }
        ],
        'alert': []
    }

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IrisAlerter(rule)

    match = {
        '@timestamp': '2023-10-21 20:00:00.000', 'username': 'evil_user', 'src_ip': '172.20.1.1', 'dst_ip': '10.0.0.1',
        'event_type': 'login', 'event_status': 'success'
    }

    expected_data = [
        {
            'ioc_description': 'source address',
            'ioc_tags': 'ip, ipv4',
            'ioc_tlp_id': 1,
            'ioc_type_id': 76,
            'ioc_value': '172.20.1.1'
        },
        {
            'ioc_description': 'target username',
            'ioc_tags': 'login, username',
            'ioc_tlp_id': 3,
            'ioc_type_id': 3,
            'ioc_value': 'evil_user'
        }
    ]

    actual_data = alert.make_iocs_records([match])
    assert expected_data == actual_data


def test_iris_handle_multiple_alerts_with_iocs(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test Context',
        'type': 'any',
        'iris_type': 'alert',
        'iris_host': '127.0.0.1',
        'iris_api_token': 'token 12345',
        'iris_customer_id': 1,
        'iris_iocs': [
            {
                'ioc_description': 'source address',
                'ioc_tags': 'ip, ipv4',
                'ioc_tlp_id': 1,
                'ioc_type_id': 76,
                'ioc_value': 'src_ip'
            },
            {
                'ioc_description': 'target username',
                'ioc_tags': 'login, username',
                'ioc_tlp_id': 3,
                'ioc_type_id': 3,
                'ioc_value': 'username'
            },
            {
                'ioc_description': 'empty ioc',
                'ioc_tags': 'ioc',
                'ioc_tlp_id': 3,
                'ioc_type_id': 3,
                'ioc_value': 'non_existent_data'
            }
        ],
        'alert': []
    }

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IrisAlerter(rule)

    match = {
        '@timestamp': '2023-10-21 20:00:00.000', 'username': 'evil_user', 'src_ip': '172.20.1.1', 'dst_ip': '10.0.0.1',
        'event_type': 'login', 'event_status': 'success'
    }

    expected_data = [
        {
            'ioc_description': 'source address',
            'ioc_tags': 'ip, ipv4',
            'ioc_tlp_id': 1,
            'ioc_type_id': 76,
            'ioc_value': '172.20.1.1'
        },
        {
            'ioc_description': 'target username',
            'ioc_tags': 'login, username',
            'ioc_tlp_id': 3,
            'ioc_type_id': 3,
            'ioc_value': 'evil_user'
        }
    ]

    # Submitting a bogus alert to test follow up alerts
    alert.make_iocs_records([match])
    actual_data = alert.make_iocs_records([match])
    assert expected_data == actual_data


def test_iris_make_alert_minimal(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test Minimal Alert Body',
        'type': 'any',
        'iris_host': '127.0.0.1',
        'iris_api_token': 'token 12345',
        'iris_customer_id': 1,
        'alert': [],
    }

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IrisAlerter(rule)

    match = {
        '@timestamp': '2023-10-21 20:00:00.000', 'username': 'evil_user', 'src_ip': '172.20.1.1', 'dst_ip': '10.0.0.1',
        'event_type': 'login', 'event_status': 'success'
    }

    expected_data = {
        "alert_title": 'Test Minimal Alert Body',
        "alert_description": "Test Minimal Alert Body\n\n@timestamp: 2023-10-21 20:00:00.000\ndst_ip: 10.0.0.1\n\
event_status: success\nevent_type: login\nsrc_ip: 172.20.1.1\nusername: evil_user\n",
        "alert_source": "ElastAlert2",
        "alert_severity_id": 1,
        "alert_status_id": 2,
        "alert_source_event_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "alert_note": None,
        "alert_tags": None,
        "alert_customer_id": 1
    }

    actual_data = alert.make_alert([match])
    assert expected_data == actual_data


def test_iris_make_alert_maximal(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test Maximal Alert Body',
        'type': 'any',
        'iris_host': '127.0.0.1',
        'iris_api_token': 'token 12345',
        'iris_customer_id': 1,
        'iris_description': 'test description in alert',
        'iris_alert_note': 'test note',
        'iris_alert_tags': 'test, alert',
        'iris_overwrite_timestamp': True,
        'iris_alert_source_link': 'https://example.com',
        'iris_alert_source': "TestSource",
        'iris_iocs': [
            {
                'ioc_description': 'source address',
                'ioc_tags': 'ip, ipv4',
                'ioc_tlp_id': 1,
                'ioc_type_id': 76,
                'ioc_value': 'src_ip'
            },
            {
                'ioc_description': 'target username',
                'ioc_tags': 'login, username',
                'ioc_tlp_id': 3,
                'ioc_type_id': 3,
                'ioc_value': 'username'
            }
        ],
        'iris_alert_context': {'username': 'username', 'ip': 'src_ip', 'login_status': 'event_status'},
        'alert': [],
    }

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IrisAlerter(rule)

    match = {
        '@timestamp': '2023-10-21 20:00:00.000', 'username': 'evil_user', 'src_ip': '172.20.1.1', 'dst_ip': '10.0.0.1',
        'event_type': 'login', 'event_status': 'success'
    }

    expected_data = {
        "alert_title": 'Test Maximal Alert Body',
        "alert_description": 'test description in alert',
        "alert_source": "TestSource",
        "alert_severity_id": 1,
        "alert_status_id": 2,
        "alert_source_event_time": '2023-10-21 20:00:00.000',
        "alert_note": 'test note',
        "alert_tags": 'test, alert',
        "alert_customer_id": 1,
        "alert_source_link": 'https://example.com',
        "alert_iocs": [
            {
                'ioc_description': 'source address',
                'ioc_tags': 'ip, ipv4',
                'ioc_tlp_id': 1,
                'ioc_type_id': 76,
                'ioc_value': '172.20.1.1'
            },
            {
                'ioc_description': 'target username',
                'ioc_tags': 'login, username',
                'ioc_tlp_id': 3,
                'ioc_type_id': 3,
                'ioc_value': 'evil_user'
            }
        ],
        "alert_context": {
            'username': 'evil_user',
            'ip': '172.20.1.1',
            'login_status': 'success'
        },
    }

    actual_data = alert.make_alert([match])
    assert expected_data == actual_data


def test_iris_make_alert_auto_description(caplog):
    """Test for the built-in elastalert2 create_title and create_body functions

    These functions use the alert_subject and alert_text fields to automatically
    build the title and description based on alert match data if available.
    """

    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test Maximal Alert Body',
        'alert_subject': 'Test Alert Subject',
        'alert_text': 'Test alert text',
        'type': 'any',
        'iris_host': '127.0.0.1',
        'iris_api_token': 'token 12345',
        'iris_customer_id': 1,
        'iris_alert_note': 'test note',
        'iris_alert_tags': 'test, alert',
        'iris_overwrite_timestamp': True,
        'iris_alert_source_link': 'https://example.com',
        'iris_iocs': [
            {
                'ioc_description': 'source address',
                'ioc_tags': 'ip, ipv4',
                'ioc_tlp_id': 1,
                'ioc_type_id': 76,
                'ioc_value': 'src_ip'
            },
            {
                'ioc_description': 'target username',
                'ioc_tags': 'login, username',
                'ioc_tlp_id': 3,
                'ioc_type_id': 3,
                'ioc_value': 'username'
            }
        ],
        'iris_alert_context': {'username': 'username', 'ip': 'src_ip', 'login_status': 'event_status'},
        'alert': [],
    }

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IrisAlerter(rule)

    match = {
        '@timestamp': '2023-10-21 20:00:00.000', 'username': 'evil_user', 'src_ip': '172.20.1.1', 'dst_ip': '10.0.0.1',
        'event_type': 'login', 'event_status': 'success'
    }

    expected_data = {
        "alert_title": 'Test Alert Subject',
        "alert_description": 'Test alert text\n\n@timestamp: 2023-10-21 20:00:00.000\ndst_ip: 10.0.0.1\n\
event_status: success\nevent_type: login\nsrc_ip: 172.20.1.1\nusername: evil_user\n',
        "alert_source": "ElastAlert2",
        "alert_severity_id": 1,
        "alert_status_id": 2,
        "alert_source_event_time": '2023-10-21 20:00:00.000',
        "alert_note": 'test note',
        "alert_tags": 'test, alert',
        "alert_customer_id": 1,
        "alert_source_link": 'https://example.com',
        "alert_iocs": [
            {
                'ioc_description': 'source address',
                'ioc_tags': 'ip, ipv4',
                'ioc_tlp_id': 1,
                'ioc_type_id': 76,
                'ioc_value': '172.20.1.1'
            },
            {
                'ioc_description': 'target username',
                'ioc_tags': 'login, username',
                'ioc_tlp_id': 3,
                'ioc_type_id': 3,
                'ioc_value': 'evil_user'
            }
        ],
        "alert_context": {
            'username': 'evil_user',
            'ip': '172.20.1.1',
            'login_status': 'success'
        },
    }

    actual_data = alert.make_alert([match])
    assert expected_data == actual_data


def test_iris_make_alert_auto_description_realert(caplog):
    """Test for the built-in elastalert2 create_title and create_body functions

    These functions use the alert_subject and alert_text fields to automatically
    build the title and description based on alert match data if available.
    Testing for a bug where follow up alerts are having their description
    overwritten. This time testing with a filled description.
    """

    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test Maximal Alert Body',
        'alert_subject': 'Test Alert Subject',
        'alert_text': 'Test alert text',
        'type': 'any',
        'iris_host': '127.0.0.1',
        'iris_api_token': 'token 12345',
        'iris_customer_id': 1,
        'iris_alert_note': 'test note',
        'iris_alert_tags': 'test, alert',
        'iris_overwrite_timestamp': True,
        'iris_alert_source_link': 'https://example.com',
        'iris_iocs': [
            {
                'ioc_description': 'source address',
                'ioc_tags': 'ip, ipv4',
                'ioc_tlp_id': 1,
                'ioc_type_id': 76,
                'ioc_value': 'src_ip'
            },
            {
                'ioc_description': 'target username',
                'ioc_tags': 'login, username',
                'ioc_tlp_id': 3,
                'ioc_type_id': 3,
                'ioc_value': 'username'
            }
        ],
        'iris_alert_context': {'username': 'username', 'ip': 'src_ip', 'login_status': 'event_status'},
        'alert': [],
    }

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IrisAlerter(rule)

    first_match = {
        '@timestamp': '2023-10-21 20:00:00.000', 'username': 'evil_user', 'src_ip': '172.20.1.1', 'dst_ip': '10.0.0.1',
        'event_type': 'login', 'event_status': 'success'
    }

    first_expected_data = {
        "alert_title": 'Test Alert Subject',
        "alert_description": 'Test alert text\n\n@timestamp: 2023-10-21 20:00:00.000\ndst_ip: 10.0.0.1\n\
event_status: success\nevent_type: login\nsrc_ip: 172.20.1.1\nusername: evil_user\n',
        "alert_source": "ElastAlert2",
        "alert_severity_id": 1,
        "alert_status_id": 2,
        "alert_source_event_time": '2023-10-21 20:00:00.000',
        "alert_note": 'test note',
        "alert_tags": 'test, alert',
        "alert_customer_id": 1,
        "alert_source_link": 'https://example.com',
        "alert_iocs": [
            {
                'ioc_description': 'source address',
                'ioc_tags': 'ip, ipv4',
                'ioc_tlp_id': 1,
                'ioc_type_id': 76,
                'ioc_value': '172.20.1.1'
            },
            {
                'ioc_description': 'target username',
                'ioc_tags': 'login, username',
                'ioc_tlp_id': 3,
                'ioc_type_id': 3,
                'ioc_value': 'evil_user'
            }
        ],
        "alert_context": {
            'username': 'evil_user',
            'ip': '172.20.1.1',
            'login_status': 'success'
        },
    }

    second_match = {
        '@timestamp': '2023-10-21 20:00:00.000', 'username': 'good_user', 'src_ip': '192.168.125.33', 'dst_ip': '216.73.245.89',
        'event_type': 'login', 'event_status': 'failure'
    }

    second_expected_data = {
        "alert_title": 'Test Alert Subject',
        "alert_description": 'Test alert text\n\n@timestamp: 2023-10-21 20:00:00.000\ndst_ip: 216.73.245.89\n\
event_status: failure\nevent_type: login\nsrc_ip: 192.168.125.33\nusername: good_user\n',
        "alert_source": "ElastAlert2",
        "alert_severity_id": 1,
        "alert_status_id": 2,
        "alert_source_event_time": '2023-10-21 20:00:00.000',
        "alert_note": 'test note',
        "alert_tags": 'test, alert',
        "alert_customer_id": 1,
        "alert_source_link": 'https://example.com',
        "alert_iocs": [
            {
                'ioc_description': 'source address',
                'ioc_tags': 'ip, ipv4',
                'ioc_tlp_id': 1,
                'ioc_type_id': 76,
                'ioc_value': '192.168.125.33'
            },
            {
                'ioc_description': 'target username',
                'ioc_tags': 'login, username',
                'ioc_tlp_id': 3,
                'ioc_type_id': 3,
                'ioc_value': 'good_user'
            }
        ],
        "alert_context": {
            'username': 'good_user',
            'ip': '192.168.125.33',
            'login_status': 'failure'
        },
    }

    first_data = alert.make_alert([first_match])
    second_data = alert.make_alert([second_match])

    assert first_expected_data == first_data
    assert second_expected_data == second_data


def test_iris_make_alert_auto_blank_description_realert(caplog):
    """Test for the built-in elastalert2 create_title and create_body functions

    These functions use the alert_subject and alert_text fields to automatically
    build the title and description based on alert match data if available.
    Testing for a bug where follow up alerts are having their description
    overwritten. This time testing with a blank description.
    """

    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test Maximal Alert Body',
        'alert_subject': 'Test Alert Subject',
        'alert_text': '',
        'type': 'any',
        'iris_host': '127.0.0.1',
        'iris_api_token': 'token 12345',
        'iris_customer_id': 1,
        'iris_alert_note': 'test note',
        'iris_alert_tags': 'test, alert',
        'iris_overwrite_timestamp': True,
        'iris_alert_source_link': 'https://example.com',
        'iris_iocs': [
            {
                'ioc_description': 'source address',
                'ioc_tags': 'ip, ipv4',
                'ioc_tlp_id': 1,
                'ioc_type_id': 76,
                'ioc_value': 'src_ip'
            },
            {
                'ioc_description': 'target username',
                'ioc_tags': 'login, username',
                'ioc_tlp_id': 3,
                'ioc_type_id': 3,
                'ioc_value': 'username'
            }
        ],
        'iris_alert_context': {'username': 'username', 'ip': 'src_ip', 'login_status': 'event_status'},
        'alert': [],
    }

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IrisAlerter(rule)

    first_match = {
        '@timestamp': '2023-10-21 20:00:00.000', 'username': 'evil_user', 'src_ip': '172.20.1.1', 'dst_ip': '10.0.0.1',
        'event_type': 'login', 'event_status': 'success'
    }

    first_expected_data = {
        "alert_title": 'Test Alert Subject',
        "alert_description": '\n\n@timestamp: 2023-10-21 20:00:00.000\ndst_ip: 10.0.0.1\n\
event_status: success\nevent_type: login\nsrc_ip: 172.20.1.1\nusername: evil_user\n',
        "alert_source": "ElastAlert2",
        "alert_severity_id": 1,
        "alert_status_id": 2,
        "alert_source_event_time": '2023-10-21 20:00:00.000',
        "alert_note": 'test note',
        "alert_tags": 'test, alert',
        "alert_customer_id": 1,
        "alert_source_link": 'https://example.com',
        "alert_iocs": [
            {
                'ioc_description': 'source address',
                'ioc_tags': 'ip, ipv4',
                'ioc_tlp_id': 1,
                'ioc_type_id': 76,
                'ioc_value': '172.20.1.1'
            },
            {
                'ioc_description': 'target username',
                'ioc_tags': 'login, username',
                'ioc_tlp_id': 3,
                'ioc_type_id': 3,
                'ioc_value': 'evil_user'
            }
        ],
        "alert_context": {
            'username': 'evil_user',
            'ip': '172.20.1.1',
            'login_status': 'success'
        },
    }

    second_match = {
        '@timestamp': '2023-10-21 20:00:00.000', 'username': 'good_user', 'src_ip': '192.168.125.33', 'dst_ip': '216.73.245.89',
        'event_type': 'login', 'event_status': 'failure'
    }

    second_expected_data = {
        "alert_title": 'Test Alert Subject',
        "alert_description": '\n\n@timestamp: 2023-10-21 20:00:00.000\ndst_ip: 216.73.245.89\n\
event_status: failure\nevent_type: login\nsrc_ip: 192.168.125.33\nusername: good_user\n',
        "alert_source": "ElastAlert2",
        "alert_severity_id": 1,
        "alert_status_id": 2,
        "alert_source_event_time": '2023-10-21 20:00:00.000',
        "alert_note": 'test note',
        "alert_tags": 'test, alert',
        "alert_customer_id": 1,
        "alert_source_link": 'https://example.com',
        "alert_iocs": [
            {
                'ioc_description': 'source address',
                'ioc_tags': 'ip, ipv4',
                'ioc_tlp_id': 1,
                'ioc_type_id': 76,
                'ioc_value': '192.168.125.33'
            },
            {
                'ioc_description': 'target username',
                'ioc_tags': 'login, username',
                'ioc_tlp_id': 3,
                'ioc_type_id': 3,
                'ioc_value': 'good_user'
            }
        ],
        "alert_context": {
            'username': 'good_user',
            'ip': '192.168.125.33',
            'login_status': 'failure'
        },
    }

    first_data = alert.make_alert([first_match])
    second_data = alert.make_alert([second_match])

    assert first_expected_data == first_data
    assert second_expected_data == second_data


def test_iris_make_alert_auto_description_args(caplog):
    """Test for the built-in elastalert2 create_title and create_body functions

    These functions use the alert_subject and alert_text fields to automatically
    build the title and description based on alert match data if available.

    This test specifically uses _args for the alert_text to ensure match args
    are passed through properly.
    """
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test Maximal Alert Body',
        'alert_subject': 'Test Alert Subject',
        'alert_text': 'Username: {0} from {1}',
        'alert_text_type': 'alert_text_only',
        'alert_text_args': ['username', 'src_ip'],
        'type': 'any',
        'iris_host': '127.0.0.1',
        'iris_api_token': 'token 12345',
        'iris_customer_id': 1,
        'iris_alert_note': 'test note',
        'iris_alert_tags': 'test, alert',
        'iris_overwrite_timestamp': True,
        'iris_alert_source_link': 'https://example.com',
        'iris_iocs': [
            {
                'ioc_description': 'source address',
                'ioc_tags': 'ip, ipv4',
                'ioc_tlp_id': 1,
                'ioc_type_id': 76,
                'ioc_value': 'src_ip'
            },
            {
                'ioc_description': 'target username',
                'ioc_tags': 'login, username',
                'ioc_tlp_id': 3,
                'ioc_type_id': 3,
                'ioc_value': 'username'
            }
        ],
        'iris_alert_context': {'username': 'username', 'ip': 'src_ip', 'login_status': 'event_status'},
        'alert': [],
    }

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IrisAlerter(rule)

    match = {
        '@timestamp': '2023-10-21 20:00:00.000', 'username': 'evil_user', 'src_ip': '172.20.1.1', 'dst_ip': '10.0.0.1',
        'event_type': 'login', 'event_status': 'success'
    }

    expected_data = {
        "alert_title": 'Test Alert Subject',
        "alert_description": 'Username: evil_user from 172.20.1.1\n\n',
        "alert_source": "ElastAlert2",
        "alert_severity_id": 1,
        "alert_status_id": 2,
        "alert_source_event_time": '2023-10-21 20:00:00.000',
        "alert_note": 'test note',
        "alert_tags": 'test, alert',
        "alert_customer_id": 1,
        "alert_source_link": 'https://example.com',
        "alert_iocs": [
            {
                'ioc_description': 'source address',
                'ioc_tags': 'ip, ipv4',
                'ioc_tlp_id': 1,
                'ioc_type_id': 76,
                'ioc_value': '172.20.1.1'
            },
            {
                'ioc_description': 'target username',
                'ioc_tags': 'login, username',
                'ioc_tlp_id': 3,
                'ioc_type_id': 3,
                'ioc_value': 'evil_user'
            }
        ],
        "alert_context": {
            'username': 'evil_user',
            'ip': '172.20.1.1',
            'login_status': 'success'
        },
    }

    actual_data = alert.make_alert([match])
    assert expected_data == actual_data


def test_iris_make_alert_maximal_with_nested_json(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test Maximal Alert Body',
        'type': 'any',
        'iris_host': '127.0.0.1',
        'iris_api_token': 'token 12345',
        'iris_customer_id': 1,
        'iris_description': 'test description in alert',
        'iris_alert_note': 'test note',
        'iris_alert_tags': 'test, alert',
        'iris_overwrite_timestamp': True,
        'iris_alert_source_link': 'https://example.com',
        'iris_alert_source': "TestSource",
        'iris_iocs': [
            {
                'ioc_description': 'source address',
                'ioc_tags': 'ip, ipv4',
                'ioc_tlp_id': 1,
                'ioc_type_id': 76,
                'ioc_value': 'host.src_ip'
            },
            {
                'ioc_description': 'target username',
                'ioc_tags': 'login, username',
                'ioc_tlp_id': 3,
                'ioc_type_id': 3,
                'ioc_value': 'username'
            }
        ],
        'iris_alert_context': {'username': 'username', 'ip': 'host.src_ip', 'login_status': 'event_status'},
        'alert': [],
    }

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IrisAlerter(rule)

    match = {
        '@timestamp': '2023-10-21 20:00:00.000', 'username': 'evil_user', 'host': {'src_ip': '172.20.1.1'}, 'dst_ip': '10.0.0.1',
        'event_type': 'login', 'event_status': 'success'
    }

    expected_data = {
        "alert_title": 'Test Maximal Alert Body',
        "alert_description": 'test description in alert',
        "alert_source": "TestSource",
        "alert_severity_id": 1,
        "alert_status_id": 2,
        "alert_source_event_time": '2023-10-21 20:00:00.000',
        "alert_note": 'test note',
        "alert_tags": 'test, alert',
        "alert_customer_id": 1,
        "alert_source_link": 'https://example.com',
        "alert_iocs": [
            {
                'ioc_description': 'source address',
                'ioc_tags': 'ip, ipv4',
                'ioc_tlp_id': 1,
                'ioc_type_id': 76,
                'ioc_value': '172.20.1.1'
            },
            {
                'ioc_description': 'target username',
                'ioc_tags': 'login, username',
                'ioc_tlp_id': 3,
                'ioc_type_id': 3,
                'ioc_value': 'evil_user'
            }
        ],
        "alert_context": {
            'username': 'evil_user',
            'ip': '172.20.1.1',
            'login_status': 'success'
        },
    }

    actual_data = alert.make_alert([match])
    assert expected_data == actual_data


def test_iris_make_case_minimal(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test Minimal Case',
        'type': 'any',
        'iris_host': '127.0.0.1',
        'iris_api_token': 'token 12345',
        'iris_type': 'case',
        'iris_customer_id': 1,
        'alert': [],
    }

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IrisAlerter(rule)

    match = {
        '@timestamp': '2023-10-21 20:00:00.000', 'username': 'evil_user', 'src_ip': '172.20.1.1', 'dst_ip': '10.0.0.1',
        'event_type': 'login', 'event_status': 'success'
    }

    expected_data = {
        "case_soc_id": "SOC_123456",
        "case_customer": 1,
        "case_name": "Test Minimal Case",
        "case_description": None
    }

    with patch('uuid.uuid4', return_value='123456'):
        actual_data, actual_data_iocs = alert.make_case([match])

    assert expected_data == actual_data


def test_iris_make_case_maximal(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test Maximal Case',
        'type': 'any',
        'iris_host': '127.0.0.1',
        'iris_api_token': 'token 12345',
        'iris_type': 'case',
        'iris_customer_id': 1,
        'iris_case_template_id': 55,
        'iris_iocs': [
            {
                'ioc_description': 'source address',
                'ioc_tags': 'ip, ipv4',
                'ioc_tlp_id': 1,
                'ioc_type_id': 76,
                'ioc_value': 'src_ip'
            },
            {
                'ioc_description': 'target username',
                'ioc_tags': 'login, username',
                'ioc_tlp_id': 3,
                'ioc_type_id': 3,
                'ioc_value': 'username'
            }
        ],
        'alert': [],
    }

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IrisAlerter(rule)

    match = {
        '@timestamp': '2023-10-21 20:00:00.000', 'username': 'evil_user', 'src_ip': '172.20.1.1', 'dst_ip': '10.0.0.1',
        'event_type': 'login', 'event_status': 'success'
    }

    expected_data = {
        "case_soc_id": "SOC_123456",
        "case_customer": 1,
        "case_name": "Test Maximal Case",
        "case_description": None,
        "case_template_id": 55,
    }

    expected_data_iocs = [
        {
            'ioc_description': 'source address',
            'ioc_tags': 'ip, ipv4',
            'ioc_tlp_id': 1,
            'ioc_type_id': 76,
            'ioc_value': '172.20.1.1'
        },
        {
            'ioc_description': 'target username',
            'ioc_tags': 'login, username',
            'ioc_tlp_id': 3,
            'ioc_type_id': 3,
            'ioc_value': 'evil_user'
        }
    ]

    with patch('uuid.uuid4', return_value='123456'):
        actual_data, actual_data_iocs = alert.make_case([match])

    assert expected_data == actual_data
    assert expected_data_iocs == actual_data_iocs


def test_iris_alert_alert(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test Main',
        'type': 'any',
        'iris_host': '127.0.0.1',
        'iris_api_token': 'token 12345',
        'iris_description': 'test description in alert',
        'iris_alert_note': 'test note',
        'iris_alert_tags': 'test, alert',
        'iris_overwrite_timestamp': True,
        'iris_alert_source_link': 'https://example.com',
        'iris_iocs': [
            {
                'ioc_description': 'source address',
                'ioc_tags': 'ip, ipv4',
                'ioc_tlp_id': 1,
                'ioc_type_id': 76,
                'ioc_value': 'src_ip'
            },
            {
                'ioc_description': 'target username',
                'ioc_tags': 'login, username',
                'ioc_tlp_id': 3,
                'ioc_type_id': 3,
                'ioc_value': 'username'
            }
        ],
        'iris_alert_context': {'username': 'username', 'ip': 'src_ip', 'login_status': 'event_status'},
        'alert': [],
    }

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IrisAlerter(rule)

    match = {
        '@timestamp': '2023-10-21 20:00:00.000', 'username': 'evil_user', 'src_ip': '172.20.1.1', 'dst_ip': '10.0.0.1',
        'event_type': 'login', 'event_status': 'success'
    }

    expected_data = {
        "alert_title": 'Test Main',
        "alert_description": 'test description in alert',
        "alert_source": "ElastAlert2",
        "alert_severity_id": 1,
        "alert_status_id": 2,
        "alert_source_event_time": '2023-10-21 20:00:00.000',
        "alert_note": 'test note',
        "alert_tags": 'test, alert',
        "alert_customer_id": 1,
        "alert_source_link": 'https://example.com',
        "alert_iocs": [
            {
                'ioc_description': 'source address',
                'ioc_tags': 'ip, ipv4',
                'ioc_tlp_id': 1,
                'ioc_type_id': 76,
                'ioc_value': '172.20.1.1'
            },
            {
                'ioc_description': 'target username',
                'ioc_tags': 'login, username',
                'ioc_tlp_id': 3,
                'ioc_type_id': 3,
                'ioc_value': 'evil_user'
            }
        ],
        "alert_context": {
            'username': 'evil_user',
            'ip': '172.20.1.1',
            'login_status': 'success'
        },
    }
    mock_response = mock.Mock()
    mock_response.status_code = 200
    with mock.patch('requests.post', return_value=mock_response) as mock_post_request:
        alert.alert([match])

    mock_post_request.assert_called_once_with(
        url=f'https://{rule["iris_host"]}/alerts/add',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {rule["iris_api_token"]}'
        },
        json=mock.ANY,
        verify=True,
    )

    assert expected_data == mock_post_request.call_args_list[0][1]['json']
    assert ('elastalert', logging.INFO, 'Alert sent to Iris') == caplog.record_tuples[0]


def test_iris_alert_alert_with_custom_customer_id(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test Main',
        'type': 'any',
        'iris_host': '127.0.0.1',
        'iris_api_token': 'token 12345',
        'iris_customer_id': 2,
        'iris_description': 'test description in alert',
        'iris_alert_note': 'test note',
        'iris_alert_tags': 'test, alert',
        'iris_overwrite_timestamp': True,
        'iris_alert_source_link': 'https://example.com',
        'iris_iocs': [
            {
                'ioc_description': 'source address',
                'ioc_tags': 'ip, ipv4',
                'ioc_tlp_id': 1,
                'ioc_type_id': 76,
                'ioc_value': 'src_ip'
            },
            {
                'ioc_description': 'target username',
                'ioc_tags': 'login, username',
                'ioc_tlp_id': 3,
                'ioc_type_id': 3,
                'ioc_value': 'username'
            }
        ],
        'iris_alert_context': {'username': 'username', 'ip': 'src_ip', 'login_status': 'event_status'},
        'alert': [],
    }

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IrisAlerter(rule)

    match = {
        '@timestamp': '2023-10-21 20:00:00.000', 'username': 'evil_user', 'src_ip': '172.20.1.1', 'dst_ip': '10.0.0.1',
        'event_type': 'login', 'event_status': 'success'
    }

    expected_data = {
        "alert_title": 'Test Main',
        "alert_description": 'test description in alert',
        "alert_source": "ElastAlert2",
        "alert_severity_id": 1,
        "alert_status_id": 2,
        "alert_source_event_time": '2023-10-21 20:00:00.000',
        "alert_note": 'test note',
        "alert_tags": 'test, alert',
        "alert_customer_id": 2,
        "alert_source_link": 'https://example.com',
        "alert_iocs": [
            {
                'ioc_description': 'source address',
                'ioc_tags': 'ip, ipv4',
                'ioc_tlp_id': 1,
                'ioc_type_id': 76,
                'ioc_value': '172.20.1.1'
            },
            {
                'ioc_description': 'target username',
                'ioc_tags': 'login, username',
                'ioc_tlp_id': 3,
                'ioc_type_id': 3,
                'ioc_value': 'evil_user'
            }
        ],
        "alert_context": {
            'username': 'evil_user',
            'ip': '172.20.1.1',
            'login_status': 'success'
        },
    }
    mock_response = mock.Mock()
    mock_response.status_code = 200
    with mock.patch('requests.post', return_value=mock_response) as mock_post_request:
        alert.alert([match])

    mock_post_request.assert_called_once_with(
        url=f'https://{rule["iris_host"]}/alerts/add',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {rule["iris_api_token"]}'
        },
        json=mock.ANY,
        verify=True,
    )

    assert expected_data == mock_post_request.call_args_list[0][1]['json']
    assert ('elastalert', logging.INFO, 'Alert sent to Iris') == caplog.record_tuples[0]


def test_iris_get_info(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test Info',
        'type': 'any',
        'iris_host': '127.0.0.1',
        'iris_api_token': 'token 12345',
        'iris_customer_id': 1,
        'alert': [],
    }

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IrisAlerter(rule)

    expected_data = {
        'type': 'IrisAlerter',
        'iris_api_endpoint': 'https://127.0.0.1'
    }

    actual_data = alert.get_info()
    assert expected_data == actual_data
