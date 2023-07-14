import elastalert.eql as eql
from elastalert import ElasticSearchClient
from unittest import mock


def test_format_request_without_eql():
    assert eql.format_request({}) is None
    assert eql.format_request({'query': {}}) is None
    assert eql.format_request({'query': {'bool': {}}}) is None
    assert eql.format_request({'query': {'bool': {'filter': {}}}}) is None
    assert eql.format_request({'query': {'bool': {'filter': {'bool': {}}}}}) is None
    assert eql.format_request({'query': {'bool': {'filter': {'bool': {'must': []}}}}}) is None
    assert eql.format_request({'query': {'bool': {'filter': {'bool': {'must': [{'foo': 'bar'}]}}}}}) is None


def test_format_request_with_eql():
    body = eql_body()
    expected_body = {'filter': {'bool': {'must': [{'other': 'other filter'}]}}, 'query': 'test query'}
    assert eql.format_request(body) == expected_body


def eql_body():
    body = {
        'query': {
            'bool': {
                'filter': {
                    'bool': {
                        'must': [
                            {'eql': 'test query'},
                            {'other': 'other filter'},
                        ]
                    }
                }
            }
        }
    }
    return body


def test_format_request_with_excessive_eql():
    body = eql_body()
    body['query']['bool']['filter']['bool']['must'].append({'eql': 'newer query'})
    expected_body = {'filter': {'bool': {'must': [{'other': 'other filter'}]}}, 'query': 'newer query'}
    assert eql.format_request(body) == expected_body


def test_format_results_without_events():
    expected_results = {'hits': {'hits': []}}
    results = expected_results
    assert eql.format_results(results) == expected_results


def test_format_results_with_events():
    expected_results = {'hits': {'hits': [{'foo': 'bar'}]}, 'eql': True}
    results = {'hits': {'events': [{'foo': 'bar'}]}}
    assert eql.format_results(results) == expected_results


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


def test_search_without_eql():
    es_client = init_client()

    expected_params = {'from': True, 'size': 12, 'scroll': True, '_source_includes': True}
    expected_headers = {}
    expected_body = {}
    results = {}
    es_client.transport = mock.Mock()
    es_client.transport.perform_request.return_value = results

    body = {}
    params = {'from_': True, 'size': 12, 'scroll': True, '_source_includes': True}
    es_client.search(body=body, index='test', params=params)
    es_client.transport.perform_request.assert_called_with('POST', '/test/_search',
                                                           params=expected_params,
                                                           headers=expected_headers,
                                                           body=expected_body)


def test_search_with_eql():
    es_client = init_client()

    expected_params = {'from': True}
    expected_headers = {}
    expected_body = {'filter': {'bool': {'must': [{'other': 'other filter'}]}}, 'query': 'test query', 'size': 12}
    results = {}
    es_client.transport = mock.Mock()
    es_client.transport.perform_request.return_value = results

    body = eql_body()
    params = {'from_': True, 'size': 12, 'scroll': True, '_source_includes': True}
    results = es_client.search(body=body, index='test', params=params)
    es_client.transport.perform_request.assert_called_with('POST', '/test/_eql/search',
                                                           params=expected_params,
                                                           headers=expected_headers,
                                                           body=expected_body)
