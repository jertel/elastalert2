import logging
from unittest import mock
import pytest
from elasticsearch.exceptions import TransportError
from elastalert.util import EAException
from elastalert.loaders import FileRulesLoader
from elastalert.alerters.indexer import IndexerAlerter


def rule_config():
    return {
        'alert': [],
        'name': 'test-alert',
        'index': 'my-index',
        'filter': [{'key': {'query': {'query': 'test_query'}}}],
        'description': 'test',
        'indexer_connection': {
            'es_host': 'localhost',
            'es_port': 9200,
            'indexer_alerts_name': 'test_index'
        },
        'indexer_alert_config': {
            'get_index': 'index',
            'get_type': 'type',
            'get_field1': 'field1',
            'get_field2': 'field2',
            '@timestamp': '@timestamp'
        },
        'type': 'any'
    }


def test_indexer_alerter(caplog):

    caplog.set_level(logging.INFO)
    rule = rule_config()

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IndexerAlerter(rule)

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
    assert ('elastalert', logging.INFO, 'Alert sent to SIEM') == caplog.record_tuples[0]


def test_alert_with_file_config():

    rule = rule_config()
    rule.pop('indexer_connection')
    rule['indexer_config'] = 'config.yaml'

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IndexerAlerter(rule)

    match = {
        'index': 'test-index',
        'type': 'test-type',
        'field1': 'value1',
        'field2': 'value2',
        '@timestamp': '2021-05-09T14:43:30'
    }

    with mock.patch('elasticsearch.Elasticsearch.index') as mock_create, \
            mock.patch('os.path.isfile', return_value=True), \
            mock.patch('builtins.open', new_callable=mock.mock_open,
                       read_data='indexer_connection:\n  es_host: localhost\n  es_port: 9200\n  indexer_alerts_name: test_index'), \
            mock.patch('yaml.load', return_value={'es_host': 'localhost', 'es_port': 9200, 'indexer_alerts_name': 'test_index'}):
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


def test_alert_with_transport_error():

    with pytest.raises(EAException) as ea:
        rule = rule_config()
        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = IndexerAlerter(rule)
        match = {
            '@timestamp': '2021-01-01T00:00:00',
            'somefield': 'foobarbaz'
        }

        mock_run = mock.MagicMock(side_effect=TransportError(500, "Error creating index"))
        # Mocking the Elasticsearch create method to raise TransportError
        with mock.patch('elasticsearch.Elasticsearch.index', mock_run), pytest.raises(TransportError):
            alert.alert([match])

    assert "Error posting to SIEM" in str(ea)


def test_get_query():

    body_request_raw = [{'key': {'query': {'query': 'test_query'}}}]
    rule = rule_config()

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IndexerAlerter(rule)
    expected_data = {
        'get_query': 'test_query'
    }

    actual_data = {'get_query': alert.get_query(body_request_raw)}
    assert expected_data == actual_data


def test_lookup_field():

    rule = rule_config()

    match = {'field1': 'some important'}
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IndexerAlerter(rule)
    expected_data1 = {
        'get_field1': 'some important',
    }
    expected_data2 = {
        'get_field1': 'field2'
    }

    actual_data = {'get_field1': alert.lookup_field(match, expected_data1['get_field1'], expected_data1['get_field1'])}
    assert expected_data1 == actual_data
    actual_data = {'get_field1': alert.lookup_field(match, expected_data2['get_field1'], expected_data2['get_field1'])}
    assert expected_data2 == actual_data


def test_lookup_list_fields():

    rule = rule_config()
    match = {'field1': 'value1'}
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IndexerAlerter(rule)

    # Test simple case with direct value lookup
    original_fields_raw = [{'name': 'field1', 'value': 'field1'}]
    expected_data = {'field1': 'value1'}
    actual_data = alert.lookup_list_fields(original_fields_raw, match)
    assert expected_data == actual_data

    # Test simple case with direct value lookup not str
    original_fields_raw = [{'name': 'field1', 'value': 123}]
    expected_data = {'field1': 123}
    actual_data = alert.lookup_list_fields(original_fields_raw, match)
    assert expected_data == actual_data

    # Test with 'filter' keyword
    original_fields_raw = [{'name': 'query', 'value': 'filter'}]
    expected_data = {'query': 'test_query'}
    actual_data = alert.lookup_list_fields(original_fields_raw, match)
    assert actual_data == expected_data

    original_fields_raw = [{'name': 'query', 'value': 'filter'}]
    expected_data = {'query': 'test_query'}
    actual_data = alert.lookup_list_fields(original_fields_raw, match)
    assert actual_data == expected_data

    original_fields_raw = [{'test_event_data': [{'name': 'test', 'value': 'test_event'}]}]
    expected_data = {'test_event_data': {'test': 'test_event'}}
    actual_data = alert.lookup_list_fields(original_fields_raw, match)
    assert actual_data == expected_data


