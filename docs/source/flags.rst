Command Line Flags
******************

ElastAlert 2 accepts several optional command line parameters:

``--config`` will specify the configuration file to use. The default is
``config.yaml``. 

``--debug`` will run ElastAlert 2 in debug mode. This will increase the logging
verboseness, change all alerts to ``DebugAlerter``, which prints alerts and
suppresses their normal action, and skips writing search and alert metadata back
to Elasticsearch. Not compatible with `--verbose`.

``--end <timestamp>`` will force ElastAlert 2 to stop querying after the given
time, instead of the default, querying to the present time. This really only
makes sense when running standalone. The timestamp is formatted as
``YYYY-MM-DDTHH:MM:SS`` (UTC) or with timezone ``YYYY-MM-DDTHH:MM:SS-XX:00``
(UTC-XX).

``--es_debug`` will enable logging for all queries made to Elasticsearch.

``--es_debug_trace <trace.log>`` will enable logging curl commands for all
queries made to Elasticsearch to the specified log file. ``--es_debug_trace`` is
passed through to `elasticsearch.py
<http://elasticsearch-py.readthedocs.io/en/master/index.html#logging>`_ which
logs `localhost:9200` instead of the actual ``es_host``:``es_port``.

``--pin_rules`` will stop ElastAlert 2 from loading, reloading or removing rules
based on changes to their config files.

``--prometheus_port`` exposes ElastAlert 2 `Prometheus metrics <https://elastalert2.readthedocs.io/en/latest/recipes/exposing_rule_metrics.html>`_ on the specified
port. Prometheus metrics disabled by default.

``--prometheus_addr`` allows you to specify the host address that the Prometheus metrics server will bind to.

``--rule <rule.yaml>`` will only run the given rule. The rule file may be a
complete file path or a filename in ``rules_folder`` or its subdirectories.

``--silence <unit>=<number>`` will silence the alerts for a given rule for a
period of time. The rule must be specified using ``--rule``. <unit> is one of
days, weeks, hours, minutes or seconds. <number> is an integer. For example,
``--rule noisy_rule.yaml --silence hours=4`` will stop noisy_rule from
generating any alerts for 4 hours.

``--silence_qk_value <value`` will silence the rule only for the given 
query key value. This parameter is intended to be used with the ``--rule`` 
parameter.

``--start <timestamp>`` will force ElastAlert 2 to begin querying from the given
time, instead of the default, querying from the present. The timestamp should be
ISO8601, e.g.  ``YYYY-MM-DDTHH:MM:SS`` (UTC) or with timezone
``YYYY-MM-DDTHH:MM:SS-08:00`` (PST). Note that if querying over a large date
range, no alerts will be sent until that rule has finished querying over the
entire time period. To force querying from the current time, use "NOW".

``--verbose`` will increase the logging verboseness, which allows you to see
information about the state of queries. Not compatible with `--debug`.
