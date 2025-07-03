# -*- coding: utf-8 -*-
from datetime import timedelta
import pytest

from elastalert.opensearch_discover import generate_opensearch_discover_url


@pytest.mark.parametrize("opensearch_version", [
    '2.11',
    '3.0',
    '0.0',
    ' '
])
def test_generate_opensearch_discover_url_with_relative_opensearch_discover_app_url(opensearch_version):
    url = generate_opensearch_discover_url(
        rule={
            'opensearch_discover_app_url': 'http://opensearch:5601/#/discover',
            'opensearch_discover_version': opensearch_version,
            'opensearch_discover_index_pattern_id': 'd6cabfb6-aaef-44ea-89c5-600e9a76991a',
            'timestamp_field': 'timestamp'
        },
        match={
            'timestamp': '2019-09-01T00:30:00Z'
        }
    )
    expectedUrl = (
        'http://opensearch:5601/#/discover'
        + '?_g=%28'  # global start
        + 'filters%3A%21%28%29%2C'
        + 'refreshInterval%3A%28pause%3A%21t%2Cvalue%3A0%29%2C'
        + 'time%3A%28'  # time start
        + 'from%3A%272019-09-01T00%3A20%3A00Z%27%2C'
        + 'to%3A%272019-09-01T00%3A40%3A00Z%27'
        + '%29'  # time end
        + '%29'  # global end
        + '&_a=%28'  # app start
        + 'discover%3A%28columns%3A%21%28_source%29%2C'
        + 'isDirty%3A%21f%2Csort%3A%21%28%29%29%2C'
        + 'metadata%3A%28indexPattern%3Ad6cabfb6-aaef-44ea-89c5-600e9a76991a%2C'
        + 'view%3Adiscover%29%29'  # app end
        + '&_q=%28filters%3A%21%28%29%2C'  # query and filter start
        + 'query%3A%28language%3Alucene%2Cquery%3A%27%27%29%29'  # query and filter start
    )
    assert url == expectedUrl


def test_generate_opensearch_discover_url_with_relative_opensearch_discover_app_url_without_http():
    url = generate_opensearch_discover_url(
        rule={
            'opensearch_discover_app_url': 'app/discover#/',
            'opensearch_discover_version': '2.11',
            'opensearch_discover_index_pattern_id': '620ad0e6-43df-4557-bda2-384960fa9086',
            'timestamp_field': 'timestamp'
        },
        match={
            'timestamp': '2021-10-08T00:30:00Z'
        }
    )
    expectedUrl = (
        'app/discover#/'
        + '?_g=%28'
        + 'filters%3A%21%28%29%2C'
        + 'refreshInterval%3A%28pause%3A%21t%2Cvalue%3A0%29%2C'
        + 'time%3A%28'
        + 'from%3A%272021-10-08T00%3A20%3A00Z%27%2C'
        + 'to%3A%272021-10-08T00%3A40%3A00Z%27'
        + '%29'
        + '%29'
        + '&_a=%28'
        + 'discover%3A%28columns%3A%21%28_source%29%2C'
        + 'isDirty%3A%21f%2Csort%3A%21%28%29%29%2C'
        + 'metadata%3A%28indexPattern%3A%27620ad0e6-43df-4557-bda2-384960fa9086%27%2Cview%3Adiscover%29%29'
        + '&_q=%28filters%3A%21%28%29%2Cquery%3A%28language%3Alucene%2Cquery%3A%27%27%29%29'
    )
    assert url == expectedUrl