def test_event_orig_fields():

    rule = rule_config()
    match = {'field1': 'value1'}
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IndexerAlerter(rule)

    # test if (isinstance(original_fields_raw, str))
    expected_data = {'field1': 'value1'}
    actual_data = {'field1': alert.event_orig_fields('field1', match)}
    assert expected_data == actual_data

    # test elif (isinstance(original_fields_raw, list))
    list_data = [{'name': 'field1', 'value': 'value1'}]
    expected_data = {'field1': 'value1'}
    actual_data = alert.event_orig_fields(list_data, match)
    assert expected_data == actual_data

    # test else not str or list
    expected_data = {'test_data': 10}
    actual_data = alert.event_orig_fields(expected_data, match)
    assert expected_data == actual_data


def test_make_nested_fields():

    rule = rule_config()
    data = {
        'a.b.c': 1, 'a.b.d': 2, 'e': 3
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IndexerAlerter(rule)
    expected_data = {'a': {'b': {'c': 1, 'd': 2}}, 'e': 3}
    actual_data = alert.make_nested_fields(data)
    assert expected_data == actual_data


def test_flatten_dict():

    rule = rule_config()
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IndexerAlerter(rule)
    data = {'a': {'b': {'c': 1, 'd': 2}}, 'e': 3}
    expected_data = {'a.b.c': 1, 'a.b.d': 2, 'e': 3}
    actual_data = alert.flatten_dict(data)
    assert expected_data == actual_data


def test_remove_matching_pairs():

    rule = rule_config()
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IndexerAlerter(rule)
    data = {'a': 'a', 'b': 'c'}
    expected_data = {'b': 'c'}
    actual_data = alert.remove_matching_pairs(data)
    assert actual_data == expected_data


def test_indexer_getinfo():

    rule = rule_config()

    alert = IndexerAlerter(rule)
    expected_data = {
        'type': 'indexer'
    }
    actual_data = alert.get_info()
    assert expected_data == actual_data


def test_alert_with_matches():

    rule = rule_config()
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IndexerAlerter(rule)

    match = {'field1': 'value1'}
    alert_config = {
        '@timestamp': '2021-01-01T00:00:00',
        'key1': 'value1',
        'key2': 'value2'
    }

    with mock.patch('elasticsearch.Elasticsearch.index') as mock_create, \
            mock.patch.object(alert, 'flatten_dict', return_value=alert_config) as mock_flatten, \
            mock.patch.object(alert, 'event_orig_fields', side_effect=lambda x, y: f"processed_{y}") as mock_event_orig_fields, \
            mock.patch.object(alert, 'remove_matching_pairs', return_value=alert_config) as mock_remove_matching_pairs, \
            mock.patch.object(alert, 'make_nested_fields', return_value=alert_config) as mock_make_nested_fields:

        alert.alert([match])

        mock_flatten.assert_called()
        mock_event_orig_fields.assert_called()
        mock_remove_matching_pairs.assert_called()
        mock_make_nested_fields.assert_called()

        # Ensure that flatten_dict was called twice
        expected_data = 2
        actual_data = mock_flatten.call_count
        assert actual_data == expected_data

        # Check if event_orig_fields was called for each key in alert_config
        expected_data = len(alert_config)
        actual_data = mock_event_orig_fields.call_count
        assert actual_data == expected_data

        # Verify if the transformed alert_config is passed to remove_matching_pairs and make_nested_fields
        mock_remove_matching_pairs.assert_called_with(alert_config)
        mock_make_nested_fields.assert_called_with(alert_config)

        mock_create.assert_called_once_with(
            index='test_index', body=alert_config, refresh=True
        )


def test_alert_with_empty_matches():

    rule = rule_config()
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = IndexerAlerter(rule)
    match = []
    alert_config = {
        '@timestamp': '2021-01-01T00:00:00',
        'key1': 'value1',
        'key2': 'value2'
    }
    with mock.patch('elasticsearch.Elasticsearch.index') as mock_create, \
            mock.patch.object(alert, 'flatten_dict', return_value=alert_config) as mock_flatten, \
            mock.patch.object(alert, 'remove_matching_pairs', return_value=alert_config) as mock_remove_matching_pairs, \
            mock.patch.object(alert, 'make_nested_fields', return_value=alert_config) as mock_make_nested_fields, \
            mock.patch.object(alert, 'event_orig_fields') as mock_event_orig_fields:
        alert.alert(match)

        mock_flatten.assert_called()
        mock_remove_matching_pairs.assert_called()
        mock_make_nested_fields.assert_called()
        mock_event_orig_fields.assert_not_called()
        # Ensure that flatten_dict was called twice
        expected_data = 1
        actual_data = mock_flatten.call_count
        assert actual_data == expected_data

        expected_data = 0
        actual_data = mock_event_orig_fields.call_count
        assert expected_data == actual_data
        # Verify if the transformed alert_config is passed to remove_matching_pairs and make_nested_fields
        mock_remove_matching_pairs.assert_called_with(alert_config)
        mock_make_nested_fields.assert_called_with(alert_config)

        mock_create.assert_called_once_with(
            index='test_index', body=alert_config, refresh=True
        )
