Introduction
************

ElastAlert 2 is a simple framework for alerting on anomalies, spikes, or other patterns of interest from data in `Elasticsearch <https://www.elastic.co/elasticsearch/>`_ and `OpenSearch <https://opensearch.org/>`_.

If you have data being written into Elasticsearch in near real time and want to be alerted when that data matches certain patterns, ElastAlert 2 is the tool for you.

Overview
========

We designed ElastAlert 2 to be :ref:`reliable <reliability>`, highly :ref:`modular <modularity>`, and easy to setup.

It works by combining Elasticsearch with two types of components, rules and alerts.
The datasource, typically Elasticsearch, is periodically queried and the data is passed to the rule type, which determines when
a match is found. When a match occurs, it is given to one or more alerts, which take action based on the match.

This is configured by a set of rules, each of which defines a query, a rule type, and a set of alerts.

Several rule types with common monitoring paradigms are included with ElastAlert 2:

- "Match where there are X events in Y time" (``frequency`` type)
- "Match when the rate of events increases or decreases" (``spike`` type)
- "Match when there are less than X events in Y time" (``flatline`` type)
- "Match when a certain field matches a blacklist/whitelist" (``blacklist`` and ``whitelist`` type)
- "Match on any event matching a given filter" (``any`` type)
- "Match when a field has two different values within some time" (``change`` type)

Currently, we have support built in for these alert types:

- Alerta
- Alertmanager
- AWS SES (Amazon Simple Email Service)
- AWS SNS (Amazon Simple Notification Service)
- Chatwork
- Command
- Datadog
- Debug
- Dingtalk
- Discord
- Email
- Exotel
- Flashduty
- Gitter
- GoogleChat
- Graylog GELF
- HTTP POST
- HTTP POST 2
- Indexer
- Iris
- Jira
- Lark
- Line Notify
- Matrix Hookshot
- Mattermost
- Microsoft Teams
- Microsoft Power Automate
- OpsGenie
- PagerDuty
- PagerTree
- Rocket.Chat
- Squadcast
- ServiceNow
- Slack
- SMSEagle
- Splunk On-Call (Formerly VictorOps)
- Stomp
- Telegram
- Tencent SMS
- TheHive
- Twilio
- Webex Incoming Webhook
- WorkWechat  
- Zabbix

Additional rule types and alerts can be easily imported or written. (See :ref:`Writing rule types <writingrules>` and :ref:`Writing alerts <writingalerts>`)

In addition to this basic usage, there are many other features that make alerts more useful:

- Alerts link to Kibana Discover searches
- Aggregate counts for arbitrary fields
- Combine alerts into periodic reports
- Separate alerts by using a unique key field
- Intercept and enhance match data

To get started, check out :ref:`Running ElastAlert 2 For The First Time <tutorial>`.

.. _reliability:

Reliability
===========

ElastAlert 2 has several features to make it more reliable in the event of restarts or Elasticsearch unavailability:

- ElastAlert 2 :ref:`saves its state to Elasticsearch <metadata>` and, when started, will resume where previously stopped
- If Elasticsearch is unresponsive, ElastAlert 2 will wait until it recovers before continuing
- Alerts which throw errors may be automatically retried for a period of time

.. _modularity:

Modularity
==========

ElastAlert 2 has three main components that may be imported as a module or customized:

Rule types
----------

The rule type is responsible for processing the data returned from Elasticsearch. It is initialized with the rule configuration, passed data
that is returned from querying Elasticsearch with the rule's filters, and outputs matches based on this data. See :ref:`Writing rule types <writingrules>`
for more information.

Alerts
------

Alerts are responsible for taking action based on a match. A match is generally a dictionary containing values from a document in Elasticsearch,
but may contain arbitrary data added by the rule type. See :ref:`Writing alerts <writingalerts>` for more information.

Enhancements
------------

Enhancements are a way of intercepting an alert and modifying or enhancing it in some way. They are passed the match dictionary before it is given
to the alerter. See :ref:`Enhancements` for more information.
