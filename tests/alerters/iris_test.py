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
        "alert_description": None,
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