def test_generate_opensearch_discover_url_with_missing_opensearch_discover_version():
    url = generate_opensearch_discover_url(
        rule={
            'opensearch_discover_app_url': 'http://opensearch:5601/#/discover',
            'opensearch_discover_index_pattern_id': 'd6cabfb6-aaef-44ea-89c5-600e9a76991a',
            'timestamp_field': 'timestamp',
            'name': 'test'
        },
        match={
            'timestamp': '2019-09-01T00:30:00Z'
        }
    )
    expectedUrl = (
        'http://opensearch:5601/#/discover'
        + '?_g=%28'  # global start
        + 'filters%3A%21%28%29%2C'
        + 'refreshInterval%3A%28pause%3A%21t%2Cvalue%3A0%29%2C'
        + 'time%3A%28'  # time start
        + 'from%3A%272019-09-01T00%3A20%3A00Z%27%2C'
        + 'to%3A%272019-09-01T00%3A40%3A00Z%27'
        + '%29'  # time end
        + '%29'  # global end
        + '&_a=%28'  # app start
        + 'discover%3A%28columns%3A%21%28_source%29%2C'
        + 'isDirty%3A%21f%2Csort%3A%21%28%29%29%2C'
        + 'metadata%3A%28indexPattern%3Ad6cabfb6-aaef-44ea-89c5-600e9a76991a%2C'
        + 'view%3Adiscover%29%29'  # app end
        + '&_q=%28filters%3A%21%28%29%2C'  # query and filter start
        + 'query%3A%28language%3Alucene%2Cquery%3A%27%27%29%29'  # query and filter start
    )
    assert url == expectedUrl


def test_generate_opensearch_discover_url_with_missing_opensearch_discover_app_url():
    url = generate_opensearch_discover_url(
        rule={
            'opensearch_discover_version': '8.11',
            'opensearch_discover_index_pattern_id': 'logs',
            'timestamp_field': 'timestamp',
            'name': 'test'
        },
        match={
            'timestamp': '2019-09-01T00:30:00Z'
        }
    )
    assert url is None


def test_generate_opensearch_discover_url_with_missing_opensearch_discover_index_pattern_id():
    url = generate_opensearch_discover_url(
        rule={
            'opensearch_discover_app_url': 'http://opensearch:5601/#/discover',
            'opensearch_discover_version': '8.11',
            'timestamp_field': 'timestamp',
            'name': 'test'
        },
        match={
            'timestamp': '2019-09-01T00:30:00Z'
        }
    )
    assert url is None


def test_generate_opensearch_discover_url_with_invalid_opensearch_version():
    url = generate_opensearch_discover_url(
        rule={
            'opensearch_discover_app_url': 'http://opensearch:5601/#/discover',
            'opensearch_discover_version': '4.5',
            'opensearch_discover_index_pattern_id': 'd6cabfb6-aaef-44ea-89c5-600e9a76991a',
            'timestamp_field': 'timestamp'
        },
        match={
            'timestamp': '2019-09-01T00:30:00Z'
        }
    )
    expectedUrl = (
        'http://opensearch:5601/#/discover'
        + '?_g=%28'  # global start
        + 'filters%3A%21%28%29%2C'
        + 'refreshInterval%3A%28pause%3A%21t%2Cvalue%3A0%29%2C'
        + 'time%3A%28'  # time start
        + 'from%3A%272019-09-01T00%3A20%3A00Z%27%2C'
        + 'to%3A%272019-09-01T00%3A40%3A00Z%27'
        + '%29'  # time end
        + '%29'  # global end
        + '&_a=%28'  # app start
        + 'discover%3A%28columns%3A%21%28_source%29%2C'
        + 'isDirty%3A%21f%2Csort%3A%21%28%29%29%2C'
        + 'metadata%3A%28indexPattern%3Ad6cabfb6-aaef-44ea-89c5-600e9a76991a%2C'
        + 'view%3Adiscover%29%29'  # app end
        + '&_q=%28filters%3A%21%28%29%2C'  # query and filter start
        + 'query%3A%28language%3Alucene%2Cquery%3A%27%27%29%29'  # query and filter start
    )
    assert url == expectedUrl


