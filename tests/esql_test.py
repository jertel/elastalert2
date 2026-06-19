import elastalert.esql as esql
from elastalert import ElasticSearchClient
from unittest import mock


def test_format_request_without_esql():
    assert esql.format_request({}) is None
    assert esql.format_request({'query': {}}) is None
    assert esql.format_request({'query': {'bool': {}}}) is None
    assert esql.format_request({'query': {'bool': {'filter': {}}}}) is None
    assert esql.format_request({'query': {'bool': {'filter': {'bool': {}}}}}) is None
    assert esql.format_request({'query': {'bool': {'filter': {'bool': {'must': []}}}}}) is None
    assert esql.format_request({'query': {'bool': {'filter': {'bool': {'must': [{'foo': 'bar'}]}}}}}) is None


def test_format_request_with_esql():
    body = esql_body()
    expected_body = {'filter': {'bool': {'must': [{'other': 'other filter'}]}}, 'query': 'FROM logs-* | WHERE status == 500'}
    assert esql.format_request(body) == expected_body


def esql_body():
    body = {
        'query': {
            'bool': {
                'filter': {
                    'bool': {
                        'must': [
                            {'esql': 'FROM logs-* | WHERE status == 500'},
                            {'other': 'other filter'},
                        ]
                    }
                }
            }
        }
    }
    return body


def test_format_request_with_excessive_esql():
    body = esql_body()
    body['query']['bool']['filter']['bool']['must'].append({'esql': 'FROM logs-* | WHERE status == 200'})
    expected_body = {'filter': {'bool': {'must': [{'other': 'other filter'}]}}, 'query': 'FROM logs-* | WHERE status == 200'}
    assert esql.format_request(body) == expected_body


def test_format_results_without_columns_values():
    expected_results = {'hits': {'hits': []}}
    results = expected_results
    assert esql.format_results(results) == expected_results


def test_format_results_with_columns_values():
    results = {
        'columns': [
            {'name': '@timestamp', 'type': 'date'},
            {'name': 'message', 'type': 'keyword'},
            {'name': '_id', 'type': 'keyword'},
            {'name': '_index', 'type': 'keyword'}
        ],
        'values': [
            ['2026-06-05T09:00:00Z', 'Hello', 'id-1', 'logs-1']
        ]
    }
    formatted = esql.format_results(results, default_index='test-default')
    assert formatted['esql'] is True
    assert len(formatted['hits']['hits']) == 1
    hit = formatted['hits']['hits'][0]
    assert hit['_id'] == 'id-1'
    assert hit['_index'] == 'logs-1'
    assert hit['_source']['message'] == 'Hello'


def test_format_results_fallback_id():
    results = {
        'columns': [
            {'name': '@timestamp', 'type': 'date'},
            {'name': 'message', 'type': 'keyword'}
        ],
        'values': [
            ['2026-06-05T09:00:00Z', 'Hello']
        ]
    }
    formatted = esql.format_results(results, default_index='test-default')
    assert formatted['esql'] is True
    assert len(formatted['hits']['hits']) == 1
    hit = formatted['hits']['hits'][0]
    assert hit['_id'] is not None
    assert len(hit['_id']) == 64  # sha256 hex
    assert hit['_index'] == 'test-default'
    assert hit['_source']['message'] == 'Hello'


def init_client():
    conn = {
        'es_host': '',
        'es_hosts': [],
        'es_port': 123,
        'es_url_prefix': '',
        'use_ssl': False,
        'verify_certs': False,
        'ca_certs': [],
        'ssl_show_warn': False,
        'http_auth': '',
        'headers': [],
        'es_conn_timeout': 0,
        'send_get_body_as': '',
        'client_cert': '',
        'client_key': ''
    }
    return ElasticSearchClient(conn)


def test_search_with_esql():
    es_client = init_client()

    expected_params = {'format': 'json'}
    expected_headers = {}
    expected_body = {'filter': {'bool': {'must': [{'other': 'other filter'}]}}, 'query': 'FROM logs-* | WHERE status == 500'}

    # Mock return value with ES|QL format
    results = {
        'columns': [{'name': 'message', 'type': 'keyword'}],
        'values': [['Test message']]
    }
    es_client.transport = mock.Mock()
    es_client.transport.perform_request.return_value = results

    body = esql_body()
    params = {'from_': True, 'size': 12, 'scroll': True, '_source_includes': True}
    res = es_client.search(body=body, index='test', params=params)

    es_client.transport.perform_request.assert_called_with('POST', '/_query',
                                                           params=expected_params,
                                                           headers=expected_headers,
                                                           body=expected_body)
    assert res['esql'] is True
    assert res['hits']['hits'][0]['_source']['message'] == 'Test message'


def test_process_hits_missing_timestamp():
    from elastalert.elastalert import ElastAlerter
    from elastalert.util import EAException
    import pytest

    rule = {
        'timestamp_field': '@timestamp',
        'ts_to_dt': lambda x: x,
        '_source_enabled': True
    }
    hits = [{'_source': {'message': 'Hello'}}]
    with pytest.raises(EAException) as excinfo:
        ElastAlerter.process_hits(rule, hits)
    assert "The configured timestamp_field '@timestamp' was not found" in str(excinfo.value)
