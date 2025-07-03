Rules
*****

Examples of several types of rule configuration can be found in the ``examples/rules`` folder.

.. _commonconfig:

.. note:: All "time" formats are of the form ``unit: X`` where unit is one of weeks, days, hours, minutes or seconds.
    Such as ``minutes: 15`` or ``hours: 1``.


Rule Configuration Cheat Sheet
==============================


+--------------------------------------------------------------------------+
|              FOR ALL RULES                                               |
+==============================================================+===========+
| ``es_host`` (string)                                         |  Required |
+--------------------------------------------------------------+           |
| ``es_port`` (number)                                         |           |
+--------------------------------------------------------------+           |
| ``index`` (string)                                           |           |
+--------------------------------------------------------------+           |
| ``type`` (string)                                            |           |
+--------------------------------------------------------------+           |
| ``alert`` (string or list)                                   |           |
+--------------------------------------------------------------+-----------+
| ``es_hosts`` (list, no default)                              |           |
+--------------------------------------------------------------+           |
| ``name`` (string, defaults to the filename)                  |           |
+--------------------------------------------------------------+           |
| ``use_strftime_index`` (boolean, default False)              |  Optional |
+--------------------------------------------------------------+           |
| ``use_ssl`` (boolean, default False)                         |           |
+--------------------------------------------------------------+           |
| ``verify_certs`` (boolean, default True)                     |           |
+--------------------------------------------------------------+           |
| ``ssl_show_warn`` (boolean, default True)                    |           |
+--------------------------------------------------------------+           |
| ``es_username`` (string, no default)                         |           |
+--------------------------------------------------------------+           |
| ``es_password`` (string, no default)                         |           |
+--------------------------------------------------------------+           |
| ``es_bearer`` (string, no default)                           |           |
+--------------------------------------------------------------+           |
| ``es_api_key`` (string, no default)                          |           |
+--------------------------------------------------------------+           |
| ``es_url_prefix`` (string, no default)                       |           |
+--------------------------------------------------------------+           |
| ``statsd_instance_tag`` (string, no default)                 |           |
+--------------------------------------------------------------+           |
| ``statsd_host`` (string, no default)                         |           |
+--------------------------------------------------------------+           |
| ``es_send_get_body_as`` (string, default "GET")              |           |
+--------------------------------------------------------------+           |
| ``aggregation`` (time, no default)                           |           |
+--------------------------------------------------------------+           |
| ``limit_execution`` (string, no default)                     |           |
+--------------------------------------------------------------+           |
| ``description`` (string, default empty string)               |           |
+--------------------------------------------------------------+           |
| ``kibana_url`` (string, default from es_host)                |           |
+--------------------------------------------------------------+           |
| ``kibana_username`` (string, no default)                     |           |
+--------------------------------------------------------------+           |
| ``kibana_password`` (string, no default)                     |           |
+--------------------------------------------------------------+           |
| ``kibana_verify_certs`` (boolean, default True)              |           |
+--------------------------------------------------------------+           |
| ``generate_kibana_discover_url`` (boolean, default False)    |           |
+--------------------------------------------------------------+           |
| ``shorten_kibana_discover_url`` (boolean, default False)     |           |
+--------------------------------------------------------------+           |
| ``kibana_discover_app_url`` (string, no default)             |           |
+--------------------------------------------------------------+           |
| ``kibana_discover_version`` (string, no default)             |           |
+--------------------------------------------------------------+           |
| ``kibana_discover_index_pattern_id`` (string, no default)    |           |
+--------------------------------------------------------------+           |
| ``kibana_discover_security_tenant``  (string, no default)    |           |
+--------------------------------------------------------------+           |
| ``kibana_discover_columns`` (list of strs, default _source)  |           |
+--------------------------------------------------------------+           |
| ``kibana_discover_from_timedelta`` (time, default: 10 min)   |           |
+--------------------------------------------------------------+           |
| ``kibana_discover_to_timedelta`` (time, default: 10 min)     |           |
+--------------------------------------------------------------+           |
| ``generate_opensearch_discover_url`` (boolean, default False)|           |
+--------------------------------------------------------------+           |
| ``opensearch_discover_app_url`` (string, no default)         |           |
+--------------------------------------------------------------+           |
| ``opensearch_discover_version`` (string, no default)         |           |
+--------------------------------------------------------------+           |
| ``opensearch_discover_index_pattern_id`` (string, no default)|           |
+--------------------------------------------------------------+           |
|``opensearch_discover_columns`` (list of strs,default _source)|           |
+--------------------------------------------------------------+           |
| ``opensearch_discover_from_timedelta`` (time,default: 10 min)|           |
+--------------------------------------------------------------+           |
| ``opensearch_discover_to_timedelta`` (time, default: 10 min) |           |
+--------------------------------------------------------------+           |
| ``use_local_time`` (boolean, default True)                   |           |
+--------------------------------------------------------------+           |
| ``realert`` (time, default: 1 min)                           |           |
+--------------------------------------------------------------+           |
| ``realert_key`` (string, defaults to the rule name)          |           |
+--------------------------------------------------------------+           |
| ``exponential_realert`` (time, no default)                   |           |
+--------------------------------------------------------------+           |
| ``match_enhancements`` (list of strs, no default)            |           |
+--------------------------------------------------------------+           |
| ``top_count_number`` (int, default 5)                        |           |
+--------------------------------------------------------------+           |
| ``top_count_keys`` (list of strs)                            |           |
+--------------------------------------------------------------+           |
| ``raw_count_keys`` (boolean, default True)                   |           |
+--------------------------------------------------------------+           |
| ``include`` (list of strs, default ["*"])                    |           |
+--------------------------------------------------------------+           |
| ``include_fields`` (list of strs, no default)                |           |
+--------------------------------------------------------------+           |
| ``include_rule_params_in_matches`` (list of strs, no default)|           |
+--------------------------------------------------------------+           |
| ``include_rule_params_in_first_match_only`` (boolean, False) |           |
+--------------------------------------------------------------+           |
| ``filter`` (ES filter DSL, no default)                       |           |
+--------------------------------------------------------------+           |
| ``max_query_size`` (int, default global max_query_size)      |           |
+--------------------------------------------------------------+           |
| ``query_delay`` (time, default 0 min)                        |           |
+--------------------------------------------------------------+           |
| ``owner`` (string, default empty string)                     |           |
+--------------------------------------------------------------+           |
| ``priority`` (int, default 2)                                |           |
+--------------------------------------------------------------+           |
| ``category`` (string, default empty string)                  |           |
+--------------------------------------------------------------+           |
| ``scan_entire_timeframe`` (bool, default False)              |           |
+--------------------------------------------------------------+           |
| ``query_timezone`` (string, default empty string)            |           |
+--------------------------------------------------------------+           |
| ``import`` (string)                                          |           |
|                                                              |           |
| IGNORED IF ``use_count_query`` or ``use_terms_query`` is true|           |
+--------------------------------------------------------------+           +
| ``buffer_time`` (time, default from config.yaml)             |           |
+--------------------------------------------------------------+           |
| ``timestamp_field`` (string, default "@timestamp")           |           |
+--------------------------------------------------------------+           |
| ``timestamp_type`` (string, default iso)                     |           |
+--------------------------------------------------------------+           |
| ``timestamp_format`` (string, default "%Y-%m-%dT%H:%M:%SZ")  |           |
+--------------------------------------------------------------+           |
| ``timestamp_format_expr`` (string, no default )              |           |
+--------------------------------------------------------------+           |
| ``timestamp_to_datetime_format_expr`` (string, no default )  |           |
+--------------------------------------------------------------+           |
| ``_source_enabled`` (boolean, default True)                  |           |
+--------------------------------------------------------------+           |
| ``alert_text_args`` (array of strs)                          |           |
+--------------------------------------------------------------+           |
| ``alert_text_kw`` (object)                                   |           |
+--------------------------------------------------------------+           |
| ``alert_missing_value`` (string, default "<MISSING VALUE>")  |           |
+--------------------------------------------------------------+           |
| ``is_enabled`` (boolean, default True)                       |           |
+--------------------------------------------------------------+-----------+
| ``search_extra_index`` (boolean, default False)              |           |
+--------------------------------------------------------------+-----------+

|

