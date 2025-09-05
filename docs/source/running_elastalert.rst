.. _tutorial:

Getting Started
***************

ElastAlert 2 can easily be run as :ref:`a Docker container<docker-instructions>`
or directly on your machine as :ref:`a Python package<python-instructions>`.
If you are not interested in modifying the internals of  ElastAlert 2, the Docker
container is recommended for ease of use.

.. _docker-instructions:

As a Docker container
=====================

If you're interested in a pre-built Docker image check out the
elastalert2 container image on `Docker Hub <https://hub.docker.com/r/jertel/elastalert2>`_ or `GitHub Container Registry <https://github.com/jertel/elastalert2/pkgs/container/elastalert2%2Felastalert2>`_. Both images are published for each release. Use GitHub Container Registry if you are running into Docker Hub usage limits.

Be aware that the ``latest`` tag of the image represents the latest commit into
the master branch. If you prefer to upgrade more slowly you will need utilize a
versioned tag, such as ``2.26.0`` instead, or ``2`` if you are comfortable with
always using the latest released version of ElastAlert 2.

A properly configured config.yaml file must be mounted into the container during
startup of the container. Use the `example file
<https://github.com/jertel/elastalert2/blob/master/examples/config.yaml.example>`_
as a template.

The following example assumes Elasticsearch container has already been started with Docker. 
This example also assumes both the Elasticsearch and ElastAlert2 containers are using the default Docker network: ``es_default``

Create a rule directory and rules file in addition to elastalert.yaml, and then mount both into the ElastAlert 2 container:

.. code-block::

    elastalert.yaml
    rules/
      a.yaml

elastalert.yaml

.. code-block::

    rules_folder: /opt/elastalert/rules

    run_every:
      seconds: 10

    buffer_time:
      minutes: 15

    es_host: elasticsearch
    es_port: 9200

    writeback_index: elastalert_status

    alert_time_limit:
      days: 2

a.yaml

.. code-block::

    name: "a"
    type: "frequency"
    index: "mariadblog-*"
    is_enabled: true
    num_events: 2
    realert:
      minutes: 5
    terms_size: 50
    timeframe:
      minutes: 5
    timestamp_field: "@timestamp"
    timestamp_type: "iso"
    use_strftime_index: false
    alert_subject: "Test {} 123 aa☃"
    alert_subject_args:
      - "message"
      - "@log_name"
    alert_text: "Test {}  123 bb☃"
    alert_text_args:
      - "message"
    filter:
      - query:
          query_string:
            query: "@timestamp:*"
    alert:
      - "slack"
    slack_webhook_url: 'https://hooks.slack.com/services/xxxxxxxxx'
    slack_channel_override: "#abc"
    slack_emoji_override: ":kissing_cat:"
    slack_msg_color: "warning"
    slack_parse_override: "none"
    slack_username_override: "elastalert"

Starting the container via Docker Hub (hub.docker.com)

.. code-block::

    docker run --net=es_default -d --name elastalert --restart=always \
    -v $(pwd)/elastalert.yaml:/opt/elastalert/config.yaml \
    -v $(pwd)/rules:/opt/elastalert/rules \
    jertel/elastalert2 --verbose

    docker logs -f elastalert

Starting the container via GitHub Container Registry (ghcr.io)

.. code-block::

    docker run --net=es_default -d --name elastalert --restart=always \
    -v $(pwd)/elastalert.yaml:/opt/elastalert/config.yaml \
    -v $(pwd)/rules:/opt/elastalert/rules \
    ghcr.io/jertel/elastalert2/elastalert2 --verbose

    docker logs -f elastalert

For developers, the below command can be used to build the image locally:

.. code-block::

    docker build . -t elastalert2


.. _kubernetes-instructions:

As a Kubernetes deployment
==========================

The Docker container for ElastAlert 2 can be used directly as a Kubernetes
deployment, but for convenience, a Helm chart is also available. See the
`Chart Readme <https://github.com/jertel/elastalert2/blob/master/chart/elastalert2/README.md>`_ 
for more information on how to install, configure, and run the chart.

.. _python-instructions:

As a Python package
===================

This method is only recommended for advanced users, as providing support is very
challenging due to the numerous differences between everyone's environment.

Requirements
------------