def test_generate_opensearch_discover_url_with_from_timedelta_and_timeframe():
    url = generate_opensearch_discover_url(
        rule={
            'opensearch_discover_app_url': 'http://opensearch:5601/#/discover',
            'opensearch_discover_version': '2.11',
            'opensearch_discover_index_pattern_id': 'd6cabfb6-aaef-44ea-89c5-600e9a76991a',
            'opensearch_discover_from_timedelta': timedelta(hours=1),
            'timeframe': timedelta(minutes=20),
            'timestamp_field': 'timestamp'
        },
        match={
            'timestamp': '2019-09-01T04:00:00Z'
        }
    )
    expectedUrl = (
        'http://opensearch:5601/#/discover'
        + '?_g=%28'
        + 'filters%3A%21%28%29%2C'
        + 'refreshInterval%3A%28pause%3A%21t%2Cvalue%3A0%29%2C'
        + 'time%3A%28'
        + 'from%3A%272019-09-01T03%3A00%3A00Z%27%2C'
        + 'to%3A%272019-09-01T04%3A20%3A00Z%27'
        + '%29'
        + '%29'
        + '&_a=%28discover%3A%28columns%3A%21%28_source%29%2C'
        + 'isDirty%3A%21f%2Csort%3A%21%28%29%29%2C'
        + 'metadata%3A%28indexPattern%3Ad6cabfb6-aaef-44ea-89c5-600e9a76991a%2Cview%3Adiscover%29%29'
        + '&_q=%28filters%3A%21%28%29%2Cquery%3A%28language%3Alucene%2Cquery%3A%27%27%29%29'
    )
    assert url == expectedUrl


def test_generate_opensearch_discover_url_with_to_timedelta_and_timeframe():
    url = generate_opensearch_discover_url(
        rule={
            'opensearch_discover_app_url': 'http://opensearch:5601/#/discover',
            'opensearch_discover_version': '2.11',
            'opensearch_discover_index_pattern_id': 'd6cabfb6-aaef-44ea-89c5-600e9a76991a',
            'opensearch_discover_to_timedelta': timedelta(hours=1),
            'timeframe': timedelta(minutes=20),
            'timestamp_field': 'timestamp'
        },
        match={
            'timestamp': '2019-09-01T04:00:00Z'
        }
    )
    expectedUrl = (
        'http://opensearch:5601/#/discover'
        + '?_g=%28'
        + 'filters%3A%21%28%29%2C'
        + 'refreshInterval%3A%28pause%3A%21t%2Cvalue%3A0%29%2C'
        + 'time%3A%28'
        + 'from%3A%272019-09-01T03%3A40%3A00Z%27%2C'
        + 'to%3A%272019-09-01T05%3A00%3A00Z%27'
        + '%29'
        + '%29'
        + '&_a=%28discover%3A%28columns%3A%21%28_source%29%2C'
        + 'isDirty%3A%21f%2Csort%3A%21%28%29%29%2C'
        + 'metadata%3A%28indexPattern%3Ad6cabfb6-aaef-44ea-89c5-600e9a76991a%2Cview%3Adiscover%29%29'
        + '&_q=%28filters%3A%21%28%29%2Cquery%3A%28language%3Alucene%2Cquery%3A%27%27%29%29'
    )
    assert url == expectedUrl


def test_generate_opensearch_discover_url_with_custom_columns():
    url = generate_opensearch_discover_url(
        rule={
            'opensearch_discover_app_url': 'http://opensearch:5601/#/discover',
            'opensearch_discover_version': '2.11',
            'opensearch_discover_index_pattern_id': 'logs-*',
            'opensearch_discover_columns': ['level', 'message'],
            'timestamp_field': 'timestamp'
        },
        match={
            'timestamp': '2019-09-01T00:30:00Z'
        }
    )
    expectedUrl = (
        'http://opensearch:5601/#/discover'
        + '?_g=%28'
        + 'filters%3A%21%28%29%2CrefreshInterval%3A%28pause%3A%21t%2Cvalue%3A0%29%2C'
        + 'time%3A%28'
        + 'from%3A%272019-09-01T00%3A20%3A00Z%27%2C'
        + 'to%3A%272019-09-01T00%3A40%3A00Z%27%'
        + '29%'
        + '29'
        + '&_a=%28'
        + 'discover%3A%28columns%3A%21%28level%2Cmessage%29%2C'
        + 'isDirty%3A%21f%2Csort%3A%21%28%29%29%2C'
        + 'metadata%3A%28indexPattern%3A%27logs-%2A%27%2Cview%3Adiscover%29%29'
        + '&_q=%28filters%3A%21%28%29%2Cquery%3A%28language%3Alucene%2Cquery%3A%27%27%29%29'
    )
    assert url == expectedUrl