+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|      RULE TYPE                                        |   Any  | Blacklist | Whitelist | Change | Frequency | Spike | Flatline |New_term|Cardinality|Metric Aggregation|Spike Aggregation|Percentage Match|
+=======================================================+========+===========+===========+========+===========+=======+==========+========+===========+==================+=================+================+
| ``compare_key`` (list of strs, no default)            |        |    Req    |   Req     |  Req   |           |       |          |        |           |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``blacklist`` (list of strs, no default)               |        |    Req    |           |        |           |       |          |        |           |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``whitelist`` (list of strs, no default)               |        |           |   Req     |        |           |       |          |        |           |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
| ``ignore_null`` (boolean, default False)              |        |           |   Req     |  Req   |           |       |          |        |           |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
| ``query_key`` (string or list, no default)            |   Opt  |           |           |   Req  |    Opt    |  Opt  |   Opt    |  Req   |  Opt      |  Opt             |  Opt            |  Opt           |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
| ``aggregation_key`` (string, no default)              |   Opt  |           |           |        |           |       |          |        |           |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
| ``summary_table_fields`` (list, no default)           |   Opt  |           |           |        |           |       |          |        |           |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
| ``timeframe`` (time, no default)                      |        |           |           |   Opt  |    Req    |  Req  |   Req    |        |  Req      |                  |  Req            |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
| ``num_events`` (int, no default)                      |        |           |           |        |    Req    |       |          |        |           |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
| ``attach_related`` (boolean, default False)           |        |           |           |        |    Opt    |       |          |        |           |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``use_count_query`` (boolean, default False)           |        |           |           |        |     Opt   | Opt   | Opt      |        |           |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``use_terms_query`` (boolean, default False)           |        |           |           |        |     Opt   | Opt   |          | Opt    |           |                  |                 |                |
|                                                       |        |           |           |        |           |       |          |        |           |                  |                 |                |
|``query_key`` (string or list, no default)             |        |           |           |        |           |       |          |        |           |                  |                 |                |
|                                                       |        |           |           |        |           |       |          |        |           |                  |                 |                |
|``terms_size`` (int, default 50)                       |        |           |           |        |           |       |          |        |           |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
| ``spike_height`` (int, no default)                    |        |           |           |        |           |   Req |          |        |           |                  |  Req            |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``spike_type`` ([up|down|both], no default)            |        |           |           |        |           |   Req |          |        |           |                  |  Req            |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``alert_on_new_data`` (boolean, default False)         |        |           |           |        |           |   Opt |          |        |           |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``threshold_ref`` (int, no default)                    |        |           |           |        |           |   Opt |          |        |           |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``threshold_ref`` (number, no default)                 |        |           |           |        |           |       |          |        |           |                  |  Opt            |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``threshold_cur`` (int, no default)                    |        |           |           |        |           |   Opt |          |        |           |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``threshold_cur`` (number, no default)                 |        |           |           |        |           |       |          |        |           |                  |  Opt            |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``threshold`` (int, no default)                        |        |           |           |        |           |       |    Req   |        |           |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``fields`` (string or list, no default)                |        |           |           |        |           |       |          | Req    |           |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``terms_window_size`` (time, default 30 days)          |        |           |           |        |           |       |          | Opt    |           |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``window_step_size`` (time, default 1 day)             |        |           |           |        |           |       |          | Opt    |           |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``alert_on_missing_field`` (boolean, default False)    |        |           |           |        |           |       |          | Opt    |           |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``cardinality_field`` (string, no default)             |        |           |           |        |           |       |          |        |  Req      |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``max_cardinality`` (boolean, default False)           |        |           |           |        |           |       |          |        |  Opt      |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``min_cardinality`` (boolean, default False)           |        |           |           |        |           |       |          |        |  Opt      |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``metric_agg_key`` (string, no default)                |        |           |           |        |           |       |          |        |           |  Req             |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``metric_agg_type`` (no default,                       |        |           |           |        |           |       |          |        |           |  Req             |  Req            |                |
|                                                       |        |           |           |        |           |       |          |        |           |                  |                 |                |
|([min|max|avg|sum|cardinality|value_count|percentiles])|        |           |           |        |           |       |          |        |           |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``metric_agg_script`` (no default)                     |        |           |           |        |           |       |          |        |           |  Opt             |  Opt            |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``percentile_range`` ++required if percentiles is used |        |           |           |        |           |       |          |        |           |  Req++           |  Req++          |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``max_threshold`` (number, no default)                 |        |           |           |        |           |       |          |        |           |  Opt             |                 |                |
|                                                       |        |           |           |        |           |       |          |        |           |                  |                 |                |
|``min_threshold`` (number, no default)                 |        |           |           |        |           |       |          |        |           |                  |                 |                |
|                                                       |        |           |           |        |           |       |          |        |           |                  |                 |                |
|Requires at least one of the two options               |        |           |           |        |           |       |          |        |           |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``min_doc_count`` (int, default 1)                     |        |           |           |        |           |       |          |        |           |   Opt            |   Opt           |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``use_run_every_query_size`` (boolean, default False)  |        |           |           |        |           |       |          |        |           |   Opt            |                 |   Opt          |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``allow_buffer_time_overlap`` (boolean, default False) |        |           |           |        |           |       |          |        |           |   Opt            |                 |   Opt          |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``bucket_interval`` (time, no default)                 |        |           |           |        |           |       |          |        |           |   Opt            |                 |   Opt          |
|                                                       |        |           |           |        |           |       |          |        |           |                  |                 |                |
|``sync_bucket_interval`` (boolean, default False)      |        |           |           |        |           |       |          |        |           |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``metric_format_string`` (string, no default)          |        |           |           |        |           |       |          |        |           |   Opt            |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``match_bucket_filter`` (no default)                   |        |           |           |        |           |       |          |        |           |                  |                 |  Req           |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``min_percentage`` (number, no default)                |        |           |           |        |           |       |          |        |           |                  |                 |  Req           |
|                                                       |        |           |           |        |           |       |          |        |           |                  |                 |                |
|``max_percentage`` (number, no default)                |        |           |           |        |           |       |          |        |           |                  |                 |                |
|                                                       |        |           |           |        |           |       |          |        |           |                  |                 |                |
|Requires at least one of the two options               |        |           |           |        |           |       |          |        |           |                  |                 |                |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``percentage_format_string`` (string, no default)      |        |           |           |        |           |       |          |        |           |                  |                 |   Opt          |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+
|``min_denominator`` (int, default 0)                   |        |           |           |        |           |       |          |        |           |                  |                 |   Opt          |
+-------------------------------------------------------+--------+-----------+-----------+--------+-----------+-------+----------+--------+-----------+------------------+-----------------+----------------+

Common Configuration Options
============================

Every file that ends in ``.yaml`` in the ``rules_folder`` will be run by default.
The following configuration settings are common to all types of rules.

.. note::

  While the following are marked as *required*, if they are already defined in the global configuration 
  then those settings will be utilized. If desired, each rule can override the global settings.

Required Settings
~~~~~~~~~~~~~~~~~

es_host
^^^^^^^

``es_host``: The hostname of the Elasticsearch cluster the rule will use to query. (Required, string, no default)
The environment variable ``ES_HOST`` will override this field.
For multiple host Elasticsearch clusters see ``es_hosts`` parameter.

es_port
^^^^^^^

``es_port``: The port of the Elasticsearch cluster. (Required, number, no default)
The environment variable ``ES_PORT`` will override this field.

index
^^^^^

``index``: The name of the index that will be searched. Wildcards can be used here, such as:
``index: my-index-*`` which will match ``my-index-2014-10-05``. You can also use a format string containing
``%Y`` for year, ``%m`` for month, and ``%d`` for day. To use this, you must also set ``use_strftime_index`` to true. (Required, string, no default)

For example, Separate multiple indices with commas.::

    index: topbeat-*,packetbeat-*

name
^^^^

``name``: The name of the rule. This must be unique across all rules. The name will be used in
alerts and used as a key when writing and reading search metadata back from Elasticsearch. (Required, string, no default)

type
^^^^

``type``: The ``RuleType`` to use. This may either be one of the built in rule types, see :ref:`Rule Types <ruletypes>` section below for more information,
or loaded from a module. For loading from a module, the type should be specified as ``module.file.RuleName``. (Required, string, no default)

alert
^^^^^

``alert``: The ``Alerter`` type to use. This may be one or more of the built in alerts, see :ref:`Alert Types <alert_types>` section below for more information,
or loaded from a module. For loading from a module, the alert should be specified as ``module.file.AlertName``. (Required, string or list, no default)

Optional Settings
~~~~~~~~~~~~~~~~~
es_hosts
^^^^^^^^

``es_hosts``: The list of nodes of the Elasticsearch cluster that the rule will use for the request. (Optional, list, default none). Values can be specified as ``host:port`` if overriding the default port.
The environment variable ``ES_HOSTS`` will override this field, and can be specified as a comma-separated value. Note that the ``es_host`` parameter must still be specified in order to identify a primary Elasticsearch host. 

import
^^^^^^

``import``: If specified includes all the settings from this yaml file. This allows common config options to be shared. Note that imported files that aren't
complete rules should not have a ``.yml`` or ``.yaml`` suffix so that ElastAlert 2 doesn't treat them as rules. Filters in imported files are merged (ANDed)
with any filters in the rule. You can have one import per rule (value is string) or several imports per rule (value is a list of strings).
The imported file can import another file or multiple files, recursively.
The filename can be an absolute path or relative to the rules directory. (Optional, string or array of strings, no default)

use_ssl
^^^^^^^

``use_ssl``: Whether or not to connect to ``es_host`` using TLS. (Optional, boolean, default False)
The environment variable ``ES_USE_SSL`` will override this field.

ssl_show_warn
^^^^^^^^^^^^^

``ssl_show_warn``: Whether or not to show SSL/TLS warnings when ``verify_certs`` is disabled. (Optional, boolean, default True)

verify_certs
^^^^^^^^^^^^

``verify_certs``: Whether or not to verify TLS certificates. (Optional, boolean, default True)

client_cert
^^^^^^^^^^^

``client_cert``: Path to a PEM certificate to use as the client certificate (Optional, string, no default)

client_key
^^^^^^^^^^^

``client_key``: Path to a private key file to use as the client key (Optional, string, no default)

ca_certs
^^^^^^^^

``ca_certs``: Path to a CA cert bundle to use to verify SSL connections (Optional, string, no default)


disable_rules_on_error
^^^^^^^^^^^^^^^^^^^^^^

``disable_rules_on_error``: If true, ElastAlert 2 will disable rules which throw uncaught (not EAException) exceptions. It
will upload a traceback message to ``elastalert_metadata`` and if ``notify_email`` is set, send an email notification. The
rule will no longer be run until either ElastAlert 2 restarts or the rule file has been modified. This defaults to ``True``.

es_conn_timeout
^^^^^^^^^^^^^^^

``es_conn_timeout``: Optional; sets timeout for connecting to and reading from ``es_host``; defaults to ``20``.

es_username
^^^^^^^^^^^

``es_username``: basic-auth username for connecting to ``es_host``. (Optional, string, no default) The environment variable ``ES_USERNAME`` will override this field.

es_password
^^^^^^^^^^^

``es_password``: basic-auth password for connecting to ``es_host``. (Optional, string, no default) The environment variable ``ES_PASSWORD`` will override this field.

es_bearer
^^^^^^^^^^^

``es_bearer``: bearer-token authorization for connecting to ``es_host``. (Optional, string, no default) The environment variable ``ES_BEARER`` will override this field. This authentication option will override the password authentication option.

es_api_key
^^^^^^^^^^^

``es_api_key``: api-key-token authorization for connecting to ``es_host``. (Optional, base64 string, no default) The environment variable ``ES_API_KEY`` will override this field. This authentication option will override both the bearer and the password authentication options.

es_url_prefix
^^^^^^^^^^^^^

``es_url_prefix``: URL prefix for the Elasticsearch endpoint. (Optional, string, no default)

statsd_instance_tag
^^^^^^^^^^^^^^^^^^^

``statsd_instance_tag``: prefix for statsd metrics. (Optional, string, no default)


statsd_host
^^^^^^^^^^^^^

``statsd_host``: statsd host. (Optional, string, no default)

es_send_get_body_as
^^^^^^^^^^^^^^^^^^^

``es_send_get_body_as``: Method for querying Elasticsearch. (Optional, string, default "GET")

use_strftime_index
^^^^^^^^^^^^^^^^^^

``use_strftime_index``: If this is true, ElastAlert 2 will format the index using datetime.strftime for each query.
See https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior for more details.
If a query spans multiple days, the formatted indexes will be concatenated with commas. This is useful
as narrowing the number of indexes searched, compared to using a wildcard, may be significantly faster. For example, if ``index`` is
``logstash-%Y.%m.%d``, the query url will be similar to ``elasticsearch.example.com/logstash-2015.02.03/...`` or
``elasticsearch.example.com/logstash-2015.02.03,logstash-2015.02.04/...``.

search_extra_index
^^^^^^^^^^^^^^^^^^

``search_extra_index``: If this is true, ElastAlert 2 will add an extra index on the early side onto each search. For example, if it's querying
completely within 2018-06-28, it will actually use 2018-06-27,2018-06-28. This can be useful if your timestamp_field is not what's being used
to generate the index names. If that's the case, sometimes a query would not have been using the right index.

aggregation
^^^^^^^^^^^

``aggregation``: This option allows you to aggregate multiple matches together into one alert. Every time a match is found,
ElastAlert 2 will wait for the ``aggregation`` period, and send all of the matches that have occurred in that time for a particular
rule together.

For example::

    aggregation:
      hours: 2

means that if one match occurred at 12:00, another at 1:00, and a third at 2:30, one
alert would be sent at 2:00, containing the first two matches, and another at 4:30, containing the third match plus any additional matches
occurring before 4:30. This can be very useful if you expect a large number of matches and only want a periodic report. (Optional, time, default none)

If you wish to aggregate all your alerts and send them on a recurring interval, you can do that using the ``schedule`` field.

For example, if you wish to receive alerts every Monday and Friday::

    aggregation:
      schedule: '2 4 * * mon,fri'

This uses Cron syntax, which you can read more about `here <http://www.nncron.ru/help/EN/working/cron-format.htm>`_. Make sure to `only` include either a schedule field or standard datetime fields (such as ``hours``, ``minutes``, ``days``), not both.

By default, all events that occur during an aggregation window are grouped together. However, if your rule has the ``aggregation_key`` field set, then each event sharing a common key value will be grouped together. A separate aggregation window will be made for each newly encountered key value.

For example, if you wish to receive alerts that are grouped by the user who triggered the event, you can set::

    aggregation_key: 'my_data.username'

Then, assuming an aggregation window of 10 minutes, if you receive the following data points::

    {'my_data': {'username': 'alice', 'event_type': 'login'}, '@timestamp': '2016-09-20T00:00:00'}
    {'my_data': {'username': 'bob', 'event_type': 'something'}, '@timestamp': '2016-09-20T00:05:00'}
    {'my_data': {'username': 'alice', 'event_type': 'something else'}, '@timestamp': '2016-09-20T00:06:00'}

This should result in 2 alerts: One containing alice's two events, sent at ``2016-09-20T00:10:00`` and one containing bob's one event sent at ``2016-09-20T00:16:00``

For aggregations, there can sometimes be a large number of documents present in the viewing medium (email, Jira ticket, etc..). If you set the ``summary_table_fields`` field, ElastAlert 2 will provide a summary of the specified fields from all the results.

The formatting style of the summary table can be switched between ``ascii`` (default), ``markdown``, or ``html`` with parameter ``summary_table_type``.

The maximum number of rows in the summary table can be limited with the parameter ``summary_table_max_rows``.

For example, if you wish to summarize the usernames and event_types that appear in the documents so that you can see the most relevant fields at a quick glance, you can set::

    summary_table_fields:
        - my_data.username
        - my_data.event_type

Then, for the same sample data shown above listing alice and bob's events, ElastAlert 2 will provide the following summary table in the alert medium::

    +------------------+--------------------+
    | my_data.username | my_data.event_type |
    +------------------+--------------------+
    |      alice       |       login        |
    |       bob        |     something      |
    |      alice       |   something else   |
    +------------------+--------------------+


.. note::
   By default, aggregation time is relative to the current system time, not the time of the match. This means that running ElastAlert 2 over
   past events will result in different alerts than if ElastAlert 2 had been running while those events occured. This behavior can be changed
   by setting ``aggregate_by_match_time``.

limit_execution
^^^^^^^^^^^^^^^

``limit_execution``: This option allows you to activate the rule during a limited period of time. This uses the cron format.

For example, if you wish to activate the rule from monday to friday, between 10am to 6pm::

    limit_execution: "* 10-18 * * 1-5"

aggregate_by_match_time
^^^^^^^^^^^^^^^^^^^^^^^

Setting this to true will cause aggregations to be created relative to the timestamp of the first event, rather than the current time. This
is useful for querying over historic data or if using a very large buffer_time and you want multiple aggregations to occur from a single query.

aggregation_alert_time_compared_with_timestamp_field
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``aggregation_alert_time_compared_with_timestamp_field``: This option controls how aggregation works when a rule processes events
older than ``current time - aggregation window`` and ``aggregate_by_match_time`` is set to true. Defaults to false.
When false, the expected send timestamp of the pending alert (waiting for additional events to aggregate) is compared with the current time.
As a result, following events will not be aggregated with the pending alert, because it is considered already notified,
leading to past events being notified one by one instead of being grouped together.
When true, it allows the aggregation of events with old timestamps, as long as they are within the aggregation window.
(Optional, boolean, default false)

realert
^^^^^^^

``realert``: This option allows you to ignore repeating alerts for a period of time. If the rule uses a ``query_key``, this option
will be applied on a per key basis. All matches for a given rule, or for matches with the same ``query_key``, will be ignored for
the given time. All matches with a missing ``query_key`` will be grouped together using a value of ``_missing``.
This is applied to the time the alert is sent, not to the time of the event. It defaults to one minute, which means
that if ElastAlert 2 is run over a large time period which triggers many matches, only the first alert will be sent by default. If you want
every alert, set realert to 0 minutes. (Optional, time, default 1 minute)

realert_key
^^^^^^^^^^^

``realert_key``: This option allows you to customize the key for ``realert``.  The default is the rule name, but if you have multiple rules that
you would like to use the same key for you can set the ``realert_key`` to be the same in those rules. (Optional, string, default is the rule name)

exponential_realert
^^^^^^^^^^^^^^^^^^^

``exponential_realert``: This option causes the value of ``realert`` to exponentially increase while alerts continue to fire. If set,
the value of ``exponential_realert`` is the maximum ``realert`` will increase to. If the time between alerts is less than twice ``realert``,
``realert`` will double. For example, if ``realert: minutes: 10`` and ``exponential_realert: hours: 1``, an alerts fires at 1:00 and another
at 1:15, the next alert will not be until at least 1:35. If another alert fires between 1:35 and 2:15, ``realert`` will increase to the
1 hour maximum. If more than 2 hours elapse before the next alert, ``realert`` will go back down. Note that alerts that are ignored (e.g.
one that occurred at 1:05) would not change ``realert``. (Optional, time, no default)

buffer_time
^^^^^^^^^^^

``buffer_time``: This options allows the rule to override the ``buffer_time`` global setting defined in config.yaml. This value is ignored if
``use_count_query`` or ``use_terms_query`` is true. (Optional, time)

query_delay
^^^^^^^^^^^

``query_delay``: This option will cause ElastAlert 2 to subtract a time delta from every query, causing the rule to run with a delay.
This is useful if the data is Elasticsearch doesn't get indexed immediately. (Optional, time)

For example::

    query_delay:
      hours: 2

owner
^^^^^

``owner``: This value will be used to identify the stakeholder of the alert. Optionally, this field can be included in any alert type. (Optional, string)

priority
^^^^^^^^

``priority``: This value will be used to identify the relative priority of the alert. Optionally, this field can be included in any alert type (e.g. for use in email subject/body text). (Optional, int, default 2)

category
^^^^^^^^

``category``: This value will be used to identify the category of the alert. Optionally, this field can be included in any alert type (e.g. for use in email subject/body text). (Optional, string, default empty string)

max_query_size
^^^^^^^^^^^^^^

``max_query_size``: The maximum number of documents that will be downloaded from Elasticsearch in a single query. If you
expect a large number of results, consider using ``use_count_query`` for the rule. If this
limit is reached, a warning will be logged but ElastAlert 2 will continue without downloading more results. This setting will
override a global ``max_query_size``. (Optional, int, default value of global ``max_query_size``)

filter
^^^^^^

``filter``: A list of Elasticsearch query DSL filters that is used to query Elasticsearch. ElastAlert 2 will query Elasticsearch using the format
``{'filter': {'bool': {'must': [config.filter]}}}`` with an additional timestamp range filter.
All of the results of querying with these filters are passed to the ``RuleType`` for analysis.
For more information writing filters, see :ref:`Writing Filters <writingfilters>`. (Required, Elasticsearch query DSL, no default)

include
^^^^^^^

``include``: A list of terms that should be included in query results and passed to rule types and alerts. When set, only those
fields, along with '@timestamp', ``query_key``, ``compare_key``, and ``top_count_keys``  are included, if present.
(Optional, list of strings, default all fields)

include_fields
^^^^^^^^^^^^^^

``include_fields``: A list of fields that should be included in query results and passed to rule types and alerts. If ``_source_enabled`` is False,
only these fields and those from ``include`` are included.  When ``_source_enabled`` is True, these are in addition to source.  This is used
for runtime fields, script fields, etc.  This only works with Elasticsearch version 7.11 and newer.  (Optional, list of strings, no default)

include_rule_params_in_matches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``include_rule_params_in_matches``: This is an optional list of rule parameter names that will have their values copied from the rule into the match records prior to sending out alerts. This allows alerters to have access to specific data in the originating rule. The parameters will be keyed into the match with a ``rule_param_`` prefix. For example, if the ``name`` rule parameter is specified in this list, the match record will have access to the rule name via the ``rule_param_name`` field. Including parameters with complex types, such as maps (Dictionaries) or lists (Arrays) can cause problems if the alerter is unable to convert these into formats that it needs. For example, including the ``query_key`` list parameter in matches that use the http_post2 alerter can cause JSON serialization errors.

.. note::

    That this option can cause performance to degrade when a rule is triggered with many matching records since each match record will need to have the rule parameter data copied into it. See the ``include_rule_params_in_first_match_only`` boolean setting, which can mitigate this performance degradation. This performance degradation is more likely to occur with aggregated alerts.

Example::

    include_rule_params_in_matches:
    - name
    - some_custom_param

include_rule_params_in_first_match_only
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``include_rule_params_in_first_match_only``: When using the ``include_rule_params_in_matches`` setting mentioned above, optionally set to this setting to ``True`` to only copy the rule parameters into the first match record. This is primarily useful for aggregation rules that match hundreds or thousands of records during each run, and where only the first match is used in the alerter. The effectiveness of this setting is dependent upon which alerter(s) are being used. For example, using this setting with ``True`` in a rule that uses the http_post2 alerter will not be useful, since that alerter simply iterates across all matches and POSTs them to the HTTP URL. This would cause only the first POST to have the additional rule parameter values.

top_count_keys
^^^^^^^^^^^^^^

``top_count_keys``: A list of fields. ElastAlert 2 will perform a terms query for the top X most common values for each of the fields,
where X is 5 by default, or ``top_count_number`` if it exists.
For example, if ``num_events`` is 100, and ``top_count_keys`` is ``- "username"``, the alert will say how many of the 100 events
have each username, for the top 5 usernames. When this is computed, the time range used is from ``timeframe`` before the most recent event
to 10 minutes past the most recent event. Because ElastAlert 2 uses an aggregation query to compute this, it will attempt to use the
field name plus ".keyword" to count unanalyzed terms. To turn this off, set ``raw_count_keys`` to false.

top_count_number
^^^^^^^^^^^^^^^^

``top_count_number``: The number of terms to list if ``top_count_keys`` is set. (Optional, integer, default 5)

raw_count_keys
^^^^^^^^^^^^^^

``raw_count_keys``: If true, all fields in ``top_count_keys`` will have ``.keyword`` appended to them.  This used to be ".raw" in older Elasticsearch versions, but the setting name `raw_count_keys` was left as-is to avoid breaking existing installations. (Optional, boolean, default true)

description
^^^^^^^^^^^

``description``: text describing the purpose of rule. (Optional, string, default empty string)
Can be referenced in custom alerters to provide context as to why a rule might trigger.

kibana_url
^^^^^^^^^^

``kibana_url``: The base url of the Kibana application. If not specified, a URL will be constructed using ``es_host``
and ``es_port``.

This value will be used if ``generate_kibana_discover_url`` is true and ``kibana_discover_app_url`` is a relative path

(Optional, string, default ``http://<es_host>:<es_port>/_plugin/kibana/``)

kibana_username
^^^^^^^^^^^^^^^

``kibana_username``: The username used to make basic authenticated API requests against Kibana.
This value is only used if ``shorten_kibana_discover_url`` is true.

(Optional, string, no default)

kibana_password
^^^^^^^^^^^^^^^

``kibana_password``: The password used to make basic authenticated API requests against Kibana.
This value is only used if ``shorten_kibana_discover_url`` is true.

(Optional, string, no default)

kibana_verify_certs
^^^^^^^^^^^^^^^^^^^

``kibana_verify_certs``: Whether or not to verify TLS certificates when querying Kibana. (Optional, boolean, default True)

generate_kibana_discover_url
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``generate_kibana_discover_url``: Enables the generation of the ``kibana_discover_url`` variable for the Kibana Discover application.
This setting requires the following settings are also configured:

- ``kibana_discover_app_url``
- ``kibana_discover_version``
- ``kibana_discover_index_pattern_id``

``generate_kibana_discover_url: true``

Example kibana_discover_app_url only usage::

    generate_kibana_discover_url: true
    kibana_discover_app_url: "http://localhost:5601/app/discover#/"
    kibana_discover_index_pattern_id: "4babf380-c3b1-11eb-b616-1b59c2feec54"
    kibana_discover_version: "7.15"
    alert_text: '{}'
    alert_text_args: [ kibana_discover_url ]
    alert_text_type: alert_text_only

Example kibana_url + kibana_discover_app_url usage::

    generate_kibana_discover_url: true
    kibana_url: "http://localhost:5601/"
    kibana_discover_app_url: "app/discover#/"
    kibana_discover_index_pattern_id: "4babf380-c3b1-11eb-b616-1b59c2feec54"
    kibana_discover_version: "7.15"
    alert_text: '{}'
    alert_text_args: [ kibana_discover_url ]
    alert_text_type: alert_text_only

shorten_kibana_discover_url
^^^^^^^^^^^^^^^^^^^^^^^^^^^

``shorten_kibana_discover_url``: Enables the shortening of the generated Kibana Discover urls.
In order to use the Kibana Shorten URL REST API, the ``kibana_discover_app_url`` must be provided
as a relative url (e.g. app/discover?#/).

ElastAlert may need to authenticate with Kibana to invoke the Kibana Shorten URL REST API. The
supported authentication methods are:

- Basic authentication by specifying ``kibana_username`` and ``kibana_password``
- AWS authentication (if configured already for ElasticSearch)

(Optional, bool, false)

kibana_discover_app_url
^^^^^^^^^^^^^^^^^^^^^^^

``kibana_discover_app_url``: The url of the Kibana Discover application used to generate the ``kibana_discover_url`` variable.
This value can use `$VAR` and `${VAR}` references to expand environment variables.
This value should be relative to the base kibana url defined by ``kibana_url`` and will vary depending on your installation.

``kibana_discover_app_url: app/discover#/``

(Optional, string, no default)

kibana_discover_security_tenant
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``kibana_discover_security_tenant``: The Kibana security tenant to include in the generated
``kibana_discover_url`` variable.

(Optional, string, no default)

kibana_discover_version
^^^^^^^^^^^^^^^^^^^^^^^

``kibana_discover_version``: Older version of Kibana use an obsolete URL shortener API. If using a version between 7.0 and 7.15 you must specify that major and minor version here.

Note that ElastAlert 2 only supports Kibana version 7.0 or newer.

Example:

``kibana_discover_version: '7.15'``

kibana_discover_index_pattern_id
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``kibana_discover_index_pattern_id``: The id of the data view to link to in the Kibana Discover application.
These ids are usually generated and can be found in url of the ``Data Views`` page, or by exporting its saved object.

In this documentation all references of "index pattern" refer to the similarly named concept in Kibana 8+ called "data view".

Example export of an index pattern's saved object:

.. code-block:: text

    [
        {
            "_id": "4e97d188-8a45-4418-8a37-07ed69b4d34c",
            "_type": "index-pattern",
            "_source": { ... }
        }
    ]

You can modify an index pattern's id by exporting the saved object, modifying the ``_id`` field, and re-importing.

``kibana_discover_index_pattern_id: 4e97d188-8a45-4418-8a37-07ed69b4d34c``

kibana_discover_columns
^^^^^^^^^^^^^^^^^^^^^^^

``kibana_discover_columns``: The columns to display in the generated Kibana Discover application link.
Defaults to the ``_source`` column.

``kibana_discover_columns: [ timestamp, message ]``

kibana_discover_from_timedelta
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``kibana_discover_from_timedelta``:  The offset to the `from` time of the Kibana Discover link's time range.
The `from` time is calculated by subtracting this timedelta from the event time.  Defaults to 10 minutes.

``kibana_discover_from_timedelta: minutes: 2``

kibana_discover_to_timedelta
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``kibana_discover_to_timedelta``:  The offset to the `to` time of the Kibana Discover link's time range.
The `to` time is calculated by adding this timedelta to the event time.  Defaults to 10 minutes.

``kibana_discover_to_timedelta: minutes: 2``

opensearch_url
^^^^^^^^^^^^^^

``opensearch_url``: The base url of the opensearch application. If not specified, a URL will be constructed using ``es_host``
and ``es_port``.

This value will be used if ``generate_opensearch_discover_url`` is true and ``opensearch_discover_app_url`` is a relative path

(Optional, string, default ``http://<opensearch_host>:<opensearch_port>/_plugin/_dashboards/``)

generate_opensearch_discover_url
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``generate_opensearch_discover_url``: Enables the generation of the ``opensearch_discover_url`` variable for the Opensearch Discover application.
This setting requires the following settings are also configured:

- ``opensearch_discover_app_url``
- ``opensearch_discover_version``
- ``opensearch_discover_index_pattern_id``

``generate_opensearch_discover_url: true``

Example opensearch_discover_app_url only usage for opensearch::

    generate_opensearch_discover_url: true
    opensearch_discover_app_url: "http://localhost:5601/app/data-explorer/discover?security_tenant=Admin#"
    opensearch_discover_index_pattern_id: "4babf380-c3b1-11eb-b616-1b59c2feec54"
    opensearch_discover_version: "2.11"
    alert_text: '{}'
    alert_text_args: [ opensearch_discover_url ]
    alert_text_type: alert_text_only

Example opensearch_url + opensearch_discover_app_url usage for opensearch::

    generate_opensearch_discover_url: true
    opensearch_url: "http://localhost:5601/"
    opensearch_discover_app_url: "app/data-explorer/discover?security_tenant=Admin#"
    opensearch_discover_index_pattern_id: "4babf380-c3b1-11eb-b616-1b59c2feec54"
    opensearch_discover_version: "2.11"
    alert_text: '{}'
    alert_text_args: [ opensearch_discover_url ]
    alert_text_type: alert_text_only

opensearch_discover_app_url
^^^^^^^^^^^^^^^^^^^^^^^^^^^

``opensearch_discover_app_url``: The url of the opensearch Discover application used to generate the ``opensearch_discover_url`` variable.
This value can use `$VAR` and `${VAR}` references to expand environment variables.
This value should be relative to the base opensearch url defined by ``opensearch_url`` and will vary depending on your installation.

``opensearch_discover_app_url: app/discover#/``

(Optional, string, no default)

opensearch_discover_version
^^^^^^^^^^^^^^^^^^^^^^^^^^^

``opensearch_discover_version``: Specifies the version of the opensearch Discover application. Currently unused.

Note that ElastAlert 2 only supports Discover version 2.11 or newer.

Example:

``opensearch_discover_version: '2.11'``

opensearch_discover_index_pattern_id
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``opensearch_discover_index_pattern_id``: The id of the index pattern to link to in the opensearch Discover application.
These ids are usually generated and can be found in url of the index pattern management page, or by exporting its saved object.


Example export of an index pattern's saved object:

.. code-block:: text

    [
        {
            "_id": "4e97d188-8a45-4418-8a37-07ed69b4d34c",
            "_type": "index-pattern",
            "_source": { ... }
        }
    ]

You can modify an index pattern's id by exporting the saved object, modifying the ``_id`` field, and re-importing.

``opensearch_discover_index_pattern_id: 4e97d188-8a45-4418-8a37-07ed69b4d34c``

opensearch_discover_columns
^^^^^^^^^^^^^^^^^^^^^^^^^^^

``opensearch_discover_columns``: The columns to display in the generated opensearch Discover application link.
Defaults to the ``_source`` column.

``opensearch_discover_columns: [ timestamp, message ]``

opensearch_discover_from_timedelta
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``opensearch_discover_from_timedelta``:  The offset to the `from` time of the opensearch Discover link's time range.
The `from` time is calculated by subtracting this timedelta from the event time.  Defaults to 10 minutes.

``opensearch_discover_from_timedelta: minutes: 2``

opensearch_discover_to_timedelta
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``opensearch_discover_to_timedelta``:  The offset to the `to` time of the opensearch Discover link's time range.
The `to` time is calculated by adding this timedelta to the event time.  Defaults to 10 minutes.

``opensearch_discover_to_timedelta: minutes: 2``

use_local_time
^^^^^^^^^^^^^^

``use_local_time``: Whether to convert timestamps to the local time zone in alerts. If false, timestamps will
be converted to UTC, which is what ElastAlert 2 uses internally. (Optional, boolean, default true)

match_enhancements
^^^^^^^^^^^^^^^^^^

``match_enhancements``: A list of enhancement modules to use with this rule. An enhancement module is a subclass of enhancements.BaseEnhancement
that will be given the match dictionary and can modify it before it is passed to the alerter. The enhancements will be run after silence and realert
is calculated and in the case of aggregated alerts, right before the alert is sent. This can be changed by setting ``run_enhancements_first``.
The enhancements should be specified as
``module.file.EnhancementName``. See :ref:`Enhancements` for more information. (Optional, list of strings, no default)

run_enhancements_first
^^^^^^^^^^^^^^^^^^^^^^

``run_enhancements_first``: If set to true, enhancements will be run as soon as a match is found. This means that they can be changed
or dropped before affecting realert or being added to an aggregation. Silence stashes will still be created before the
enhancement runs, meaning even if a ``DropMatchException`` is raised, the rule will still be silenced. (Optional, boolean, default false)

query_key
^^^^^^^^^

``query_key``: Having a query key means that realert time will be counted separately for each unique value of ``query_key``. For rule types which
count documents, such as spike, frequency and flatline, it also means that these counts will be independent for each unique value of ``query_key``.
For example, if ``query_key`` is set to ``username`` and ``realert`` is set, and an alert triggers on a document with ``{'username': 'bob'}``,
additional alerts for ``{'username': 'bob'}`` will be ignored while other usernames will trigger alerts. Documents which are missing the
``query_key`` will be grouped together. A list of fields may also be used, which will create a compound query key. This compound key is
treated as if it were a single field whose value is the component values, or "None", joined by commas. A new field with the key
"field1,field2,etc" will be created in each document and may conflict with existing fields of the same name.

aggregation_key
^^^^^^^^^^^^^^^

``aggregation_key``: Having an aggregation key in conjunction with an aggregation will make it so that each new value encountered for the aggregation_key field will result in a new, separate aggregation window.

summary_table_fields
^^^^^^^^^^^^^^^^^^^^

``summary_table_fields``: Specifying the summmary_table_fields in conjunction with an aggregation will make it so that each aggregated alert will contain a table summarizing the values for the specified fields in all the matches that were aggregated together.

summary_table_type
^^^^^^^^^^^^^^^^^^^^

``summary_table_type``: One of: ``ascii`` or ``markdown`` or ``html``. Select the table type to use for the aggregation summary. Defaults to ``ascii`` for the classical text based table.

summary_table_max_rows
^^^^^^^^^^^^^^^^^^^^^^

``summary_table_max_rows``: Limit the maximum number of rows that will be shown in the summary table.

summary_prefix
^^^^^^^^^^^^^^^^^^^^

``summary_prefix``: Specify a prefix string, which will be added in front of the aggregation summary table. This string is currently not subject to any formatting.

summary_suffix
^^^^^^^^^^^^^^^^^^^^

``summary_suffix``: Specify a suffix string, which will be added after the aggregation summary table. This string is currently not subject to any formatting.

timestamp_field
^^^^^^^^^^^^^^^

``timestamp_field``: Specify the name of the document field containing the timestamp. 
By default, the field ``@timestamp`` is used to query Elasticsearch. 
If ``timestamp_field`` is set, this date field will be considered whenever querying, filtering and aggregating based on timestamps.
(Optional, string, default @timestamp).

timestamp_type
^^^^^^^^^^^^^^

``timestamp_type``: One of ``iso``, ``unix``, ``unix_ms``, ``custom``. This option will set the type of ``@timestamp`` (or ``timestamp_field``)
used to query Elasticsearch. ``iso`` will use ISO8601 timestamps, which will work with most Elasticsearch date type field. ``unix`` will
query using an integer unix (seconds since 1/1/1970) timestamp. ``unix_ms`` will use milliseconds unix timestamp. ``custom`` allows you to define
your own ``timestamp_format``. The default is ``iso``.
(Optional, string enum, default iso).

timestamp_format
^^^^^^^^^^^^^^^^

``timestamp_format``: In case Elasticsearch used custom date format for date type field, this option provides a way to define custom timestamp
format to match the type used for Elastisearch date type field. This option is only valid if ``timestamp_type`` set to ``custom``.
(Optional, string, default '%Y-%m-%dT%H:%M:%SZ').

timestamp_format_expr
^^^^^^^^^^^^^^^^^^^^^

``timestamp_format_expr``: In case Elasticsearch used custom date format for date type field, this option provides a way to adapt the
value obtained converting a datetime through ``timestamp_format``, when the format cannot match perfectly what defined in Elasticsearch.
When set, this option is evaluated as a Python expression along with a *globals* dictionary containing the original datetime instance
named ``dt`` and the timestamp to be refined, named ``ts``. The returned value becomes the timestamp obtained from the datetime.
For example, when the date type field in Elasticsearch uses milliseconds (``yyyy-MM-dd'T'HH:mm:ss.SSS'Z'``) and ``timestamp_format``
option is ``'%Y-%m-%dT%H:%M:%S.%fZ'``, Elasticsearch would fail to parse query terms as they contain microsecond values - that is
it gets 6 digits instead of 3 - since the ``%f`` placeholder stands for microseconds for Python *strftime* method calls.
Setting ``timestamp_format_expr: 'ts[:23] + ts[26:]'`` will truncate the value to milliseconds granting Elasticsearch compatibility.
This option is only valid if ``timestamp_type`` set to ``custom``.
(Optional, string, no default).

timestamp_to_datetime_format_expr
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``timestamp_to_datetime_format_expr``: In the same spirit as timestamp_format_expr, in case Elasticsearch used custom date format for date type field,
this option provides a way to adapt the value (as a string) returned by an Elasticsearch query before converting it into a datetime used by elastalert.
The changes are applied before converting the timestamp string to a datetime using ``timestamp_format``. This is useful when the format cannot match perfectly what is returned by Elasticsearch. When set, this option is evaluated as a Python expression along with a *globals* dictionary containing the original timestamp to be refined (as a string) named ``ts``. The returned value will be parse into a python datetime using the previously defined format (or using the default '%Y-%m-%dT%H:%M:%SZ').

For example, when the date type field returned by Elasticsearch uses nanoseconds (``yyyy-MM-dd'T'HH:mm:ss.SSS.XXXXXX``) and ``timestamp_format``
option is ``'%Y-%m-%dT%H:%M:%S.%f'`` (ns are not supported in python datetime.datetime.strptime), Elasticsearch would fail to parse the timestamp terms as they contain nanoseconds values - that is it gets 3 additional digits that can't be parsed, throwing the exception``ValueError: unconverted data remains: XXX``. Setting ``timestamp_to_datetime_format_expr: 'ts[:23]'`` will truncate the value to milliseconds, allowing a good conversion in a datetime object. This option is only valid if ``timestamp_type`` set to ``custom``. 
(Optional, string, no default).

_source_enabled
^^^^^^^^^^^^^^^

``_source_enabled``: If true, ElastAlert 2 will use _source to retrieve fields from documents in Elasticsearch. If false,
ElastAlert 2 will use ``fields`` to retrieve stored fields. Both of these are represented internally as if they came from ``_source``.
See https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-fields.html for more details. The fields used come from ``include``,
see above for more details. (Optional, boolean, default True)

scan_entire_timeframe
^^^^^^^^^^^^^^^^^^^^^

``scan_entire_timeframe``: If true, when ElastAlert 2 starts, it will always start querying at the current time minus the timeframe.
``timeframe`` must exist in the rule. This may be useful, for example, if you are using a flatline rule type with a large timeframe,
and you want to be sure that if ElastAlert 2 restarts, you can still get alerts. This may cause duplicate alerts for some rule types,
for example, Frequency can alert multiple times in a single timeframe, and if ElastAlert 2 were to restart with this setting, it may
scan the same range again, triggering duplicate alerts.

Some rules and alerts require additional options, which also go in the top level of the rule configuration file.

query_timezone
^^^^^^^^^^^^^^

``query_timezone``: Whether to convert UTC time to the specified time zone in rule queries.
If not set, start and end time of query will be used UTC. (Optional, string, default empty string)

Example value : query_timezone: "Europe/Istanbul"

.. _testing :

Testing Your Rule
=================

Once you've written a rule configuration, you will want to validate it. To do so, you can either run ElastAlert 2 in debug mode,
or use ``elastalert-test-rule``, which is a script that makes various aspects of testing easier.

It can:

- Check that the configuration file loaded successfully.

- Check that the Elasticsearch filter parses.

- Run against the last X day(s) and the show the number of hits that match your filter.

- Show the available terms in one of the results.

- Save documents returned to a JSON file.

- Run ElastAlert 2 using either a JSON file or actual results from Elasticsearch.

- Print out debug alerts or trigger real alerts.

- Check that, if they exist, the primary_key, compare_key and include terms are in the results.

- Show what metadata documents would be written to ``elastalert_status``.

Without any optional arguments, it will run ElastAlert 2 over the last 24 hours and print out any alerts that would have occurred.
Here is an example test run which triggered an alert:

.. code-block:: console

    $ elastalert-test-rule my_rules/rule1.yaml
    Successfully Loaded Example rule1

    Got 105 hits from the last 1 day

    Available terms in first hit:
        @timestamp
        field1
        field2
        ...
    Included term this_field_doesnt_exist may be missing or null

    INFO:root:Queried rule Example rule1 from 6-16 15:21 PDT to 6-17 15:21 PDT: 105 hits
    INFO:root:Alert for Example rule1 at 2015-06-16T23:53:12Z:
    INFO:root:Example rule1

    At least 50 events occurred between 6-16 18:30 PDT and 6-16 20:30 PDT

    field1:
    value1: 25
    value2: 25

    @timestamp: 2015-06-16T20:30:04-07:00
    field1: value1
    field2: something


    Would have written the following documents to elastalert_status:

    silence - {'rule_name': 'Example rule1', '@timestamp': datetime.datetime( ... ), 'exponent': 0, 'until':
    datetime.datetime( ... )}

    elastalert_status - {'hits': 105, 'matches': 1, '@timestamp': datetime.datetime( ... ), 'rule_name': 'Example rule1',
    'starttime': datetime.datetime( ... ), 'endtime': datetime.datetime( ... ), 'time_taken': 3.1415926}

Note that Docker users can also run the test tool:

.. code-block:: console

    $ docker run --rm -it --net es_default \
        -v $(pwd)/elastalert.yaml:/opt/elastalert/config.yaml \
        -v $(pwd)/rules:/opt/elastalert/rules \
        --entrypoint elastalert-test-rule \
        jertel/elastalert2 \
        /opt/elastalert/rules/example_frequency.yaml

If you want to specify an alternate configuration file to use, you can add the config flag prior to the rule filename::

    --config <path-to-config-file> 

The configuration preferences will be loaded as follows:
    1. Configurations specified in the yaml file.
    2. Configurations specified in the config file, if specified.
    3. Default configurations, for the tool to run.

Note that everything between "Alert for Example rule1 at ..." and "Would have written the following ..." is the exact text body that an alert would have.
See the section below on alert content for more details.
Also note that datetime objects are converted to ISO8601 timestamps when uploaded to Elasticsearch. See :ref:`the section on metadata <metadata>` for more details.

Other options include:

``--schema-only``: Only perform schema validation on the file. It will not load modules or query Elasticsearch. This may catch invalid YAML
and missing or misconfigured fields.

``--count-only``: Only find the number of matching documents and list available fields. ElastAlert 2 will not be run and documents will not be downloaded.

``--days N``: Instead of the default 1 day, query N days. For selecting more specific time ranges, use ``--start``
and ``--end``.

``--start <timestamp>`` The starting date/time of the search filter's time range. The timestamp is formatted as
``YYYY-MM-DDTHH:MM:SS`` (UTC) or with timezone ``YYYY-MM-DDTHH:MM:SS-XX:00``
(UTC-XX). If ``timeframe`` is specified, defaults to the ending time - timeframe. Otherwise defaults to ending time - 1 day.

``--end <timestamp>`` The ending date/time of the search filter's time range. The timestamp is formatted as
``YYYY-MM-DDTHH:MM:SS`` (UTC) or with timezone ``YYYY-MM-DDTHH:MM:SS-XX:00``
(UTC-XX). Defaults to the current time.

``--save-json FILE``: Save all documents downloaded to a file as JSON. This is useful if you wish to modify data while testing or do offline
testing in conjunction with ``--data FILE``. A maximum of 10,000 documents will be downloaded.

``--data FILE``: Use a JSON file as a data source instead of Elasticsearch. The file should be a single list containing objects,
rather than objects on separate lines. Note than this uses mock functions which mimic some Elasticsearch query methods and is not
guaranteed to have the exact same results as with Elasticsearch. For example, analyzed string fields may behave differently.

``--alert``: Trigger real alerts instead of the debug (logging text) alert.

``--formatted-output``: Output results in formatted JSON.

.. note::
   Results from running this script may not always be the same as if an actual ElastAlert 2 instance was running. Some rule types, such as spike
   and flatline require a minimum elapsed time before they begin alerting, based on their timeframe. In addition, use_count_query and
   use_terms_query rely on run_every to determine their resolution. This script uses a fixed 5 minute window, which is the same as the default.

   Also, EQL filters do not support counts, so the output relating to counts may show N/A (Not Applicable).


.. _ruletypes:

Rule Types
==========

The various ``RuleType`` classes, defined in ``elastalert/ruletypes.py``, form the main logic behind ElastAlert 2. An instance
is held in memory for each rule, passed all of the data returned by querying Elasticsearch with a given filter, and generates
matches based on that data.

To select a rule type, set the ``type`` option to the name of the rule type in the rule configuration file:

``type: <rule type>``

Any
~~~

``any``: The any rule will match everything. Every hit that the query returns will generate an alert.

Blacklist
~~~~~~~~~

``blacklist``: The blacklist rule will check a certain field against a blacklist, and match if it is in the blacklist.

This rule requires two additional options:

``compare_key``: The name of the field to use to compare to the blacklist. If the field is null, those events will be ignored.

``blacklist``: A list of blacklisted values, and/or a list of paths to flat files which contain the blacklisted values using ``- "!file /path/to/file"``; for example::

    blacklist:
        - value1
        - value2
        - "!file /tmp/blacklist1.txt"
        - "!file /tmp/blacklist2.txt"

It is possible to mix between blacklist value definitions, or use either one. The ``compare_key`` term must be equal to one of these values for it to match.

Whitelist
~~~~~~~~~

``whitelist``: Similar to ``blacklist``, this rule will compare a certain field to a whitelist, and match if the list does not contain
the term.

This rule requires three additional options:

``compare_key``: The name of the field to use to compare to the whitelist.

``ignore_null``: If true, events without a ``compare_key`` field will not match.

``whitelist``: A list of whitelisted values, and/or a list of paths to flat files which contain the whitelisted values using  ``- "!file /path/to/file"``; for example::

    whitelist:
        - value1
        - value2
        - "!file /tmp/whitelist1.txt"
        - "!file /tmp/whitelist2.txt"

It is possible to mix between whitelisted value definitions, or use either one. The ``compare_key`` term must be in this list or else it will match.

Change
~~~~~~

For an example configuration file using this rule type, look at ``examples/rules/example_change.yaml``.

``change``: This rule will monitor a certain field and match if that field changes. The field
must change with respect to the last event with the same ``query_key``.

This rule requires three additional options:

``compare_key``: The names of the field to monitor for changes. Since this is a list of strings, we can
have multiple keys. An alert will trigger if any of the fields change.

``ignore_null``: If true, events without a ``compare_key`` field will not count as changed. Currently this checks for all the fields in ``compare_key``

``query_key``: This rule is applied on a per-``query_key`` basis. This field must be present in all of
the events that are checked.

There is also an optional field:

``timeframe``: The maximum time between changes. After this time period, ElastAlert 2 will forget the old value
of the ``compare_key`` field.

Frequency
~~~~~~~~~

For an example configuration file using this rule type, look at ``examples/rules/example_frequency.yaml``.

``frequency``: This rule matches when there are at least a certain number of events in a given time frame. This
may be counted on a per-``query_key`` basis.

This rule requires two additional options:

``num_events``: The number of events which will trigger an alert, inclusive.

``timeframe``: The time that ``num_events`` must occur within.

Optional:

``use_count_query``: If true, ElastAlert 2 will poll Elasticsearch using the count api, and not download all of the matching documents. This is
useful is you care only about numbers and not the actual data. It should also be used if you expect a large number of query hits, in the order
of tens of thousands or more.

``use_terms_query``: If true, ElastAlert 2 will make an aggregation query against Elasticsearch to get counts of documents matching
each unique value of ``query_key``. This must be used with ``query_key``. This will only return a maximum of ``terms_size``,
default 50, unique terms.

``terms_size``: When used with ``use_terms_query``, this is the maximum number of terms returned per query. Default is 50.

``query_key``: Counts of documents will be stored independently for each value of ``query_key``. Only ``num_events`` documents,
all with the same value of ``query_key``, will trigger an alert.


``attach_related``: Will attach all the related events to the event that triggered the frequency alert. For example in an alert triggered with ``num_events``: 3,
the 3rd event will trigger the alert on itself and add the other 2 events in a key named ``related_events`` that can be accessed in the alerter.

Spike
~~~~~

``spike``: This rule matches when the volume of events during a given time period is ``spike_height`` times larger or smaller
than during the previous time period. It uses two sliding windows to compare the current and reference frequency
of events. We will call this two windows "reference" and "current".

This rule requires three additional options:

``spike_height``: The ratio of number of events in the last ``timeframe`` to the previous ``timeframe`` that when hit
will trigger an alert.

``spike_type``: Either 'up', 'down' or 'both'. 'Up' meaning the rule will only match when the number of events is ``spike_height`` times
higher. 'Down' meaning the reference number is ``spike_height`` higher than the current number. 'Both' will match either.

``timeframe``: The rule will average out the rate of events over this time period. For example, ``hours: 1`` means that the 'current'
window will span from present to one hour ago, and the 'reference' window will span from one hour ago to two hours ago. The rule
will not be active until the time elapsed from the first event is at least two timeframes. This is to prevent an alert being triggered
before a baseline rate has been established. This can be overridden using ``alert_on_new_data``, provided the rule uses the ``query_key`` 
property (see more information on this below).


Optional:

``field_value``: When set, uses the value of the field in the document and not the number of matching documents.
This is useful to monitor for example a temperature sensor and raise an alarm if the temperature grows too fast.
Note that the means of the field on the reference and current windows are used to determine if the ``spike_height`` value is reached.
Note also that the threshold parameters are ignored in this mode.


``threshold_ref``: The minimum number of events that must exist in the reference window for an alert to trigger. For example, if
``spike_height: 3`` and ``threshold_ref: 10``, then the 'reference' window must contain at least 10 events and the 'current' window at
least three times that for an alert to be triggered.

``threshold_cur``: The minimum number of events that must exist in the current window for an alert to trigger. For example, if
``spike_height: 3`` and ``threshold_cur: 60``, then an alert will occur if the current window has more than 60 events and
the reference window has less than a third as many.

To illustrate the use of ``threshold_ref``, ``threshold_cur``, ``alert_on_new_data``, ``timeframe`` and ``spike_height`` together,
consider the following examples::

    " Alert if at least 15 events occur within two hours and less than a quarter of that number occurred within the previous two hours. "
    timeframe: hours: 2
    spike_height: 4
    spike_type: up
    threshold_cur: 15

    hour1: 5 events (ref: 0, cur: 5) - No alert because (a) threshold_cur not met, (b) ref window not filled
    hour2: 5 events (ref: 0, cur: 10) - No alert because (a) threshold_cur not met, (b) ref window not filled
    hour3: 10 events (ref: 5, cur: 15) - No alert because (a) spike_height not met, (b) ref window not filled
    hour4: 35 events (ref: 10, cur: 45) - Alert because (a) spike_height met, (b) threshold_cur met, (c) ref window filled

    hour1: 20 events (ref: 0, cur: 20) - No alert because ref window not filled
    hour2: 21 events (ref: 0, cur: 41) - No alert because ref window not filled
    hour3: 19 events (ref: 20, cur: 40) - No alert because (a) spike_height not met, (b) ref window not filled
    hour4: 23 events (ref: 41, cur: 42) - No alert because spike_height not met

    hour1: 10 events (ref: 0, cur: 10) - No alert because (a) threshold_cur not met, (b) ref window not filled
    hour2: 0 events (ref: 0, cur: 10) - No alert because (a) threshold_cur not met, (b) ref window not filled
    hour3: 0 events (ref: 10, cur: 0) - No alert because (a) threshold_cur not met, (b) ref window not filled, (c) spike_height not met
    hour4: 30 events (ref: 10, cur: 30) - No alert because spike_height not met
    hour5: 5 events (ref: 0, cur: 35) - Alert because (a) spike_height met, (b) threshold_cur met, (c) ref window filled

    " Alert if at least 5 events occur within two hours, and twice as many events occur within the next two hours. "
    timeframe: hours: 2
    spike_height: 2
    spike_type: up
    threshold_ref: 5

    hour1: 20 events (ref: 0, cur: 20) - No alert because (a) threshold_ref not met, (b) ref window not filled
    hour2: 100 events (ref: 0, cur: 120) - No alert because (a) threshold_ref not met, (b) ref window not filled
    hour3: 100 events (ref: 20, cur: 200) - No alert because ref window not filled
    hour4: 100 events (ref: 120, cur: 200) - No alert because spike_height not met

    hour1: 0 events (ref: 0, cur: 0) - No alert because (a) threshold_ref not met, (b) ref window not filled
    hour2: 20 events (ref: 0, cur: 20) - No alert because (a) threshold_ref not met, (b) ref window not filled
    hour3: 100 events (ref: 0, cur: 120) - No alert because (a) threshold_ref not met, (b) ref window not filled
    hour4: 100 events (ref: 20, cur: 200) - Alert because (a) spike_height met, (b) threshold_ref met, (c) ref window filled

    hour1: 1 events (ref: 0, cur: 1) - No alert because (a) threshold_ref not met, (b) ref window not filled
    hour2: 2 events (ref: 0, cur: 3) - No alert because (a) threshold_ref not met, (b) ref window not filled
    hour3: 2 events (ref: 1, cur: 4) - No alert because (a) threshold_ref not met, (b) ref window not filled
    hour4: 1000 events (ref: 3, cur: 1002) - No alert because threshold_ref not met
    hour5: 2 events (ref: 4, cur: 1002) - No alert because threshold_ref not met
    hour6: 4 events: (ref: 1002, cur: 6) - No alert because spike_height not met

    hour1: 1000 events (ref: 0, cur: 1000) - No alert because (a) threshold_ref not met, (b) ref window not filled
    hour2: 0 events (ref: 0, cur: 1000) - No alert because (a) threshold_ref not met, (b) ref window not filled
    hour3: 0 events (ref: 1000, cur: 0) - No alert because (a) spike_height not met, (b) ref window not filled
    hour4: 0 events (ref: 1000, cur: 0) - No alert because spike_height not met
    hour5: 1000 events (ref: 0, cur: 1000) - No alert because threshold_ref not met
    hour6: 1050 events (ref: 0, cur: 2050)- No alert because threshold_ref not met
    hour7: 1075 events (ref: 1000, cur: 2125) Alert because (a) spike_height met, (b) threshold_ref met, (c) ref window filled

    " Alert if at least 100 events occur within two hours and less than a fifth of that number occurred in the previous two hours. "
    timeframe: hours: 2
    spike_height: 5
    spike_type: up
    threshold_cur: 100

    hour1: 1000 events (ref: 0, cur: 1000) - No alert because ref window not filled

    hour1: 2 events (ref: 0, cur: 2) - No alert because (a) threshold_cur not met, (b) ref window not filled
    hour2: 1 events (ref: 0, cur: 3) - No alert because (a) threshold_cur not met, (b) ref window not filled
    hour3: 20 events (ref: 2, cur: 21) - No alert because (a) threshold_cur not met, (b) ref window not filled
    hour4: 81 events (ref: 3, cur: 101) - Alert because (a) spike_height met, (b) threshold_cur met, (c) ref window filled

    hour1: 10 events (ref: 0, cur: 10) - No alert because (a) threshold_cur not met, (b) ref window not filled
    hour2: 20 events (ref: 0, cur: 30) - No alert because (a) threshold_cur not met, (b) ref window not filled
    hour3: 40 events (ref: 10, cur: 60) - No alert because (a) threshold_cur not met, (b) ref window not filled
    hour4: 80 events (ref: 30, cur: 120) - No alert because spike_height not met
    hour5: 200 events (ref: 60, cur: 280) - No alert because spike_height not met

``alert_on_new_data``: This option is only used if ``query_key`` is set. When this is set to true, any new ``query_key`` encountered may
trigger an immediate alert. When set to false, baseline must be established for each new ``query_key`` value, and then subsequent spikes may
cause alerts. Baseline is established after ``timeframe`` has elapsed twice since first occurrence.

``use_count_query``: If true, ElastAlert 2 will poll Elasticsearch using the count api, and not download all of the matching documents. This is
useful is you care only about numbers and not the actual data. It should also be used if you expect a large number of query hits, in the order
of tens of thousands or more. 

``use_terms_query``: If true, ElastAlert 2 will make an aggregation query against Elasticsearch to get counts of documents matching
each unique value of ``query_key``. This must be used with ``query_key``. This will only return a maximum of ``terms_size``,
default 50, unique terms.

``terms_size``: When used with ``use_terms_query``, this is the maximum number of terms returned per query. Default is 50.

``query_key``: Counts of documents will be stored independently for each value of ``query_key``.

.. note::

  Matches of the rule type ``spike`` contain two additional fields: ``spike_count`` contains the number of events that occurred during the
  current timeframe. ``reference_count`` contains the number of events that occurred during the reference timeframe.

Flatline
~~~~~~~~

``flatline``: This rule matches when the total number of events is under a given ``threshold`` for a time period.

This rule requires two additional options:

``threshold``: The minimum number of events for an alert not to be triggered.

``timeframe``: The time period that must contain less than ``threshold`` events.

Optional:

``use_count_query``: If true, ElastAlert 2 will poll Elasticsearch using the count api, and not download all of the matching documents. This is
useful is you care only about numbers and not the actual data. It should also be used if you expect a large number of query hits, in the order
of tens of thousands or more.

``use_terms_query``: If true, ElastAlert 2 will make an aggregation query against Elasticsearch to get counts of documents matching
each unique value of ``query_key``. This must be used with ``query_key``. This will only return a maximum of ``terms_size``,
default 50, unique terms.

``terms_size``: When used with ``use_terms_query``, this is the maximum number of terms returned per query. Default is 50.

``query_key``: With flatline rule, ``query_key`` means that an alert will be triggered if any value of ``query_key`` has been seen at least once
and then falls below the threshold. To reference the query_key value within a flatline alert message, use ``key`` as the field name.

``forget_keys``: Only valid when used with ``query_key``. If this is set to true, ElastAlert 2 will "forget" about the ``query_key`` value that
triggers an alert, therefore preventing any more alerts for it until it's seen again.

New Term
~~~~~~~~

``new_term``: This rule matches when a new value appears in a field that has never been seen before. When ElastAlert 2 starts, it will
use an aggregation query to gather all known terms for a list of fields.

This rule requires one additional option:

``fields``: A list of fields to monitor for new terms. ``query_key`` will be used if ``fields`` is not set. Each entry in the
list of fields can itself be a list.  If a field entry is provided as a list, it will be interpreted as a set of fields
that compose a composite key used for the ElasticSearch query.

.. note::

   The composite fields may only refer to primitive types, otherwise the initial ElasticSearch query will not properly return
   the aggregation results, thus causing alerts to fire every time the ElastAlert 2 service initially launches with the rule.
   A warning will be logged to the console if this scenario is encountered. However, future alerts will actually work as
   expected after the initial flurry.

Optional:

``terms_window_size``: The amount of time used for the initial query to find existing terms. No term that has occurred within this time frame
will trigger an alert. The default is 30 days.

``window_step_size``: When querying for existing terms, split up the time range into steps of this size. For example, using the default
30 day window size, and the default 1 day step size, 30 invidivdual queries will be made. This helps to avoid timeouts for very
expensive aggregation queries. The default is 1 day.

``alert_on_missing_field``: Whether or not to alert when a field is missing from a document. The default is false.

``use_terms_query``: If true, ElastAlert 2 will use aggregation queries to get terms instead of regular search queries. This is faster
than regular searching if there is a large number of documents. If this is used, you may only specify a single field, and must also set
``query_key`` to that field. Also, note that ``terms_size`` (the number of buckets returned per query) defaults to 50. This means
that if a new term appears but there are at least 50 terms which appear more frequently, it will not be found.

.. note::

  When using use_terms_query, make sure that the field you are using is not analyzed. If it is, the results of each terms
  query may return tokens rather than full values. ElastAlert 2 will by default turn on use_keyword_postfix, which attempts
  to use the non-analyzed version (.keyword) to gather initial terms. These will not match the partial values and
  result in false positives.

``use_keyword_postfix``: If true, ElastAlert 2 will automatically try to add .keyword to the fields when making an
initial query. These are non-analyzed fields added by Logstash. If the field used is analyzed, the initial query will return
only the tokenized values, potentially causing false positives. Defaults to true.

Cardinality
~~~~~~~~~~~

``cardinality``: This rule matches when a the total number of unique values for a certain field within a time frame is higher or lower
than a threshold.

This rule requires:

``timeframe``: The time period in which the number of unique values will be counted.

``cardinality_field``: Which field to count the cardinality for.

This rule requires one of the two following options:

``max_cardinality``: If the cardinality of the data is greater than this number, an alert will be triggered. Each new event that
raises the cardinality will trigger an alert.

``min_cardinality``: If the cardinality of the data is lower than this number, an alert will be triggered. The ``timeframe`` must
have elapsed since the first event before any alerts will be sent. When a match occurs, the ``timeframe`` will be reset and must elapse
again before additional alerts.

Optional:

``query_key``: Group cardinality counts by this field. For each unique value of the ``query_key`` field, cardinality will be counted separately.

Metric Aggregation
~~~~~~~~~~~~~~~~~~

``metric_aggregation``: This rule matches when the value of a metric within the calculation window is higher or lower than a threshold. By
default this is ``buffer_time``.

This rule requires:

``metric_agg_key``: This is the name of the field over which the metric value will be calculated. The underlying type of this field must be
supported by the specified aggregation type.  If using a scripted field via ``metric_agg_script``, this is the name for your scripted field

``metric_agg_type``: The type of metric aggregation to perform on the ``metric_agg_key`` field. This must be one of 'min', 'max', 'avg', 'sum', 'cardinality', 'value_count', 'percentiles'. Note, if `percentiles` is used, then ``percentile_range`` must also be specified.

.. note:: When Metric Aggregation has a match, match_body includes an aggregated value that triggered the match so that you can use that on an alert. The value is named based on ``metric_agg_key`` and ``metric_agg_type``. For example, if you set ``metric_agg_key`` to 'system.cpu.total.norm.pct' and ``metric_agg_type`` to 'avg', the name of the value is 'metric_system.cpu.total.norm.pct_avg'. Because of this naming rule, you might face conflicts with jinja2 template, and when that happens, you also can use 'metric_agg_value' from match_body instead.

This rule also requires at least one of the two following options:

``max_threshold``: If the calculated metric value is greater than this number, an alert will be triggered. This threshold is exclusive.

``min_threshold``: If the calculated metric value is less than this number, an alert will be triggered. This threshold is exclusive.

``percentile_range``: An integer specifying the percentage value to aggregate against. Must be specified if ``metric_agg_type`` is set to ``percentiles``. See https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-percentile-aggregation.html for more information.

Optional:

``query_key``: Group metric calculations by this field. For each unique value of the ``query_key`` field, the metric will be calculated and
evaluated separately against the threshold(s).

``metric_agg_script``: A `Painless` formatted script describing how to calculate your metric on-the-fly::

    metric_agg_key: myScriptedMetric
    metric_agg_script:
        script: doc['field1'].value * doc['field2'].value

``min_doc_count``: The minimum number of events in the current window needed for an alert to trigger.  Used in conjunction with ``query_key``,
this will only consider terms which in their last ``buffer_time`` had at least ``min_doc_count`` records.  Default 1.

``use_run_every_query_size``: By default the metric value is calculated over a ``buffer_time`` sized window. If this parameter is true
the rule will use ``run_every`` as the calculation window.

``allow_buffer_time_overlap``: This setting will only have an effect if ``use_run_every_query_size`` is false and ``buffer_time`` is greater
than ``run_every``. If true will allow the start of the metric calculation window to overlap the end time of a previous run. By default the
start and end times will not overlap, so if the time elapsed since the last run is less than the metric calculation window size, rule execution
will be skipped (to avoid calculations on partial data).

``bucket_interval``: If present this will divide the metric calculation window into ``bucket_interval`` sized segments. The metric value will
be calculated and evaluated against the threshold(s) for each segment. If ``bucket_interval`` is specified then ``buffer_time`` must be a
multiple of ``bucket_interval``. (Or ``run_every`` if ``use_run_every_query_size`` is true).

``sync_bucket_interval``: This only has an effect if ``bucket_interval`` is present. If true it will sync the start and end times of the metric
calculation window to the keys (timestamps) of the underlying date_histogram buckets. Because of the way elasticsearch calculates date_histogram
bucket keys these usually round evenly to nearest minute, hour, day etc (depending on the bucket size). By default the bucket keys are offset to
allign with the time ElastAlert 2 runs, (This both avoid calculations on partial data, and ensures the very latest documents are included).
See: https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-datehistogram-aggregation.html#_offset for a
more comprehensive explaination.

``metric_format_string``: An optional format string applies to the aggregated metric value in the alert match text and match_body. This adds 'metric_{metric_agg_key}_formatted' value to the match_body in addition to raw, unformatted 'metric_{metric_agg_key}' value so that you can use the values for ``alert_subject_args`` and ``alert_text_args``. Must be a valid python format string. Both str.format() and %-format syntax works. For example, "{:.2%}" will format '0.966666667' to '96.67%', and "%.2f" will format '0.966666667' to '0.97'.
See: https://docs.python.org/3.4/library/string.html#format-specification-mini-language


Spike Aggregation
~~~~~~~~~~~~~~~~~~

``spike_aggregation``: This rule matches when the value of a metric within the calculation window is ``spike_height`` times larger or smaller
than during the previous time period. It uses two sliding windows to compare the current and reference metric values.
We will call these two windows "reference" and "current".

This rule requires:

``metric_agg_key``: This is the name of the field over which the metric value will be calculated. The underlying type of this field must be
supported by the specified aggregation type.  If using a scripted field via ``metric_agg_script``, this is the name for your scripted field

``metric_agg_type``: The type of metric aggregation to perform on the ``metric_agg_key`` field. This must be one of 'min', 'max', 'avg', 'sum', 'cardinality', 'value_count', 'percentiles'. Note, if `percentiles` is used, then ``percentile_range`` must also be specified.

``spike_height``: The ratio of the metric value in the last ``timeframe`` to the previous ``timeframe`` that when hit
will trigger an alert.

``spike_type``: Either 'up', 'down' or 'both'. 'Up' meaning the rule will only match when the metric value is ``spike_height`` times
higher. 'Down' meaning the reference metric value is ``spike_height`` higher than the current metric value. 'Both' will match either.

``buffer_time``: The rule will average out the rate of events over this time period. For example, ``hours: 1`` means that the 'current'
window will span from present to one hour ago, and the 'reference' window will span from one hour ago to two hours ago. The rule
will not be active until the time elapsed from the first event is at least two timeframes. This is to prevent an alert being triggered
before a baseline rate has been established. This can be overridden using ``alert_on_new_data``.

``percentile_range``: An integer specifying the percentage value to aggregate against. Must be specified if ``metric_agg_type`` is set to ``percentiles``. See https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-percentile-aggregation.html for more information.

Optional:

``query_key``: Group metric calculations by this field. For each unique value of the ``query_key`` field, the metric will be calculated and
evaluated separately against the 'reference'/'current' metric value and ``spike height``.

``metric_agg_script``: A `Painless` formatted script describing how to calculate your metric on-the-fly::

    metric_agg_key: myScriptedMetric
    metric_agg_script:
        script: doc['field1'].value * doc['field2'].value

``threshold_ref``: The minimum value of the metric in the reference window for an alert to trigger. For example, if
``spike_height: 3`` and ``threshold_ref: 10``, then the 'reference' window must have a metric value of 10 and the 'current' window at
least three times that for an alert to be triggered.

``threshold_cur``: The minimum value of the metric in the current window for an alert to trigger. For example, if
``spike_height: 3`` and ``threshold_cur: 60``, then an alert will occur if the current window has a metric value greater than 60 and
the reference window is less than a third of that value.

``min_doc_count``: The minimum number of events in the current window needed for an alert to trigger.  Used in conjunction with ``query_key``,
this will only consider terms which in their last ``buffer_time`` had at least ``min_doc_count`` records.  Default 1.

Percentage Match
~~~~~~~~~~~~~~~~

``percentage_match``: This rule matches when the percentage of document in the match bucket within a calculation window is higher or lower
than a threshold. By default the calculation window is ``buffer_time``.

This rule requires:

``match_bucket_filter``: ES filter DSL. This defines a filter for the match bucket, which should match a subset of the documents returned by the
main query filter.

This rule also requires at least one of the two following options:

``min_percentage``: If the percentage of matching documents is less than this number, an alert will be triggered.

``max_percentage``: If the percentage of matching documents is greater than this number, an alert will be triggered.

Optional:

``query_key``: Group percentage by this field. For each unique value of the ``query_key`` field, the percentage will be calculated and
evaluated separately against the threshold(s).

``use_run_every_query_size``: See ``use_run_every_query_size`` in  Metric Aggregation rule

``allow_buffer_time_overlap``:  See ``allow_buffer_time_overlap`` in  Metric Aggregation rule

``bucket_interval``: See ``bucket_interval`` in  Metric Aggregation rule

``sync_bucket_interval``: See ``sync_bucket_interval`` in  Metric Aggregation rule

``percentage_format_string``: An optional format string applies to the percentage value in the alert match text and match_body. This adds 'percentage_formatted' value to the match_body in addition to raw, unformatted 'percentage' value so that you can use the values for ``alert_subject_args`` and ``alert_text_args``. Must be a valid python format string. Both str.format() and %-format syntax works. For example, both "{:.2f}" and "%.2f" will format '96.6666667' to '96.67'.
See: https://docs.python.org/3.4/library/string.html#format-specification-mini-language

``min_denominator``: Minimum number of documents on which percentage calculation will apply. Default is 0.