- Elasticsearch 7, 8, or 9 or OpenSearch 1, 2, or 3
- ISO8601 or Unix timestamped data
- Python 3.13. Require OpenSSL 3.0.8 or newer. Note that Python 3.12 is still supported but will be removed in a future release.
- pip
- Packages on Ubuntu 24.04: build-essential python3-pip python3.13 python3.13-dev libffi-dev libssl-dev

If you want to install python 3.13 on CentOS, please install python 3.13 from the source code after installing 'Development Tools'.

Downloading and Configuring
---------------------------

You can either install the latest released version of ElastAlert 2 using pip::

    $ pip install elastalert2

or you can clone the ElastAlert2 repository for the most recent changes::

    $ git clone https://github.com/jertel/elastalert2.git

Install the module::

    $ pip install "setuptools>=11.3"
    $ python setup.py install

Next, open up ``examples/config.yaml.example``. In it, you will find several configuration
options. ElastAlert 2 may be run without changing any of these settings.

See :doc:`configuration` for details on all the configuration options available.

Save the file as ``config.yaml``

Manually Creating the ElastAlert 2 Indices
-------------------------------------------

ElastAlert 2 saves information and metadata about its queries and its alerts back
to Elasticsearch. This is useful for auditing, debugging, and it allows
ElastAlert 2 to restart and resume exactly where it left off. This is not required
for ElastAlert 2 to run, but highly recommended.

First, we need to create an index for ElastAlert 2 to write to by running
``elastalert-create-index`` and following the instructions. Note that this manual 
step is only needed by users that run ElastAlert 2 directly on the host, whereas 
container users will automatically see these indexes created on startup.::

    $ elastalert-create-index
    New index name (Default elastalert_status)
    Name of existing index to copy (Default None)
    New index elastalert_status created
    Done!

For information about what data will go here, see :ref:`ElastAlert 2 Metadata
Index <metadata>`.

Starting ElastAlert 2 via Python CLI
------------------------------------

