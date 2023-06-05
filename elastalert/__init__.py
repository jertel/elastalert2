# -*- coding: utf-8 -*-
import copy
import elastalert.eql as eql

from elasticsearch import Elasticsearch
from elasticsearch import RequestsHttpConnection
from elasticsearch.client import _make_path
from elasticsearch.client import query_params
from elasticsearch.exceptions import TransportError


class ElasticSearchClient(Elasticsearch):
    """ Extension of low level :class:`Elasticsearch` client with additional version resolving features """

    def __init__(self, conf):
        """
        :arg conf: es_conn_config dictionary. Ref. :func:`~util.build_es_conn_config`
        """
        super(ElasticSearchClient, self).__init__(host=conf.get('es_host'),
                                                  hosts=conf.get('es_hosts'),
                                                  port=conf['es_port'],
                                                  url_prefix=conf['es_url_prefix'],
                                                  use_ssl=conf['use_ssl'],
                                                  verify_certs=conf['verify_certs'],
                                                  ca_certs=conf['ca_certs'],
                                                  ssl_show_warn=conf['ssl_show_warn'],
                                                  connection_class=RequestsHttpConnection,
                                                  http_auth=conf['http_auth'],
                                                  headers=conf['headers'],
                                                  timeout=conf['es_conn_timeout'],
                                                  send_get_body_as=conf['send_get_body_as'],
                                                  client_cert=conf['client_cert'],
                                                  client_key=conf['client_key'])
        self._conf = copy.copy(conf)
        self._es_version = None

    @property
    def conf(self):
        """
        Returns the provided es_conn_config used when initializing the class instance.
        """
        return self._conf

    @property
    def es_version(self):
        """
        Returns the reported version from the Elasticsearch server.
        """
        if self._es_version is None:
            self._es_version = util.get_version_from_cluster_info(self)

        return self._es_version

    def is_atleastseven(self):
        """
        Returns True when the Elasticsearch server version >= 7
        """
        return int(self.es_version.split(".")[0]) >= 7

    def is_atleasteight(self):
        """
        Returns True when the Elasticsearch server version >= 8
        """
        return int(self.es_version.split(".")[0]) >= 8


    def resolve_writeback_index(self, writeback_index, doc_type):
        if doc_type == 'silence':
            return writeback_index + '_silence'
        elif doc_type == 'past_elastalert':
            return writeback_index + '_past'
        elif doc_type == 'elastalert_status':
            return writeback_index + '_status'
        elif doc_type == 'elastalert_error':
            return writeback_index + '_error'
        return writeback_index


    @query_params(
        "_source",
        "_source_excludes",
        "_source_includes",
        "allow_no_indices",
        "allow_partial_search_results",
        "analyze_wildcard",
        "analyzer",
        "batched_reduce_size",
        "ccs_minimize_roundtrips",
        "default_operator",
        "df",
        "docvalue_fields",
        "expand_wildcards",
        "explain",
        "from_",
        "ignore_throttled",
        "ignore_unavailable",
        "lenient",
        "max_concurrent_shard_requests",
        "pre_filter_shard_size",
        "preference",
        "q",
        "request_cache",
        "rest_total_hits_as_int",
        "routing",
        "scroll",
        "search_type",
        "seq_no_primary_term",
        "size",
        "sort",
        "stats",
        "stored_fields",
        "suggest_field",
        "suggest_mode",
        "suggest_size",
        "suggest_text",
        "terminate_after",
        "timeout",
        "track_scores",
        "track_total_hits",
        "typed_keys",
        "version",
    )
    def search(self, body=None, index=None, doc_type=None, params=None, headers=None):
        # This implementation of search is nearly identical to the base class with the following exceptions:
        # 1. If the request body contains an EQL query, the body will be restructured to support the EQL API.
        # 2. The path will be set to the EQL API endpoint, if #1 is true.
        # 3. The scroll and _source_includes params will be dropped if #1 is true, since the EQL API doesn't support them.
        # 4. The size param will be moved to a body parameter instead of a top-level param if #1 is true.
        # 5. The results will be converted from EQL API format into the standard search format.

        # from is a reserved word so it cannot be used, use from_ instead
        if "from_" in params:
            params["from"] = params.pop("from_")

        path = _make_path(index, doc_type, "_search")
        eql_body = eql.format_request(body)
        if eql_body is not None:
            path = path.replace('/_search', '/_eql/search')
            body = eql_body
            if 'size' in params:
                body['size'] = int(params.pop('size'))
            if 'scroll' in params:
                params.pop('scroll')
            if '_source_includes' in params:
                params.pop('_source_includes')

        results = self.transport.perform_request(
            "POST",
            path,
            params=params,
            headers=headers,
            body=body,
        )

        eql.format_results(results);

        return results
