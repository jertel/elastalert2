import datetime
import json
import logging
import pytest

from unittest import mock

from requests import RequestException
from requests.auth import HTTPBasicAuth

from elastalert.alerters.alertmanager import AlertmanagerAlerter
from elastalert.loaders import FileRulesLoader
from elastalert.util import EAException


def test_alertmanager(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test Alertmanager Rule',
        'type': 'any',
        'alertmanager_hosts': ['http://alertmanager:9093'],
        'alertmanager_alertname': 'Title',
        'alertmanager_annotations': {'severity': 'error'},
        'alertmanager_labels': {'source': 'elastalert'},
        'alertmanager_fields': {'msg': 'message', 'log': '@log_name'},
        'alert_subject_args': ['message', '@log_name'],
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = AlertmanagerAlerter(rule)
    match = {
        '@timestamp': '2021-01-01T00:00:00',
        'somefield': 'foobarbaz',
        'message': 'Quit 123',
        '@log_name': 'mysqld.general'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = [
        {
            'annotations':
            {
                'severity': 'error',
                'summary': 'Test Alertmanager Rule',
                'description': 'Test Alertmanager Rule\n\n' +
                '@log_name: mysqld.general\n' +
                '@timestamp: 2021-01-01T00:00:00\n' +
                'message: Quit 123\nsomefield: foobarbaz\n'
            },
            'labels': {
                'source': 'elastalert',
                'msg': 'Quit 123',
                'log': 'mysqld.general',
                'alertname': 'Title',
                'elastalert_rule': 'Test Alertmanager Rule'
            }
        }
    ]

    mock_post_request.assert_called_once_with(
        'http://alertmanager:9093/api/v1/alerts',
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10,
        auth=None
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert ('elastalert', logging.INFO, "Alert sent to Alertmanager") == caplog.record_tuples[0]


def test_alertmanager_porxy():
    rule = {
        'name': 'Test Alertmanager Rule',
        'type': 'any',
        'alertmanager_hosts': ['http://alertmanager:9093'],
        'alertmanager_alertname': 'Title',
        'alertmanager_annotations': {'severity': 'error'},
        'alertmanager_labels': {'source': 'elastalert'},
        'alertmanager_fields': {'msg': 'message', 'log': '@log_name'},
        'alertmanager_proxy': 'http://proxy.url',
        'alert_subject_args': ['message', '@log_name'],
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = AlertmanagerAlerter(rule)
    match = {
        '@timestamp': '2021-01-01T00:00:00',
        'somefield': 'foobarbaz',
        'message': 'Quit 123',
        '@log_name': 'mysqld.general'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = [
        {
            'annotations':
            {
                'severity': 'error',
                'summary': 'Test Alertmanager Rule',
                'description': 'Test Alertmanager Rule\n\n' +
                '@log_name: mysqld.general\n' +
                '@timestamp: 2021-01-01T00:00:00\n' +
                'message: Quit 123\nsomefield: foobarbaz\n'
            },
            'labels': {
                'source': 'elastalert',
                'msg': 'Quit 123',
                'log': 'mysqld.general',
                'alertname': 'Title',
                'elastalert_rule': 'Test Alertmanager Rule'
            }
        }
    ]

    mock_post_request.assert_called_once_with(
        'http://alertmanager:9093/api/v1/alerts',
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies={'https': 'http://proxy.url'},
        verify=True,
        timeout=10,
        auth=None
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_alertmanager_timeout():
    rule = {
        'name': 'Test Alertmanager Rule',
        'type': 'any',
        'alertmanager_hosts': ['http://alertmanager:9093'],
        'alertmanager_alertname': 'Title',
        'alertmanager_annotations': {'severity': 'error'},
        'alertmanager_labels': {'source': 'elastalert'},
        'alertmanager_fields': {'msg': 'message', 'log': '@log_name'},
        'alertmanager_timeout': 20,
        'alert_subject_args': ['message', '@log_name'],
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = AlertmanagerAlerter(rule)
    match = {
        '@timestamp': '2021-01-01T00:00:00',
        'somefield': 'foobarbaz',
        'message': 'Quit 123',
        '@log_name': 'mysqld.general'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = [
        {
            'annotations':
            {
                'severity': 'error',
                'summary': 'Test Alertmanager Rule',
                'description': 'Test Alertmanager Rule\n\n' +
                '@log_name: mysqld.general\n' +
                '@timestamp: 2021-01-01T00:00:00\n' +
                'message: Quit 123\nsomefield: foobarbaz\n'
            },
            'labels': {
                'source': 'elastalert',
                'msg': 'Quit 123',
                'log': 'mysqld.general',
                'alertname': 'Title',
                'elastalert_rule': 'Test Alertmanager Rule'
            }
        }
    ]

    mock_post_request.assert_called_once_with(
        'http://alertmanager:9093/api/v1/alerts',
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=20,
        auth=None
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


@pytest.mark.parametrize('ca_certs, ignore_ssl_errors, expect_verify', [
    ('',   '',     True),
    ('',   True,   False),
    ('',   False,  True),
    (True, '',     True),
    (True, True,   True),
    (True, False,  True),
    (False, '',    True),
    (False, True,  False),
    (False, False, True)
])
def test_alertmanager_ca_certs(ca_certs, ignore_ssl_errors, expect_verify):
    rule = {
        'name': 'Test Alertmanager Rule',
        'type': 'any',
        'alertmanager_hosts': ['http://alertmanager:9093'],
        'alertmanager_alertname': 'Title',
        'alertmanager_annotations': {'severity': 'error'},
        'alertmanager_labels': {'source': 'elastalert'},
        'alertmanager_fields': {'msg': 'message', 'log': '@log_name'},
        'alert_subject_args': ['message', '@log_name'],
        'alert': []
    }
    if ca_certs:
        rule['alertmanager_ca_certs'] = ca_certs

    if ignore_ssl_errors:
        rule['alertmanager_ignore_ssl_errors'] = ignore_ssl_errors

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = AlertmanagerAlerter(rule)
    match = {
        '@timestamp': '2021-01-01T00:00:00',
        'somefield': 'foobarbaz',
        'message': 'Quit 123',
        '@log_name': 'mysqld.general'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = [
        {
            'annotations':
            {
                'severity': 'error',
                'summary': 'Test Alertmanager Rule',
                'description': 'Test Alertmanager Rule\n\n' +
                '@log_name: mysqld.general\n' +
                '@timestamp: 2021-01-01T00:00:00\n' +
                'message: Quit 123\nsomefield: foobarbaz\n'
            },
            'labels': {
                'source': 'elastalert',
                'msg': 'Quit 123',
                'log': 'mysqld.general',
                'alertname': 'Title',
                'elastalert_rule': 'Test Alertmanager Rule'
            }
        }
    ]

    mock_post_request.assert_called_once_with(
        'http://alertmanager:9093/api/v1/alerts',
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=expect_verify,
        timeout=10,
        auth=None
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_alertmanager_ea_exception():
    with pytest.raises(EAException) as ea:
        rule = {
            'name': 'Test Alertmanager Rule',
            'type': 'any',
            'alertmanager_hosts': ['http://alertmanager:9093'],
            'alert': []
        }
        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = AlertmanagerAlerter(rule)
        match = {
            '@timestamp': '2021-01-01T00:00:00',
            'somefield': 'foobarbaz'
        }
        mock_run = mock.MagicMock(side_effect=RequestException)
        with mock.patch('requests.post', mock_run), pytest.raises(RequestException):
            alert.alert([match])
    assert 'Error posting to Alertmanager' in str(ea)


def test_alertmanager_getinfo():
    rule = {
        'name': 'Test Alertmanager Rule',
        'type': 'any',
        'alertmanager_hosts': 'http://alertmanager:9093',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = AlertmanagerAlerter(rule)

    expected_data = {
        'type': 'alertmanager'
    }
    actual_data = alert.get_info()
    assert expected_data == actual_data


@pytest.mark.parametrize('alertmanager_hosts, expected_data', [
    ([],      'Missing required option(s): alertmanager_hosts'),
    (['http://alertmanager:9093'],
        {
            'type': 'alertmanager'
        }),
])
def test_alertmanager_required_error(alertmanager_hosts, expected_data):
    try:
        rule = {
            'name': 'Test Alertmanager Rule',
            'type': 'any',
            'alert': []
        }

        if alertmanager_hosts:
            rule['alertmanager_hosts'] = alertmanager_hosts

        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = AlertmanagerAlerter(rule)

        actual_data = alert.get_info()
        assert expected_data == actual_data
    except Exception as ea:
        print('ea %s' % str(ea))
        assert expected_data in str(ea)


def test_alertmanager_basic_auth():
    rule = {
        'name': 'Test Alertmanager Rule',
        'type': 'any',
        'alertmanager_hosts': ['http://alertmanager:9093'],
        'alertmanager_alertname': 'Title',
        'alertmanager_annotations': {'severity': 'error'},
        'alertmanager_labels': {'source': 'elastalert'},
        'alertmanager_fields': {'msg': 'message', 'log': '@log_name'},
        'alertmanager_basic_auth_login': 'user',
        'alertmanager_basic_auth_password': 'password',
        'alert_subject_args': ['message', '@log_name'],
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = AlertmanagerAlerter(rule)
    match = {
        '@timestamp': '2021-01-01T00:00:00',
        'somefield': 'foobarbaz',
        'message': 'Quit 123',
        '@log_name': 'mysqld.general'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = [
        {
            'annotations':
            {
                'severity': 'error',
                'summary': 'Test Alertmanager Rule',
                'description': 'Test Alertmanager Rule\n\n' +
                '@log_name: mysqld.general\n' +
                '@timestamp: 2021-01-01T00:00:00\n' +
                'message: Quit 123\nsomefield: foobarbaz\n'
            },
            'labels': {
                'source': 'elastalert',
                'msg': 'Quit 123',
                'log': 'mysqld.general',
                'alertname': 'Title',
                'elastalert_rule': 'Test Alertmanager Rule'
            }
        }
    ]

    mock_post_request.assert_called_once_with(
        'http://alertmanager:9093/api/v1/alerts',
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10,
        auth=HTTPBasicAuth('user', 'password')
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_alertmanager_resolve_timeout(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test Alertmanager Rule',
        'type': 'any',
        'alertmanager_hosts': ['http://alertmanager:9093'],
        'alertmanager_alertname': 'Title',
        'alertmanager_annotations': {'severity': 'error'},
        'alertmanager_resolve_time': {'minutes': 10},
        'alertmanager_labels': {'source': 'elastalert'},
        'alertmanager_fields': {'msg': 'message', 'log': '@log_name'},
        'alert_subject_args': ['message', '@log_name'],
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)

    alert = AlertmanagerAlerter(rule)
    match = {
        '@timestamp': '2021-01-01T00:00:00',
        'somefield': 'foobarbaz',
        'message': 'Quit 123',
        '@log_name': 'mysqld.general'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.now = mock.Mock(return_value=datetime.datetime(2023, 7, 14, tzinfo=datetime.timezone.utc))
        alert.alert([match])

    expected_data = [
        {
            'annotations':
            {
                'severity': 'error',
                'summary': 'Test Alertmanager Rule',
                'description': 'Test Alertmanager Rule\n\n' +
                '@log_name: mysqld.general\n' +
                '@timestamp: 2021-01-01T00:00:00\n' +
                'message: Quit 123\nsomefield: foobarbaz\n'
            },
            'endsAt': '2023-07-14T00:10:00+00:00',
            'labels': {
                'source': 'elastalert',
                'msg': 'Quit 123',
                'log': 'mysqld.general',
                'alertname': 'Title',
                'elastalert_rule': 'Test Alertmanager Rule'
            }
        }
    ]

    mock_post_request.assert_called_once_with(
        'http://alertmanager:9093/api/v1/alerts',
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10,
        auth=None
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert ('elastalert', logging.INFO, "Alert sent to Alertmanager") == caplog.record_tuples[0]


def test_alertmanager_labels_and_annotations_with_jinja2():
    rule = {
        'name': 'Test Alertmanager Rule',
        'type': 'any',
        'jinja_root_name': '_something',
        'alertmanager_hosts': ['http://alertmanager:9093'],
        'alertmanager_alertname': 'Title',
        'alertmanager_annotations': {
            'severity': 'error',
            'some_custom_annotation': '{{ _something["host"] }}:{{ service.name }}'
        },
        'alertmanager_labels': {
            'source': 'elastalert',
            'service_name': '{{ service.name }}',
            'environment': '{{ env.name }}',
            'region': '{{ env.region }}',
            'host': '{{ _something["host"] }}',
        },
        'alertmanager_fields': {'msg': 'message', 'log': '@log_name'},
        'alert_subject_args': ['message', '@log_name'],
        'alert': []
    }

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = AlertmanagerAlerter(rule)

    match = {
        'service': {'name': 'my-service'},
        'env': {'name': 'production', 'region': 'us-east-1'},
        'host': 'server01.example.com',
        'message': 'some message',
        '@log_name': 'some.log.name'
    }

    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    payload = json.loads(mock_post_request.call_args[1]['data'])[0]

    assert payload['labels']['source'] == 'elastalert'
    assert payload['labels']['service_name'] == 'my-service'
    assert payload['labels']['environment'] == 'production'
    assert payload['labels']['region'] == 'us-east-1'
    assert payload['labels']['host'] == 'server01.example.com'
    assert payload['labels']['log'] == 'some.log.name'
    assert payload['labels']['msg'] == 'some message'
    assert payload['annotations']['severity'] == 'error'
    assert payload['annotations']['some_custom_annotation'] == 'server01.example.com:my-service'


def test_alertmanager_labels_with_invalid_jinja2_syntax():
    rule = {
        'name': 'Test Alertmanager Rule',
        'type': 'any',
        'jinja_root_name': '_something',
        'alertmanager_hosts': ['http://alertmanager:9093'],
        'alertmanager_alertname': 'Title',
        'alertmanager_annotations': {'severity': 'error'},
        'alertmanager_labels': {
            'source': 'elastalert',
            'environment': 'some_name: {{ env.name ',
        },
        'alertmanager_fields': {'msg': 'message', 'log': '@log_name'},
        'alert_subject_args': ['message', '@log_name'],
        'alert': []
    }

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = AlertmanagerAlerter(rule)

    match = {
        'env': {'name': 'production', 'region': 'us-east-1'},
        'host': 'server01.example.com',
        'message': 'some message',
        '@log_name': 'some.log.name'
    }

    with pytest.raises(ValueError) as error:
        alert.alert([match])

    assert "Alertmanager: The template provided by key 'environment' has an invalid Jinja2 syntax." in str(error)