There are two ways of invoking ElastAlert 2 without Docker. As a daemon, through Supervisor
(http://supervisord.org/), or directly with Python as shown below::

    $ python -m elastalert.elastalert --verbose --rule example_frequency.yaml  # or use the entry point: elastalert --verbose --rule ...

The argument ``--verbose`` sets it to display INFO level messages, while ``--rule example_frequency.yaml`` specifies a single rule to
run, otherwise ElastAlert 2 will attempt to load the other rules in the ``examples/rules`` folder.

Creating a Rule
===============

Each rule defines a query to perform, parameters on what triggers a match, and a
list of alerts to fire for each match. We are going to use
``examples/rules/example_frequency.yaml`` as a template::

    # From examples/rules/example_frequency.yaml
    es_host: elasticsearch.example.com
    es_port: 14900
    name: Example rule
    type: frequency
    index: logstash-*
    num_events: 50
    timeframe:
      hours: 4
    filter:
    - term:
        some_field: "some_value"
    alert:
    - "email"
    email:
    - "elastalert@example.com"

``es_host`` and ``es_port`` should point to the Elasticsearch cluster we want to
query.

``name`` is the unique name for this rule. ElastAlert 2 will not start if two
rules share the same name.

``type``: Each rule has a different type which may take different parameters.
The ``frequency`` type means "Alert when more than ``num_events`` occur within
``timeframe``." For information other types, see :ref:`Rule types <ruletypes>`.

``index``: The name of the index(es) to query. If you are using Logstash, by
default the indexes will match ``"logstash-*"``.

``num_events``: This parameter is specific to ``frequency`` type and is the
threshold for when an alert is triggered.

``timeframe`` is the time period in which ``num_events`` must occur.

``filter`` is a list of Elasticsearch filters that are used to filter results.
Here we have a single term filter for documents with ``some_field`` matching
``some_value``. See :ref:`Writing Filters For Rules <writingfilters>` for more
information. If no filters are desired, it should be specified as an empty list:
``filter: []``

``alert`` is a list of alerts to run on each match. For more information on
alert types, see :ref:`Alert Types <alert_types>`. The email alert requires an SMTP server
for sending mail. By default, it will attempt to use localhost. This can be
changed with the ``smtp_host`` option.

``email`` is a list of addresses to which alerts will be sent.

There are many other optional configuration options, see :ref:`Common
configuration options <commonconfig>`.

All documents must have a timestamp field. ElastAlert 2 will try to use
``@timestamp`` by default, but this can be changed with the ``timestamp_field``
option. By default, ElastAlert 2 uses ISO8601 timestamps, though unix timestamps
are supported by setting ``timestamp_type``.

As is, this rule means "Send an email to elastalert@example.com when there are
more than 50 documents with ``some_field == some_value`` within a 4 hour
period."

See :ref:`the testing section for more details <testing>` on how to test a specific rule file without sending alerts.

Operational Review
==================

When ElastAlert 2 starts and output is configured to be sent to the console, it will resemble the following::

    No handlers could be found for logger "Elasticsearch"
    INFO:root:Queried rule Example rule from 1-15 14:22 PST to 1-15 15:07 PST: 5 hits
    INFO:Elasticsearch:POST http://elasticsearch.example.com:14900/elastalert_status/elastalert_status?op_type=create [status:201 request:0.025s]
    INFO:root:Ran Example rule from 1-15 14:22 PST to 1-15 15:07 PST: 5 query hits (0 already seen), 0 matches, 0 alerts sent
    INFO:root:Sleeping for 297 seconds

Let's break down the response to see what's happening.

``Queried rule Example rule from 1-15 14:22 PST to 1-15 15:07 PST: 5 hits``

ElastAlert 2 periodically queries the most recent ``buffer_time`` (default 45
minutes) for data matching the filters. Here we see that it matched 5 hits:

.. code-block::

    POST http://elasticsearch.example.com:14900/elastalert_status/elastalert_status?op_type=create [status:201 request:0.025s]

This line showing that ElastAlert 2 uploaded a document to the elastalert_status
index with information about the query it just made:

.. code-block::

    Ran Example rule from 1-15 14:22 PST to 1-15 15:07 PST: 5 query hits (0 already seen), 0 matches, 0 alerts sent

The line means ElastAlert 2 has finished processing the rule. For large time
periods, sometimes multiple queries may be run, but their data will be processed
together. ``query hits`` is the number of documents that are downloaded from
Elasticsearch, ``already seen`` refers to documents that were already counted in
a previous overlapping query and will be ignored, ``matches`` is the number of
matches the rule type outputted, and ``alerts sent`` is the number of alerts
actually sent. This may differ from ``matches`` because of options like
``realert`` and ``aggregation`` or because of an error.

``Sleeping for 297 seconds``

The default ``run_every`` is 5 minutes, meaning ElastAlert 2 will sleep until 5
minutes have elapsed from the last cycle before running queries for each rule
again with time ranges shifted forward 5 minutes.

Say, over the next 297 seconds, 46 more matching documents were added to
Elasticsearch::


    INFO:root:Queried rule Example rule from 1-15 14:27 PST to 1-15 15:12 PST: 51 hits
    ...
    INFO:root:Sent email to ['elastalert@example.com']
    ...
    INFO:root:Ran Example rule from 1-15 14:27 PST to 1-15 15:12 PST: 51 query hits, 1 matches, 1 alerts sent

The body of the email will contain something like::

    Example rule

    At least 50 events occurred between 1-15 11:12 PST and 1-15 15:12 PST

    @timestamp: 2015-01-15T15:12:00-08:00

If an error occurred, such as an unreachable SMTP server, you may see:

.. code-block::

    ERROR:root:Error while running alert email: Error connecting to SMTP host: [Errno 61] Connection refused


Note that if you stop ElastAlert 2 and then run it again later, it will look up
``elastalert_status`` and begin querying at the end time of the last query. This
is to prevent duplication or skipping of alerts if ElastAlert 2 is restarted.

By using the ``--debug`` flag instead of ``--verbose``, the body of email will
instead be logged and the email will not be sent. In addition, the queries will
not be saved to ``elastalert_status``.

Disabling a Rule
================

To stop a rule from executing, add or adjust the `is_enabled` option inside the
rule's YAML file to `false`. When ElastAlert 2 reloads the rules it will detect
that the rule has been disabled and prevent it from executing. The rule reload
interval defaults to 5 minutes but can be adjusted via the `run_every`
configuration option.

Optionally, once a rule has been disabled it is safe to remove the rule file, if
there is no intention of re-activating the rule. However, be aware that removing
a rule file without first disabling it will _not_ disable the rule!