def test_generate_opensearch_discover_url_with_single_filter():
    url = generate_opensearch_discover_url(
        rule={
            'opensearch_discover_app_url': 'http://opensearch:5601/#/discover',
            'opensearch_discover_version': '2.11',
            'opensearch_discover_index_pattern_id': 'logs-*',
            'timestamp_field': 'timestamp',
            'filter': [
                {'term': {'level': 30}}
            ]
        },
        match={
            'timestamp': '2019-09-01T00:30:00Z'
        }
    )
    expectedUrl = (
        'http://opensearch:5601/#/discover'
        + '?_g=%28'
        + 'filters%3A%21%28%29%2CrefreshInterval%3A%28pause%3A%21t%2Cvalue%3A0%29%2C'
        + 'time%3A%28'
        + 'from%3A%272019-09-01T00%3A20%3A00Z%27%2C'
        + 'to%3A%272019-09-01T00%3A40%3A00Z%27%'
        + '29%'
        + '29'
        + '&_a=%28'
        + 'discover%3A%28columns%3A%21%28_source%29%2C'
        + 'isDirty%3A%21f%2Csort%3A%21%28%29%29%2C'
        + 'metadata%3A%28indexPattern%3A%27logs-%2A%27%2Cview%3Adiscover'
        + '%29'
        + '%29'
        + '&_q=%28'
        + 'filters%3A%21%28%28%27%24state%27%3A%28store%3AappState%29'
        + '%2Cmeta%3A%28alias%3Afilter%2Cdisabled%3A%21f%2Cindex%3A%27logs-%2A%27%2C'
        + 'key%3Aquery%2Cnegate%3A%21f%2Ctype%3Acustom%2Cvalue%3A%27%7B%22bool%22%3A%7B%22'
        + 'must%22%3A%5B%7B%22term%22%3A%7B%22level%22%3A30%7D%7D%5D%7D%7D%27%29'
        + '%2Cquery%3A%28bool%3A%28must%3A%21%28%28term%3A%28level%3A30%29%29%29%29%29%29%29%2C'
        + 'query%3A%28language%3Alucene%2Cquery%3A%27%27%29%29'  # app end
    )
    assert url == expectedUrl


def test_generate_opensearch_discover_url_with_multiple_filters():
    url = generate_opensearch_discover_url(
        rule={
            'opensearch_discover_app_url': 'http://opensearch:5601/#/discover',
            'opensearch_discover_version': '2.11',
            'opensearch_discover_index_pattern_id': '90943e30-9a47-11e8-b64d-95841ca0b247',
            'timestamp_field': 'timestamp',
            'filter': [
                {'term': {'app': 'test'}},
                {'term': {'level': 30}}
            ]
        },
        match={
            'timestamp': '2019-09-01T00:30:00Z'
        }
    )
    expectedUrl = (
        'http://opensearch:5601/#/discover'
        + '?_g=%28'  # global start
        + 'filters%3A%21%28%29%2CrefreshInterval%3A%28pause%3A%21t%2Cvalue%3A0%29%2C'
        + 'time%3A%28'
        + 'from%3A%272019-09-01T00%3A20%3A00Z%27%2C'
        + 'to%3A%272019-09-01T00%3A40%3A00Z%27'
        + '%29'
        + '%29'
        + '&_a=%28'
        + 'discover%3A%28columns%3A%21%28_source%29%2CisDirty%3A%21f%2Csort%3A%21%28%29%29%2C'
        + 'metadata%3A%28indexPattern%3A%2790943e30-9a47-11e8-b64d-95841ca0b247%27%2Cview%3Adiscover%29%29'
        + '&_q=%28'
        + 'filters%3A%21%28%28%27%24state%27%3A%28store%3AappState%29%2Cmeta%3A%28'
        + 'alias%3Afilter%2Cdisabled%3A%21f%2Cindex%3A%2790943e30-9a47-11e8-b64d-95841ca0b247%27%2C'
        + 'key%3Aquery%2Cnegate%3A%21f%2Ctype%3Acustom%2Cvalue%3A%27%7B%22'
        + 'bool%22%3A%7B%22must%22%3A%5B%7B%22term%22%3A%7B%22app%22%3A%22'
        + 'test%22%7D%7D%2C%7B%22term%22%3A%7B%22level%22%3A30%7D%7D%5D%7D%7D%27%29%2C'
        + 'query%3A%28bool%3A%28must%3A%21%28%28term%3A%28'
        + 'app%3Atest%29%29%2C%28term%3A%28level%3A30%29%29%29%29%29%29%29%2C'
        + 'query%3A%28language%3Alucene%2Cquery%3A%27%27%29%29'  # app end
    )
    assert url == expectedUrl


