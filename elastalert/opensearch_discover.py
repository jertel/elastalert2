# -*- coding: utf-8 -*-
# flake8: noqa
import datetime
import logging
import json
import os.path
import prison
import urllib.parse

from .util import EAException
from .util import elastalert_logger
from .util import lookup_es_key
from .util import ts_add

opensearch_default_timedelta = datetime.timedelta(minutes=10)

def generate_opensearch_discover_url(rule, match):
    ''' Creates a link for a opensearch discover app. '''

    discover_app_url = rule.get('opensearch_discover_app_url')
    if not discover_app_url:
        elastalert_logger.warning(
            'Missing opensearch_discover_app_url for rule %s' % (
                rule.get('name', '<MISSING NAME>')
            )
        )
        return None

    index = rule.get('opensearch_discover_index_pattern_id')
    if not index:
        elastalert_logger.warning(
            'Missing opensearch_discover_index_pattern_id for rule %s' % (
                rule.get('name', '<MISSING NAME>')
            )
        )
        return None

    columns = rule.get('opensearch_discover_columns', ['_source'])
    filters = rule.get('filter', [])

    if 'query_key' in rule:
        query_keys = rule.get('compound_query_key', [rule['query_key']])
    else:
        query_keys = []

    timestamp = lookup_es_key(match, rule['timestamp_field'])
    timeframe = rule.get('timeframe', opensearch_default_timedelta)
    from_timedelta = rule.get('opensearch_discover_from_timedelta', timeframe)
    from_time = ts_add(timestamp, -from_timedelta)
    to_timedelta = rule.get('opensearch_discover_to_timedelta', timeframe)
    to_time = ts_add(timestamp, to_timedelta)

    globalState = opensearch_disover_global_state(from_time, to_time)
    appState = opensearch_discover_app_state(index, columns, filters, query_keys, match)
    appFilter = opensearch_discover_app_filter(index, columns, filters, query_keys, match)

    urlqueryOriginal = "%s?_g=%s&_a=%s&_q=%s" % (
        os.path.expandvars(discover_app_url),
        urllib.parse.quote(globalState),
        urllib.parse.quote(appState),
        urllib.parse.quote(appFilter)
    )
    
    word_to_replace = 'tobereplacedbylucenequery'
    replacement_word = 'query'
    max_replacements = 1  # Replace only the first occurrence
    urlquery = urlqueryOriginal.replace(word_to_replace, replacement_word, max_replacements)
    return urlquery


def opensearch_disover_global_state(from_time, to_time):
    return prison.dumps( {
        'filters': [],
        'refreshInterval': {
            'pause': True,
            'value': 0
        },
        'time': {
            'from': from_time,
            'to': to_time
        }
    } )


def opensearch_discover_app_state(index, columns, filters, query_keys, match):
    return prison.dumps( {
        'discover': {
            'columns': columns,
            'isDirty': False,
            'sort': []
        },
        'metadata': {
            'indexPattern': index,
            'view': 'discover'
        }
    } )

def opensearch_discover_app_filter(index, columns, filters, query_keys, match):
    app_filters = []

    if filters:

        new_filters = []
        for filter in filters:
            if 'query' in filter:
                filter = filter['query']
            new_filters.append(filter)
        filters = new_filters

        bool_filter = {'bool': {'must': filters } }
        app_filters.append( {
            '$state': {
                'store': 'appState'
            },
            'meta': {
                'alias': 'filter',
                'disabled': False,
                'index': index,
                'key': 'query',
                'negate': False,
                'type': 'custom',
                'value': json.dumps(bool_filter, separators=(',', ':'))
            },
            'query': bool_filter
        } )

    for query_key in query_keys:
        query_value = lookup_es_key(match, query_key)

        if query_value is None:
            app_filters.append( {
                '$state': {
                    'store': 'appState'
                },
                'exists': {
                    'field': query_key
                },
                'meta': {
                    'alias': None,
                    'disabled': False,
                    'index': index,
                    'key': query_key,
                    'negate': True,
                    'type': 'exists',
                    'view': 'discover',
                    'value': 'exists'
                }
            } )

        else:
            app_filters.append( {
                '$state': {
                    'store': 'appState'
                },
                'meta': {
                    'alias': None,
                    'disabled': False,
                    'index': index,
                    'key': query_key,
                    'negate': False,
                    'params': {
                        'query': query_value,
                        'type': 'phrase'
                    },
                    'type': 'phrase',
                    'value': str(query_value)
                },
                'query': {
                    'match': {
                        query_key: {
                            'query': query_value,
                            'type': 'phrase'
                        }
                    }
                }
            } )

    return prison.dumps( {
        'filters': app_filters,
        'tobereplacedbylucenequery': {'language': 'lucene','query': ''}
    } )
