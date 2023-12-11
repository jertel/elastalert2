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


def _mock_query_key_option_loader(rule):
    '''
    So, some copypasta from loaders.load_options,

    if query_key is a string:
        no compound_query_key is created
    if query_key is a list:
        if len() > 1:
            compound_query_key is created
            query_key is replaced with ",".join() of the original query_key values
        if len() == 1:
            the query_key list with one string is normalilzed back to just a string
        if len() == 0:
            somehow it was an empty list and query_keys is silently dropped from the config
    '''
    raw_query_key = rule.get('query_key')
    if isinstance(raw_query_key, list):
        if len(raw_query_key) > 1:
            rule['compound_query_key'] = raw_query_key
            rule['query_key'] = ','.join(raw_query_key)
        elif len(raw_query_key) == 1:
            rule['query_key'] = raw_query_key[0]
        else:
            del(rule['query_key'])

@pytest.mark.parametrize(
    ["qk", "query_key"],

    #scenario A: 3 query keys
    [ ( ['172.16.1.10', '/api/v1/endpoint-foo', 'us-east-2'],
        ['server_ip', 'service_name', 'region'] ),

    #scenario B: 2 query keys
      ( ['172.16.1.10', '/api/v1/endpoint-foo'],
        ['server_ip', 'service_name'] ),

    #scenario C: 1 query key, but it was given as a list of one fieldname in the rule options
      ( ['172.16.1.10'],
        ['server_ip'] ),

    #scenario D: 1 query key, given as a string
      ( ['172.16.1.10'],
        'server_ip' ),

    #scenario E: no query key
      ( None,
        None )
   ],
)
def test_query_key_filter_happy_path(ea, example_agg_response, qk, query_key):

    if query_key is not None:
        ea.rules[0]['query_key'] = query_key

    # emulate the rule['compound_query_key'] creation logic which prob should be
    # factored out of loaders.load_options() instead of copypasta'd for the test
    _mock_query_key_option_loader(ea.rules[0])

    try:
        # todo: why are these values being passed as a commaspace-join and not a
        # comma-join like everything else?
        qk_csv = ", ".join(qk)
    except TypeError:
        qk_csv = None
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
        {'range': {'@timestamp': { 'gt': dt_to_ts(starttime), 'lte': dt_to_ts(endtime)}}}
    ]
    try:
        cqk = ea.rules[0]['compound_query_key']
        for fieldname, value in zip(cqk, qk):
            filter = {'term': {f'{fieldname}.keyword': value}}
            expected_filters.append(filter)
    except KeyError:
        #not a compound, eh?  it must be a string of a single filedname
        try:
            fieldname = ea.rules[0]['query_key']
            filter = {'term': {f'{fieldname}.keyword': qk[0]}}
            expected_filters.append(filter)
        except KeyError:
            pass # maybe the rule never had a query_key, or it was an empty list and purged

    expected_query = {
        'query': {'bool': {'filter': {'bool': {'must': expected_filters}}}},
         # 50 harded coded in get_hits_terms as a default for size=None
        'aggs': {'counts': {'terms': {'field': top_term_key, 'size': 50, 'min_doc_count': 1}}}
    }
    ea.thread_data.current_es.search.assert_called_with(index=index,body=expected_query, size=0, ignore_unavailable=True)