def test_generate_opensearch_discover_url_with_int_query_key():
    url = generate_opensearch_discover_url(
        rule={
            'opensearch_discover_app_url': 'http://opensearch:5601/#/discover',
            'opensearch_discover_version': '2.11',
            'opensearch_discover_index_pattern_id': 'logs-*',
            'timestamp_field': 'timestamp',
            'query_key': 'geo.dest'
        },
        match={
            'timestamp': '2019-09-01T00:30:00Z',
            'geo.dest': 200
        }
    )
    expectedUrl = (
        'http://opensearch:5601/#/discover'
        + '?_g=%28'  # global start
        + 'filters%3A%21%28%29%2CrefreshInterval%3A%28pause%3A%21t%2Cvalue%3A0%29%2C'
        + 'time%3A%28'
        + 'from%3A%272019-09-01T00%3A20%3A00Z%27%2C'
        + 'to%3A%272019-09-01T00%3A40%3A00Z%27'
        + '%29'
        + '%29'
        + '&_a=%28'
        + 'discover%3A%28columns%3A%21%28_source%29%2CisDirty%3A%21f%2Csort%3A%21%28%29%29%2C'
        + 'metadata%3A%28indexPattern%3A%27logs-%2A%27%2Cview%3Adiscover%29'
        + '%29'
        + '&_q=%28'
        + 'filters%3A%21%28%28%27%24state%27%3A%28store%3AappState%29%2C'
        + 'meta%3A%28alias%3A%21n%2Cdisabled%3A%21f%2Cindex%3A%27logs-%2A%27%2C'
        + 'key%3Ageo.dest%2Cnegate%3A%21f%2Cparams%3A%28'
        + 'query%3A200%2Ctype%3Aphrase%29%2Ctype%3Aphrase%2Cvalue%3A%27200%27%29%2C'
        + 'query%3A%28match%3A%28geo.dest%3A%28query%3A200%2C'
        + 'type%3Aphrase%29%29%29%29%29%2C'
        + 'query%3A%28language%3Alucene%2Cquery%3A%27%27%29%29'  # app end
    )
    assert url == expectedUrl


