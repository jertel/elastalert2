import logging
from unittest import mock
import pytest
from elasticsearch.exceptions import TransportError
from elastalert.util import EAException
from elastalert.loaders import FileRulesLoader
from elastalert.alerters.opensearch import OpenSearchAlerter


def test_opensearch_alerter(caplog):

    caplog.set_level(logging.INFO)
    rule = {
        'alert': [],
        'name': 'test-alert',
        'index': 'my-index',
        'query': 'some query',
        'description': 'test',
        'opensearch_connection': {
            'es_host': 'localhost',
            'es_port': 9200,
            'index_alerts_name': 'test_index'
        },
        'opensearch_alert_config': {
            'get_index': 'index',
            'get_type': 'type',
            'get_field1': 'field1',
            'get_field2': 'field2',
            '@timestamp': '@timestamp'
        },
        'type': 'any'
    }

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = OpenSearchAlerter(rule)

    match = {
        'index': 'test-index',
        'type': 'test-type',
        'field1': 'value1',
        'field2': 'value2',
        '@timestamp': '2021-05-09T14:43:30'
    }

    with mock.patch('elasticsearch.Elasticsearch.index') as mock_create:
        alert.alert([match])

    expected_data = {
        'get_index': 'test-index',
        'get_type': 'test-type',
        'get_field1': 'value1',
        'get_field2': 'value2',
        '@timestamp': '2021-05-09T14:43:30'
    }

    mock_create.assert_called_once_with(
        index='test_index', body=mock.ANY, refresh=True
    )
    actual_data = mock_create.call_args_list[0][1]['body']
    assert expected_data == actual_data
    assert ('elastalert', logging.INFO, 'Alert sent to Opensearch') == caplog.record_tuples[0]


def test_alert_with_transport_error():

    with pytest.raises(EAException) as ea:
        rule = {
            'alert': [],
            'name': 'test-alert',
            'index': 'my-index',
            'query': 'some query',
            'description': 'test',
            'opensearch_connection': {
                'es_host': 'localhost',
                'es_port': 9200,
                'index_alerts_name': 'test_index'
            },
            'opensearch_alert_config': {
                'get_index': 'index',
                'get_type': 'type',
                'get_field1': 'field1',
                'get_field2': 'field2',
                '@timestamp': '@timestamp'
            },
            'type': 'any'
        }
        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = OpenSearchAlerter(rule)
        match = {
            '@timestamp': '2021-01-01T00:00:00',
            'somefield': 'foobarbaz'
        }

        mock_run = mock.MagicMock(side_effect=TransportError(500, "Error creating index"))
        # Mocking the Elasticsearch create method to raise TransportError
        with mock.patch('elasticsearch.Elasticsearch.index', mock_run), pytest.raises(TransportError):
            alert.alert([match])

    assert "Error posting to Opensearch" in str(ea)
