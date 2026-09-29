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


def test_format_source_uses_metadata_source():
    col_names = ['_id', '_index', '_source']
    val_row = ['id-1', 'logs-1', {'process': {'name': 'cmd.exe'}, 'host': {'name': 'ws1'}}]
    assert esql.format_source(col_names, val_row) == {
        'process': {'name': 'cmd.exe'},
        'host': {'name': 'ws1'},
        '_id': 'id-1',
        '_index': 'logs-1'
    }


def test_format_source_falls_back_when_metadata_source_null():
    col_names = ['_source', 'message']
    val_row = [None, 'Hello']
    assert esql.format_source(col_names, val_row) == {'message': 'Hello'}


def test_format_source_nests_dotted_columns():
    col_names = ['process.name', 'process.pid', 'host.name']
    val_row = ['cmd.exe', 42, 'ws1']
    assert esql.format_source(col_names, val_row) == {
        'process': {'name': 'cmd.exe', 'pid': 42},
        'host': {'name': 'ws1'}
    }


def test_format_source_drops_null_columns():
    col_names = ['process.name', 'process.pid', 'host.name']
    val_row = ['cmd.exe', None, None]
    assert esql.format_source(col_names, val_row) == {'process': {'name': 'cmd.exe'}}


def test_format_source_multi_field_does_not_displace_scalar_parent():
    col_names = ['process.command_line.caseless', 'process.command_line']
    val_row = ['whoami', 'WHOAMI']
    assert esql.format_source(col_names, val_row) == {'process': {'command_line': 'WHOAMI'}}


def test_format_source_multi_field_with_null_parent():
    # ignore_above spares .text but not the parent or .caseless.
    col_names = ['process.command_line', 'process.command_line.caseless',
                 'process.command_line.text']
    val_row = [None, None, 'x' * 2000]
    assert esql.format_source(col_names, val_row) == {}


def test_format_source_keeps_nested_field_that_is_not_a_multi_field():
    # process.io is an object, not a scalar, so process.io.text is a real field.
    col_names = ['process.io.text', 'process.name']
    val_row = ['captured output', 'cmd.exe']
    assert esql.format_source(col_names, val_row) == {
        'process': {'io': {'text': 'captured output'}, 'name': 'cmd.exe'}
    }


def test_format_source_realistic_row():
    col_names = [
        '@timestamp', 'host.name', 'process.name', 'process.name.caseless',
        'process.pid', 'user.name', 'event.code',
        'process.command_line', 'process.command_line.caseless'
    ]
    val_row = [
        '2026-06-05T09:00:00Z', 'ws1', 'cmd.exe', 'cmd.exe',
        None, None, '4688',
        'WHOAMI /priv', 'whoami /priv'
    ]
    assert esql.format_source(col_names, val_row) == {
        '@timestamp': '2026-06-05T09:00:00Z',
        'host': {'name': 'ws1'},
        'process': {'name': 'cmd.exe', 'command_line': 'WHOAMI /priv'},
        'event': {'code': '4688'}
    }


def test_format_results_uses_metadata_source():
    results = {
        'columns': [
            {'name': '_id', 'type': 'keyword'},
            {'name': '_index', 'type': 'keyword'},
            {'name': '_source', 'type': '_source'}
        ],
        'values': [
            ['id-1', 'logs-1', {'process': {'name': 'cmd.exe'}}]
        ]
    }
    hit = esql.format_results(results)['hits']['hits'][0]
    assert hit['_id'] == 'id-1'
    assert hit['_index'] == 'logs-1'
    assert hit['_source']['process']['name'] == 'cmd.exe'


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
    expected_body = {'filter': {'bool': {'must': [{'other': 'other filter'}]}}, 'query': 'FROM logs-* | WHERE status == 500\n| limit 12'}

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


def test_apply_limit_appends_a_limit():
    assert esql.apply_limit('FROM logs-* | WHERE a == 1', 5000) == 'FROM logs-* | WHERE a == 1\n| limit 5000'


def test_apply_limit_leaves_an_existing_limit_alone():
    query = 'FROM logs-* | WHERE a == 1 | LIMIT 10'
    assert esql.apply_limit(query, 5000) == query

    query = 'FROM logs-* | WHERE a == 1\n| limit 10\n'
    assert esql.apply_limit(query, 5000) == query


def test_apply_limit_without_a_size():
    query = 'FROM logs-* | WHERE a == 1'
    assert esql.apply_limit(query, None) == query
    assert esql.apply_limit(query, 0) == query


def test_apply_limit_only_matches_a_trailing_limit():
    # Only a trailing LIMIT bounds the result.
    query = 'FROM logs-* | LIMIT 10 | STATS c = count() BY host'
    assert esql.apply_limit(query, 5000) == query + '\n| limit 5000'


def test_format_request_applies_the_size():
    body = esql_body()
    formatted = esql.format_request(body, size=5000)
    assert formatted['query'] == 'FROM logs-* | WHERE status == 500\n| limit 5000'


def test_format_request_without_a_size_is_unchanged():
    body = esql_body()
    formatted = esql.format_request(body)
    assert formatted['query'] == 'FROM logs-* | WHERE status == 500'


def test_truncation_warning_when_at_the_limit():
    msg = esql.truncation_warning({'documents_found': 105498}, 1000, 1000)
    assert msg is not None
    assert '1000 row limit' in msg
    assert 'at least 105498 documents matched' in msg


def test_truncation_warning_below_the_limit():
    assert esql.truncation_warning({}, 999, 1000) is None


def test_truncation_warning_without_a_limit():
    assert esql.truncation_warning({}, 5000, None) is None
    assert esql.truncation_warning({}, 5000, 0) is None


def test_truncation_warning_omits_the_scanned_note_when_unhelpful():
    msg = esql.truncation_warning({'documents_found': 1000}, 1000, 1000)
    assert msg is not None
    assert 'documents matched' not in msg

    msg = esql.truncation_warning({}, 1000, 1000)
    assert msg is not None
    assert 'documents matched' not in msg