def test_generate_opensearch_discover_url_with_str_query_key():
    url = generate_opensearch_discover_url(
        rule={
            'opensearch_discover_app_url': 'http://opensearch:5601/#/discover',
            'opensearch_discover_version': '2.11',
            'opensearch_discover_index_pattern_id': 'logs-*',
            'timestamp_field': 'timestamp',
            'query_key': 'geo.dest'
        },
        match={
            'timestamp': '2019-09-01T00:30:00Z',
            'geo': {
                'dest': 'ok'
            }
        }
    )
    expectedUrl = (
        'http://opensearch:5601/#/discover'
        + '?_g=%28'  # global start
        + 'filters%3A%21%28%29%2CrefreshInterval%3A%28pause%3A%21t%2Cvalue%3A0%29%2C'
        + 'time%3A%28'
        + 'from%3A%272019-09-01T00%3A20%3A00Z%27%2C'
        + 'to%3A%272019-09-01T00%3A40%3A00Z%27'
        + '%29%'
        + '29'
        + '&_a=%28'
        + 'discover%3A%28columns%3A%21%28_source%29%2CisDirty%3A%21f%2Csort%3A%21%28%29%29%2C'
        + 'metadata%3A%28indexPattern%3A%27logs-%2A%27%2Cview%3Adiscover'
        + '%29'
        + '%29'
        + '&_q='
        + '%28filters%3A%21%28%28%27%24state%27%3A%28store%3AappState%29%2C'
        + 'meta%3A%28alias%3A%21n%2Cdisabled%3A%21f%2Cindex%3A%27logs-%2A%27%2C'
        + 'key%3Ageo.dest%2Cnegate%3A%21f%2Cparams%3A%28query%3Aok%2Ctype%3Aphrase%29%2C'
        + 'type%3Aphrase%2Cvalue%3Aok%29%2Cquery%3A%28match%3A%28'
        + 'geo.dest%3A%28query%3Aok%2Ctype%3Aphrase%29%29%29%29%29%2C'
        + 'query%3A%28language%3Alucene%2Cquery%3A%27%27%29%29'  # app end
    )
    assert url == expectedUrl


def test_generate_opensearch_discover_url_with_missing_query_key_value():
    url = generate_opensearch_discover_url(
        rule={
            'opensearch_discover_app_url': 'http://opensearch:5601/#/discover',
            'opensearch_discover_version': '2.11',
            'opensearch_discover_index_pattern_id': 'logs-*',
            'timestamp_field': 'timestamp',
            'query_key': 'status'
        },
        match={
            'timestamp': '2019-09-01T00:30:00Z'
        }
    )
    expectedUrl = (
        'http://opensearch:5601/#/discover'
        + '?_g=%28'  # global start
        + 'filters%3A%21%28%29%2CrefreshInterval%3A%28pause%3A%21t%2Cvalue%3A0%29%2C'
        + 'time%3A%28'
        + 'from%3A%272019-09-01T00%3A20%3A00Z%27%2C'
        + 'to%3A%272019-09-01T00%3A40%3A00Z%27'
        + '%29'
        + '%29'
        + '&_a=%28'
        + 'discover%3A%28columns%3A%21%28_source%29%2CisDirty%3A%21f%2Csort%3A%21%28%29%29%2C'
        + 'metadata%3A%28indexPattern%3A%27logs-%2A%27%2Cview%3Adiscover'
        + '%29'
        + '%29&'
        + '_q=%28'
        + 'filters%3A%21%28%28%27%24state%27%3A%28store%3AappState%29%2Cexists%3A%28field%3Astatus%29%2C'
        + 'meta%3A%28alias%3A%21n%2Cdisabled%3A%21f%2Cindex%3A%27logs-%2A%27%2C'
        + 'key%3Astatus%2Cnegate%3A%21t%2Ctype%3Aexists%2C'
        + 'value%3Aexists%2Cview%3Adiscover%29%29%29%2C'
        + 'query%3A%28language%3Alucene%2Cquery%3A%27%27%29%29'  # app end
    )
    assert url == expectedUrl


