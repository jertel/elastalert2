import pytest
from datetime import datetime,timedelta

from elastalert.util import dt_to_ts


@pytest.fixture
def example_agg_response():
    res = {
        'took': 1,
        'timed_out': False,
        '_shards': {'total': 3, 'successful': 3, 'skipped': 0, 'failed': 0},
        'hits': {
            'total': {'value': 9, 'relation': 'eq'},
            'max_score': None,
            'hits': []},
        'aggregations':{
            'counts': {
                'doc_count_error_upper_bound': 0,
                'sum_other_doc_count': 0,
                'buckets': [{'key': '10.0.4.174', 'doc_count': 2},
                            {'key': '10.0.4.241', 'doc_count': 2},
                            {'key': '10.0.4.76', 'doc_count': 1},
                            {'key': '10.0.4.123', 'doc_count': 1},
                            {'key': '10.0.4.156', 'doc_count': 1},
                            {'key': '10.0.4.231', 'doc_count': 1},
                            {'key': '10.0.4.248', 'doc_count': 1}]}}
    }
    return res


def test_query_key_filter_happy_path(ea, example_agg_response):

    ea.rules[0]['compound_query_key'] = ['server_ip', 'service_name']
    qk = ('172.16.1.10', '/api/v1/endpoint-foo')
    qk_csv = ", ".join(qk)
    index = 'foo-2023-13-13' #lousy Smarch weather
    top_term_key = 'client_ip'

    endtime = datetime.now()
    starttime = endtime - timedelta(hours=1)
    ea.thread_data.current_es.search.return_value = example_agg_response

    hit_terms = ea.get_hits_terms(
        rule=ea.rules[0],
        starttime=starttime,
        endtime=endtime,
        index=index,
        key=top_term_key,
        qk = qk_csv,
        size=None
    )
    assert endtime in hit_terms
    assert hit_terms[endtime] == example_agg_response['aggregations']['counts']['buckets']

    expected_filters = [
        {'range': {'@timestamp': {
            'gt': dt_to_ts(starttime),
            'lte': dt_to_ts(endtime)}}},
        {'term': {f'{ea.rules[0]['compound_query_key'][0]}.keyword': qk[0]}},
        {'term': {f'{ea.rules[0]['compound_query_key'][1]}.keyword': qk[1]}}
    ]
    expected_query = {
        'query': {'bool': {'filter': {'bool': {'must': expected_filters}}}},
         # 50 harded coded in get_hits_terms as a default for size=None
        'aggs': {'counts': {'terms': {'field': top_term_key, 'size': 50, 'min_doc_count': 1}}}
    }
    ea.thread_data.current_es.search.assert_called_with(index=index,body=expected_query, size=0, ignore_unavailable=True)