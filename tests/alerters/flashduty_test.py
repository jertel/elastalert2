import json
import logging
from unittest import mock

import pytest
from requests import RequestException

from elastalert.alerters.flashduty import FlashdutyAlerter
from elastalert.loaders import FileRulesLoader
from elastalert.util import EAException


def test_flashduty_alert(caplog):
    caplog.set_level(logging.INFO)
    rule = {
        'name': 'Test Flashduty Rule',
        'type': 'any',
        'flashduty_integration_key': 'xxx',
        'flashduty_title': 'Test Alert',
        'flashduty_description': 'Test Description',
        'flashduty_event_status': 'Info',
        'flashduty_alert_key': 'test-alert',
        'flashduty_check': 'test-check',
        'flashduty_service': 'test-service',
        'flashduty_cluster': 'test-cluster',
        'flashduty_resource': 'test-resource',
        'flashduty_metric': 'test-metric',
        'flashduty_group': 'test-group',
        'flashduty_env': 'test-env',
        'flashduty_app': 'test-app',
        'alert': [],
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = FlashdutyAlerter(rule)
    match = {
        '@timestamp': '2025-03-20T00:00:00',
        'somefield': 'foobar'
    }

    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'title': 'Test Alert',
        'description': 'Test Description',
        'event_status': 'Info',
        'alert_key': 'test-alert',
        'labels': {
            'check': 'test-check',
            'service': 'test-service',
            'cluster': 'test-cluster',
            'resource': 'test-resource',
            'metric': 'test-metric',
            'group': 'test-group',
            'env': 'test-env',
            'app': 'test-app',
            'information': 'Test Flashduty Rule\n\n@timestamp: 2025-03-20T00:00:00\nsomefield: foobar\n'
        }
    }

    mock_post_request.assert_called_once_with(
        'https://api.flashcat.cloud/event/push/alert/standard?integration_key=' + rule['flashduty_integration_key'],
        data=mock.ANY,
        headers={'Content-Type': 'application/json'}
    )

    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data
    assert ('elastalert', logging.INFO, 'Trigger sent to flashduty') == caplog.record_tuples[0]


def test_flashduty_ea_exception():
    rule = {
        'name': 'Test Flashduty Rule',
        'type': 'any',
        'flashduty_integration_key': 'xxx',
        'alert': [],
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = FlashdutyAlerter(rule)
    match = {
        '@timestamp': '2025-03-20T00:00:00',
        'somefield': 'foobar'
    }
    mock_run = mock.MagicMock(side_effect=RequestException)
    with mock.patch('requests.post', mock_run):
        with pytest.raises(EAException) as ea:
            alert.alert([match])
    assert 'Error posting to flashduty: ' in str(ea)


def test_flashduty_getinfo():
    rule = {
        'name': 'Test Flashduty Rule',
        'type': 'any',
        'flashduty_integration_key': 'xxx',
        'flashduty_title': 'Test Alert',
        'flashduty_description': 'Test Description',
        'flashduty_event_status': 'Info',
        'flashduty_alert_key': 'test-alert',
        'flashduty_check': 'test-check',
        'flashduty_service': 'test-service',
        'flashduty_cluster': 'test-cluster',
        'flashduty_resource': 'test-resource',
        'flashduty_metric': 'test-metric',
        'flashduty_group': 'test-group',
        'flashduty_env': 'test-env',
        'flashduty_app': 'test-app',
        'alert': [],
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = FlashdutyAlerter(rule)

    expected_data = {
        'type': 'flashduty',
        'flashduty_integration_key': 'xxx',
        'flashduty_title': 'Test Alert',
        'flashduty_description': 'Test Description',
        'flashduty_event_status': 'Info',
        'flashduty_alert_key': 'test-alert',
        'flashduty_check': 'test-check',
        'flashduty_service': 'test-service',
        'flashduty_cluster': 'test-cluster',
        'flashduty_resource': 'test-resource',
        'flashduty_metric': 'test-metric',
        'flashduty_group': 'test-group',
        'flashduty_env': 'test-env',
        'flashduty_app': 'test-app'
    }
    actual_data = alert.get_info()
    assert expected_data == actual_data


def test_flashduty_required_error():
    try:
        rule = {
            'name': 'Test Flashduty Rule',
            'type': 'any',
            'alert': [],
        }
        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        FlashdutyAlerter(rule)
    except Exception as ea:
        assert 'Missing required option(s): flashduty_integration_key' in str(ea)