def test_generate_opensearch_discover_url_with_compound_query_key():
    url = generate_opensearch_discover_url(
        rule={
            'opensearch_discover_app_url': 'http://opensearch:5601/#/discover',
            'opensearch_discover_version': '2.11',
            'opensearch_discover_index_pattern_id': 'logs-*',
            'timestamp_field': 'timestamp',
            'compound_query_key': ['geo.src', 'geo.dest'],
            'query_key': 'geo.src,geo.dest'
        },
        match={
            'timestamp': '2019-09-01T00:30:00Z',
            'geo': {
                'src': 'CA',
                'dest': 'US'
            }
        }
    )
    expectedUrl = (
        'http://opensearch:5601/#/discover'
        + '?_g=%28'  # global start
        + 'filters%3A%21%28%29%2CrefreshInterval%3A%28pause%3A%21t%2Cvalue%3A0%29%2C'
        + 'time%3A%28'
        + 'from%3A%272019-09-01T00%3A20%3A00Z%27%2C'
        + 'to%3A%272019-09-01T00%3A40%3A00Z%27'
        + '%29'
        + '%29'
        + '&_a=%28'
        + 'discover%3A%28columns%3A%21%28_source%29%2CisDirty%3A%21f%2Csort%3A%21%28%29%29%2C'
        + 'metadata%3A%28indexPattern%3A%27logs-%2A%27%2Cview%3Adiscover%29%29'
        + '&_q=%28'
        + 'filters%3A%21%28%28%27%24state%27%3A%28store%3AappState%29%2C'
        + 'meta%3A%28alias%3A%21n%2Cdisabled%3A%21f%2Cindex%3A%27logs-%2A%27%2C'
        + 'key%3Ageo.src%2Cnegate%3A%21f%2Cparams%3A%28'
        + 'query%3ACA%2Ctype%3Aphrase%29%2Ctype%3Aphrase%2Cvalue%3ACA%29%2C'
        + 'query%3A%28match%3A%28geo.src%3A%28query%3ACA%2Ctype%3Aphrase%29%29%29%29%'
        + '2C%28%27%24state%27%3A%28store%3AappState%29%2Cmeta%3A%28alias%3A%21n%2Cdisabled%3A%21f%2C'
        + 'index%3A%27logs-%2A%27%2Ckey%3Ageo.dest%2Cnegate%3A%21f%2Cparams%3A%28'
        + 'query%3AUS%2Ctype%3Aphrase%29%2Ctype%3Aphrase%2Cvalue%3AUS%29%2C'
        + 'query%3A%28match%3A%28geo.dest%3A%28'
        + 'query%3AUS%2Ctype%3Aphrase%29%29%29%29%29%2C'
        + 'query%3A%28language%3Alucene%2Cquery%3A%27%27%29%29'  # app end
    )
    assert url == expectedUrl


def test_generate_opensearch_discover_url_with_filter_and_query_key():
    url = generate_opensearch_discover_url(
        rule={
            'opensearch_discover_app_url': 'http://opensearch:5601/#/discover',
            'opensearch_discover_version': '2.11',
            'opensearch_discover_index_pattern_id': 'logs-*',
            'timestamp_field': 'timestamp',
            'filter': [
                {'term': {'level': 30}}
            ],
            'query_key': 'status'
        },
        match={
            'timestamp': '2019-09-01T00:30:00Z',
            'status': 'ok'
        }
    )
    expectedUrl = (
        'http://opensearch:5601/#/discover'
        + '?_g=%28'  # global start
        + 'filters%3A%21%28%29%2C'
        + 'refreshInterval%3A%28pause%3A%21t%2Cvalue%3A0%29%2C'
        + 'time%3A%28'
        + 'from%3A%272019-09-01T00%3A20%3A00Z%27%2C'
        + 'to%3A%272019-09-01T00%3A40%3A00Z%27'
        + '%29'
        + '%29'
        + '&_a=%28'
        + 'discover%3A%28columns%3A%21%28_source%29%2CisDirty%3A%21f%2Csort%3A%21%28%29%29%2C'
        + 'metadata%3A%28indexPattern%3A%27logs-%2A%27%2Cview%3Adiscover%29%29'
        + '&_q=%28'
        + 'filters%3A%21%28%28%27%24state%27%3A%28store%3AappState%29%2C'
        + 'meta%3A%28alias%3Afilter%2Cdisabled%3A%21f%2Cindex%3A%27logs-%2A%27%2Ckey%3A'
        + 'query%2Cnegate%3A%21f%2Ctype%3Acustom%2Cvalue%3A%27%7B%22'
        + 'bool%22%3A%7B%22must%22%3A%5B%7B%22'
        + 'term%22%3A%7B%22level%22%3A30%7D%7D%5D%7D%7D%27%29%2C'
        + 'query%3A%28bool%3A%28must%3A%21%28%28term%3A%28level%3A30%29%29%29%29%29%29%2C%28%27%24'
        + 'state%27%3A%28store%3AappState%29%2Cmeta%3A%28alias%3A%21n%2Cdisabled%3A%21f%2C'
        + 'index%3A%27logs-%2A%27%2Ckey%3Astatus'
        + '%2Cnegate%3A%21f%2Cparams%3A%28query%3Aok%2Ctype%3Aphrase%29%2Ctype%3Aphrase%2Cvalue%3Aok%29%2C'
        + 'query%3A%28match%3A%28status%3A%28query%3Aok%2Ctype%3Aphrase%29%29%29%29%29%2C'
        + 'query%3A%28language%3Alucene%2Cquery%3A%27%27%29%29'  # app end
    )
    assert url == expectedUrl


def test_generate_opensearch_discover_url_with_querystring_filter_and_query_key():
    url = generate_opensearch_discover_url(
        rule={
            'opensearch_discover_app_url': 'http://opensearch:5601/#/discover',
            'opensearch_discover_version': '2.11',
            'opensearch_discover_index_pattern_id': 'logs-*',
            'timestamp_field': 'timestamp',
            'filter': [
                {'query': {'query_string': {'query': 'hello world'}}}
            ],
            'query_key': 'status'
        },
        match={
            'timestamp': '2019-09-01T00:30:00Z',
            'status': 'ok'
        }
    )
    expectedUrl = (
        'http://opensearch:5601/#/discover'
        + '?_g=%28'  # global start
        + 'filters%3A%21%28%29%2C'
        + 'refreshInterval%3A%28pause%3A%21t%2Cvalue%3A0%29%2C'
        + 'time%3A%28'
        + 'from%3A%272019-09-01T00%3A20%3A00Z%27%2C'
        + 'to%3A%272019-09-01T00%3A40%3A00Z%27'
        + '%29'
        + '%29'
        + '&_a=%28'
        + 'discover%3A%28columns%3A%21%28_source%29%2CisDirty%3A%21f%2Csort%3A%21%28%29%29%2C'
        + 'metadata%3A%28indexPattern%3A%27logs-%2A%27%2Cview%3Adiscover%29%29'
        + '&_q=%28'
        + 'filters%3A%21%28%28%27%24state%27%3A%28store%3AappState%29%2C'
        + 'meta%3A%28alias%3Afilter%2Cdisabled%3A%21f%2Cindex%3A%27logs-%2A%27%2Ckey%3A'
        + 'query%2Cnegate%3A%21f%2Ctype%3Acustom%2Cvalue%3A%27%7B%22bool%22%3A%7B%22'
        + 'must%22%3A%5B%7B%22query_string%22%3A%7B%22'
        + 'query%22%3A%22hello%20world%22%7D%7D%5D%7D%7D%27%29%2C'
        + 'query%3A%28bool%3A%28must%3A%21%28%28query_string%3A%28query%3A%27hello%20'
        + 'world%27%29%29%29%29%29%29%2C%28%27%24'
        + 'state%27%3A%28store%3AappState%29%2Cmeta%3A%28alias%3A%21n%2C'
        + 'disabled%3A%21f%2Cindex%3A%27logs-%2A%27%2Ckey%3Astatus%2Cnegate%3A%21f%2Cparams%3A%28'
        + 'query%3Aok%2Ctype%3Aphrase%29%2Ctype%3Aphrase%2Cvalue%3Aok%29%2C'
        + 'query%3A%28match%3A%28status%3A%28query%3Aok%2Ctype%3Aphrase%29%29%29%29%29%2C'
        + 'query%3A%28language%3Alucene%2Cquery%3A%27%27%29%29'  # app end
    )
    assert url == expectedUrl
