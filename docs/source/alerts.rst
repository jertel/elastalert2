.. _Alerts:

Alerts
******

Each rule may have any number of alerts attached to it. Alerts are subclasses of ``Alerter`` and are passed
a dictionary, or list of dictionaries, from ElastAlert 2 which contain relevant information. They are configured
in the rule configuration file similarly to rule types.

To set the alerts for a rule, set the ``alert`` option to the name of the alert, or a list of the names of alerts:

``alert: email``

or

.. code-block:: yaml

    alert:
      - alerta
      - alertmanager
      - chatwork
      - command
      - datadog
      - debug
      - dingtalk
      - discord
      - email
      - exotel
      - flashduty
      - gitter
      - googlechat
      - gelf
      - hivealerter
      - indexer
      - iris
      - jira
      - lark
      - matrixhookshot
      - mattermost
      - ms_teams
      - ms_power_automate
      - opsgenie
      - pagerduty
      - pagertree
      - post
      - post2
      - rocketchat
      - servicenow
      - ses
      - slack
      - smseagle
      - sns
      - stomp
      - telegram
      - tencent_sms
      - twilio
      - victorops
      - webex_webhook
      - workwechat
      - zabbix
      - yzj

Options for each alerter can either defined at the top level of the YAML file, or nested within the alert name, allowing for different settings
for multiple of the same alerter. For example, consider sending multiple emails, but with different 'To' and 'From' fields:

.. code-block:: yaml

    alert:
     - email
    from_addr: "no-reply@example.com"
    email: "customer@example.com"

versus

.. code-block:: yaml

    alert:
     - email:
         from_addr: "no-reply@example.com"
         email: "customer@example.com"
     - email:
         from_addr: "elastalert@example.com""
         email: "devs@example.com"

If multiple of the same alerter type are used, top level settings will be used as the default and inline settings will override those
for each alerter.

Alert Subject
=============

E-mail subjects, Jira issue summaries, PagerDuty alerts, or any alerter that has a "subject" can be customized by adding an ``alert_subject``
that contains a custom summary.
It can be further formatted using standard Python formatting syntax::

    alert_subject: "Issue {0} occurred at {1}"

The arguments for the formatter will be fed from the matched objects related to the alert.
The field names whose values will be used as the arguments can be passed with ``alert_subject_args``::


    alert_subject_args:
    - issue.name
    - "@timestamp"

It is mandatory to enclose the ``@timestamp`` field in quotes since in YAML format a token cannot begin with the ``@`` character. Not using the quotation marks will trigger a YAML parse error.

In case the rule matches multiple objects in the index, only the first match is used to populate the arguments for the formatter.

If the field(s) mentioned in the arguments list are missing, the email alert will have the text ``alert_missing_value`` in place of its expected value. This will also occur if ``use_count_query`` is set to true.

Alert Content
=============

There are several ways to format the body text of the various types of events. In EBNF::

    rule_name           = name
    alert_text          = alert_text
    ruletype_text       = Depends on type
    top_counts_header   = top_count_key, ":"
    top_counts_value    = Value, ": ", Count
    top_counts          = top_counts_header, LF, top_counts_value
    field_values        = Field, ": ", Value

Similarly to ``alert_subject``, ``alert_text`` can be further formatted using Jinja2 Templates or Standard Python Formatting Syntax

1. Jinja Template

By setting ``alert_text_type: alert_text_jinja`` you can use jinja2 templates in ``alert_text`` and ``alert_subject``. ::

    alert_text_type: alert_text_jinja

    alert_text: |
      Alert triggered! *({{num_hits}} Matches!)*
      Something happened with {{username}} ({{email}})
      {{description|truncate}}

Top fields are accessible via `{{field_name}}` or `{{_data['field_name']}}`, `_data` is useful when accessing *fields with dots in their keys*, as Jinja treat dot as a nested field.
If `_data` conflicts with your top level data, use  ``jinja_root_name`` to change its name.

2. Standard Python Formatting Syntax

The field names whose values will be used as the arguments can be passed with ``alert_text_args`` or ``alert_text_kw``.
You may also refer to any top-level rule property in the ``alert_subject_args``, ``alert_text_args``, ``alert_missing_value``, and ``alert_text_kw fields``.  However, if the matched document has a key with the same name, that will take preference over the rule property. ::

    alert_text: "Something happened with {0} at {1}"
    alert_text_type: alert_text_only
    alert_text_args: ["username", "@timestamp"]

By default::

    body                = rule_name

                          [alert_text]

                          ruletype_text

                          {top_counts}

                          {field_values}

With ``alert_text_type: alert_text_only``::

    body                = rule_name

                          alert_text


With ``alert_text_type: alert_text_jinja``::

    body                = rule_name

                          alert_text


With ``alert_text_type: exclude_fields``::

    body                = rule_name

                          [alert_text]

                          ruletype_text

                          {top_counts}

With ``alert_text_type: aggregation_summary_only``::

    body                = rule_name

                          aggregation_summary

ruletype_text is the string returned by RuleType.get_match_str.

field_values will contain every key value pair included in the results from Elasticsearch. These fields include "@timestamp" (or the value of ``timestamp_field``),
every key in ``include``, every key in ``top_count_keys``, ``query_key``, and ``compare_key``. If the alert spans multiple events, these values may
come from an individual event, usually the one which triggers the alert.

When using ``alert_text_args``, you can access nested fields and index into arrays. For example, if your match was ``{"data": {"ips": ["127.0.0.1", "12.34.56.78"]}}``, then by using ``"data.ips[1]"`` in ``alert_text_args``, it would replace value with ``"12.34.56.78"``. This can go arbitrarily deep into fields and will still work on keys that contain dots themselves.

Further, accessing subfields within a nested array structure is accomplished by specifying the subfield name directly after the array index brackets. 

For example, given the below data::

    {"data": { "items": [{ "name": "Mickey Mouse", "price": 24.95 }, { "name": "Winnie the Pooh", "price": 14.95 }], "tax": 2.39, "total": 42.29 } }

You would then access the fields as follows::

    data.items[0]name
    data.items[0]price
    data.items[1]name
    data.items[1]price
    data.tax
    data.total

Alerter Base Type
=================

For all Alerter subclasses, you may reference values from a top-level rule property in your Alerter fields by referring to the property name surrounded by dollar signs. This can be useful when you have rule-level properties that you would like to reference many times in your alert. For example:

Example usage::

    jira_priority: $priority$
    jira_alert_owner: $owner$


.. _alert_types:

Alert Types
===========

Alerta
~~~~~~

Alerta alerter will post an alert in the Alerta server instance through the alert API endpoint.
See https://docs.alerta.io/api/reference.html#alerts for more details on the Alerta JSON format.

For Alerta 5.0

Required:

``alerta_api_url``: API server URL.

Optional:

``alerta_api_key``: This is the api key for alerta server, sent in an ``Authorization`` HTTP header. If not defined, no Authorization header is sent.

``alerta_use_qk_as_resource``: If true and query_key is present, this will override ``alerta_resource`` field with the ``query_key value`` (Can be useful if ``query_key`` is a hostname).

``alerta_use_match_timestamp``: If true, it will use the timestamp of the first match as the ``createTime`` of the alert. otherwise, the current server time is used.

``alerta_api_skip_ssl``: Defaults to False.

``alert_missing_value``: Text to replace any match field not found when formating strings. Defaults to ``<MISSING_TEXT>``.

The following options dictate the values of the API JSON payload:

``alerta_severity``: Defaults to "warning".

``alerta_timeout``: Defaults 86400 (1 Day).

``alerta_type``: Defaults to "elastalert".

The following options use Python-like string syntax ``{<field>}`` or ``%(<field>)s`` to access parts of the match, similar to the CommandAlerter. Ie: "Alert for {clientip}".
If the referenced key is not found in the match, it is replaced by the text indicated by the option ``alert_missing_value``.

``alerta_resource``: Defaults to "elastalert".

``alerta_service``: Defaults to "elastalert".

``alerta_origin``: Defaults to "elastalert".

``alerta_environment``: Defaults to "Production".

``alerta_group``: Defaults to "".

``alerta_correlate``: Defaults to an empty list.

``alerta_tags``: Defaults to an empty list.

``alerta_event``: Defaults to the rule's name.

``alerta_text``: Defaults to the rule's text according to its type.

``alerta_value``: Defaults to "".

The ``attributes`` dictionary is built by joining the lists from  ``alerta_attributes_keys`` and ``alerta_attributes_values``, considered in order.


Example usage using old-style format::

    alert:
      - alerta
    alerta_api_url: "http://youralertahost/api/alert"
    alerta_attributes_keys:   ["hostname",   "TimestampEvent",  "senderIP" ]
    alerta_attributes_values: ["%(key)s",    "%(logdate)s",     "%(sender_ip)s"  ]
    alerta_correlate: ["ProbeUP","ProbeDOWN"]
    alerta_event: "ProbeUP"
    alerta_text:  "Probe %(hostname)s is UP at %(logdate)s GMT"
    alerta_value: "UP"

Example usage using new-style format::

    alert:
      - alerta
    alerta_attributes_values: ["{key}",    "{logdate}",     "{sender_ip}"  ]
    alerta_text:  "Probe {hostname} is UP at {logdate} GMT"

Alertmanager
~~~~~~~~~~~~

This alert type will send alerts to Alertmanager postAlerts. ``alert_subject`` and ``alert_text`` are passed as the annotations labeled ``summary`` and ``description`` accordingly. The labels can be changed.
See https://prometheus.io/docs/alerting/clients/ for more details about the Alertmanager alert format.

Required:

``alertmanager_hosts``: The list of hosts pointing to the Alertmanager.

Optional:

``alertmanager_api_version``: Defaults to `v1`.  Set to `v2` to enable the Alertmanager V2 API postAlerts.

``alertmanager_alertname``: ``alertname`` is the only required label. Defaults to using the rule name of the alert.

``alertmanager_labels``: Key:value pairs of arbitrary labels to be attached to every alert. Keys should match the regular expression ``^[a-zA-Z_][a-zA-Z0-9_]*$``. Jinja2 templating, such as ``{{ field }}``, can be used in the value to reference any field in the matched events. When field names use dot notation or reserved characters, ``_data`` can be used to access these fields. If ``_data`` conflicts with your top level data, use ``jinja_root_name`` to change its name.

``alertmanager_annotations``: Key:value pairs of arbitrary annotations to be attached to every alert. Keys should match the regular expression ``^[a-zA-Z_][a-zA-Z0-9_]*$``. Jinja2 templating, such as ``{{ field }}``, can be used in the value to reference any field in the matched events. When field names use dot notation or reserved characters, ``_data`` can be used to access these fields. If ``_data`` conflicts with your top level data, use ``jinja_root_name`` to change its name.

``alertmanager_fields``: Key:value pairs of labels and corresponding match fields. When using ``alertmanager_fields`` you can access nested fields and index into arrays the same way as with ``alert_text_args``. Keys should match the regular expression ``^[a-zA-Z_][a-zA-Z0-9_]*$``. This dictionary will be merged with the ``alertmanager_labels``.

``alertmanager_alert_subject_labelname``: Rename the annotations' label name for ``alert_subject``. Default is ``summary``.

``alertmanager_alert_text_labelname``: Rename the annotations' label name for ``alert_text``. Default is ``description``.

``alertmanager_proxy``: By default ElastAlert 2 will not use a network proxy to send notifications to Alertmanager. Set this option using ``hostname:port`` if you need to use a proxy. only supports https.

``alertmanager_ca_certs``: Set this option to ``True`` or a path to a CA cert bundle or directory (eg: ``/etc/ssl/certs/ca-certificates.crt``) to validate the SSL certificate.

``alertmanager_ignore_ssl_errors``: By default ElastAlert 2 will verify SSL certificate. Set this option to ``True`` if you want to ignore SSL errors.

``alertmanager_timeout``: You can specify a timeout value, in seconds, for making communicating with Alertmanager. The default is 10. If a timeout occurs, the alert will be retried next time ElastAlert 2 cycles.
``
``alertmanager_resolve_time``: Optionally provide an automatic resolution timeframe. If no further alerts arrive within this time period alertmanager will automatically mark the alert as resolved. If not defined it will use Alertmanager's default behavior.
``
``alertmanager_basic_auth_login``: Basic authentication username.

``alertmanager_basic_auth_password``: Basic authentication password.

Example usage::

  alert:
    - "alertmanager"
  alertmanager_hosts:
    - "http://alertmanager:9093"
  alertmanager_alertname: "Title"
  alertmanager_annotations:
    severity: "error"
  alertmanager_resolve_time:
    minutes: 10
  alertmanager_labels:
    source: "elastalert"
  alertmanager_fields:
    msg: "message"
    log: "@log_name"

Additional explanation:

ElastAlert 2 can send two categories of data to Alertmanager: labels and annotations

Labels are sent either as static values or can be formatted using jinja2 templates that reference any field values from the Elastic record that triggered the alert. For example::

    alertmanager_labels:
      someStaticLabel: "Verify this issue"
      someTemplatedLabel: "{{ someElasticFieldName }}"
      someOtherTemplatedLabel: "{{ someElasticFieldName }}:{{ _data["some.elastic.field.name"] }}"

Alternatively you can use the ``alertmanager_fields`` option to define a dictionary of labels and corresponding field names from the Elastic record which will then be merged back into the dictionary defined by ``alertmanager_labels``.

    alertmanager_fields:
      someLabel: "someElasticFieldName"
      someOtherLabel: "someOtherElasticFieldName"

Annotations are similar to labels where it can either be a static value or formatted using jinja2 templates. The only difference is that ``alert_text`` and ``alert_subject`` are merged back into the dictionary defined by ``alertmanager_annotations`` and are subjected to [different formatting rules](https://elastalert2.readthedocs.io/en/latest/ruletypes.html#alert-subject).

For example::

    alertmanager_annotations:
      someStaticAnnotation: "This is a static annotation value, it never changes"
      someTemplatedAnnotation: "This is a templated annotation value: {{ someElasticFieldName }}"

    alertmanager_alert_subject_labelname: myCustomAnnotationName1
    alertmanager_alert_text_labelname: myCustomAnnotationName2

    alert_subject: "Host {0} has status {1}"
    alert_subject_args:
    - http_host
    - status

    alert_text: "URL {0} has {1} matches"
    alert_text_type: alert_text_only
    alert_text_args:
    - uri
    - num_matches

AWS SES (Amazon Simple Email Service)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The AWS SES alerter is similar to Email alerter but uses AWS SES to send emails. The AWS SES alerter can use AWS credentials
from the rule yaml, standard AWS config files or environment variables.

AWS SES requires one option:

``ses_email``: An address or list of addresses to sent the alert to.

single address example::

  ses_email: "one@domain"

or

multiple address example::

  ses_email:
    - "one@domain"
    - "two@domain"

``ses_from_addr``: This sets the From header in the email.

Optional:

``ses_aws_access_key``: An access key to connect to AWS SES with.

``ses_aws_secret_key``: The secret key associated with the access key.

``ses_aws_region``: The AWS region in which the AWS SES resource is located. Default is us-east-1

``ses_aws_profile``: The AWS profile to use. If none specified, the default will be used.

``ses_email_reply_to``: This sets the Reply-To header in the email.

``ses_cc``: This adds the CC emails to the list of recipients. By default, this is left empty.

single address example::

  ses_cc: "one@domain"

or

multiple address example::

  ses_cc:
    - "one@domain"
    - "two@domain"

``ses_bcc``: This adds the BCC emails to the list of recipients but does not show up in the email message. By default, this is left empty.

single address example::

  ses_bcc: "one@domain"

or

multiple address example::

  ses_bcc:
    - "one@domain"
    - "two@domain"

Example When not using aws_profile usage::

    alert:
      - "ses"
    ses_aws_access_key_id: "XXXXXXXXXXXXXXXXXX'"
    ses_aws_secret_access_key: "YYYYYYYYYYYYYYYYYYYY"
    ses_aws_region: "us-east-1"
    ses_from_addr: "xxxx1@xxx.com"
    ses_email: "xxxx1@xxx.com"

Example When to use aws_profile usage::

    # Create ~/.aws/credentials

    [default]
    aws_access_key_id = xxxxxxxxxxxxxxxxxxxx
    aws_secret_access_key = yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy

    # Create ~/.aws/config

    [default]
    region = us-east-1

    # alert rule setting

    alert:
      - "ses"
    ses_aws_profile: "default"
    ses_from_addr: "xxxx1@xxx.com"
    ses_email: "xxxx1@xxx.com"

AWS SNS (Amazon Simple Notification Service)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The AWS SNS alerter will send an AWS SNS notification. The body of the notification is formatted the same as with other alerters.
The AWS SNS alerter uses boto3 and can use credentials in the rule yaml, in a standard AWS credential and config files, or
via environment variables. See http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html for details.

AWS SNS requires one option:

``sns_topic_arn``: The SNS topic's ARN. For example, ``arn:aws:sns:us-east-1:123456789:somesnstopic``

Optional:

``sns_aws_access_key_id``: An access key to connect to SNS with.

``sns_aws_secret_access_key``: The secret key associated with the access key.

``sns_aws_region``: The AWS region in which the SNS resource is located. Default is us-east-1

``sns_aws_profile``: The AWS profile to use. If none specified, the default will be used.

Example When not using aws_profile usage::

    alert:
      - sns
    sns_topic_arn: 'arn:aws:sns:us-east-1:123456789:somesnstopic'
    sns_aws_access_key_id: 'XXXXXXXXXXXXXXXXXX''
    sns_aws_secret_access_key: 'YYYYYYYYYYYYYYYYYYYY'
    sns_aws_region: 'us-east-1' # You must nest aws_region within your alert configuration so it is not used to sign AWS requests.

Example When to use aws_profile usage::

    # Create ~/.aws/credentials

    [default]
    aws_access_key_id = xxxxxxxxxxxxxxxxxxxx
    aws_secret_access_key = yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy

    # Create ~/.aws/config

    [default]
    region = us-east-1

    # alert rule setting

    alert:
      - sns
    sns_topic_arn: 'arn:aws:sns:us-east-1:123456789:somesnstopic'
    sns_aws_profile: 'default'

Chatwork
~~~~~~~~

Chatwork will send notification to a Chatwork application. The body of the notification is formatted the same as with other alerters.

Required:

``chatwork_apikey``:  Chatwork API KEY.

``chatwork_room_id``: The ID of the room you are talking to in Chatwork. How to find the room ID is the part of the number after "rid" at the end of the URL of the browser.

``chatwork_proxy``: By default ElastAlert 2 will not use a network proxy to send notifications to Chatwork. Set this option using ``hostname:port`` if you need to use a proxy. only supports https.

``chatwork_proxy_login``: The Chatwork proxy auth username.

``chatwork_proxy_pass``: The Chatwork proxy auth password.

Example usage::

    alert:
      - "chatwork"
    chatwork_apikey: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    chatwork_room_id: "xxxxxxxxx"

Command
~~~~~~~

The command alert allows you to execute an arbitrary command and pass arguments or stdin from the match. Arguments to the command can use
Python format string syntax to access parts of the match. The alerter will open a subprocess and optionally pass the match, or matches
in the case of an aggregated alert, as a JSON array, to the stdin of the process.

This alert requires one option:

``command``: A list of arguments to execute or a string to execute. If in list format, the first argument is the name of the program to execute. If passed a
string, the command is executed through the shell.

Strings can be formatted using the old-style format (``%``) or the new-style format (``.format()``). When the old-style format is used, fields are accessed
using ``%(field_name)s``, or ``%(field.subfield)s``. When the new-style format is used, fields are accessed using ``{field_name}``. New-style formatting allows accessing nested
fields (e.g., ``{field_1[subfield]}``).

In an aggregated alert, these fields come from the first match.

Optional:

``pipe_match_json``: If true, the match will be converted to JSON and passed to stdin of the command. Note that this will cause ElastAlert 2 to block
until the command exits or sends an EOF to stdout.

``pipe_alert_text``: If true, the standard alert body text will be passed to stdin of the command. Note that this will cause ElastAlert 2 to block
until the command exits or sends an EOF to stdout. It cannot be used at the same time as ``pipe_match_json``.

``fail_on_non_zero_exit``: By default this is ``False``. Allows monitoring of when commands fail to run. When a command returns a non-zero exit status, the alert raises an exception.

Example usage using old-style format::

    alert:
      - command
    command: ["/bin/send_alert", "--username", "%(username)s"]

.. warning::

    Executing commmands with untrusted data can make it vulnerable to shell injection! If you use formatted data in
    your command, it is highly recommended that you use a args list format instead of a shell string.

Example usage using new-style format::

    alert:
      - command
    command: ["/bin/send_alert", "--username", "{match[username]}"]

Datadog
~~~~~~~

This alert will create a `Datadog Event`_. Events are limited to 4000 characters. If an event is sent that contains
a message that is longer than 4000 characters, only his first 4000 characters will be displayed.

This alert requires two additional options:

``datadog_api_key``: `Datadog API key`_

``datadog_app_key``: `Datadog application key`_

Example usage::

    alert:
      - "datadog"
    datadog_api_key: "Datadog API Key"
    datadog_app_key: "Datadog APP Key"

.. _`Datadog Event`: https://docs.datadoghq.com/events/
.. _`Datadog API key`: https://docs.datadoghq.com/account_management/api-app-keys/#api-keys
.. _`Datadog application key`: https://docs.datadoghq.com/account_management/api-app-keys/#application-keys

Debug
~~~~~

The debug alerter will log the alert information using the Python logger at the info level. It is logged into a Python Logger object with the name ``elastalert`` that can be easily accessed using the ``getLogger`` command.

Dingtalk
~~~~~~~~

Dingtalk will send notification to a Dingtalk application. The body of the notification is formatted the same as with other alerters.

Required:

``dingtalk_access_token``:  Dingtalk access token.

``dingtalk_msgtype``:  Dingtalk msgtype, default to ``text``. ``markdown``, ``single_action_card``, ``action_card``.

dingtalk_msgtype single_action_card Required:

``dingtalk_single_title``: The title of a single button..

``dingtalk_single_url``: Jump link for a single button.

dingtalk_msgtype action_card Required:

``dingtalk_btns``:  Button.

dingtalk_msgtype action_card Optional:

``dingtalk_btn_orientation``:  "0": Buttons are arranged vertically "1": Buttons are arranged horizontally.

Example msgtype : text::

    alert:
      - "dingtalk"
    dingtalk_access_token: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    dingtalk_msgtype: "text"


Example msgtype : markdown::

    alert:
      - "dingtalk"
    dingtalk_access_token: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    dingtalk_msgtype: "markdown"


Example msgtype : single_action_card::

    alert:
      - "dingtalk"
    dingtalk_access_token: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    dingtalk_msgtype: "single_action_card"
    dingtalk_single_title: "test3"
    dingtalk_single_url: "https://xxxx.xxx"


Example msgtype : action_card::

    alert:
      - "dingtalk"
    dingtalk_access_token: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    dingtalk_msgtype: "action_card"
    dingtalk_btn_orientation: "0"
    dingtalk_btns: [{"title": "a", "actionURL": "https://xxxx1.xxx"}, {"title": "b", "actionURL": "https://xxxx2.xxx"}]

Optional:

``dingtalk_proxy``: By default ElastAlert 2 will not use a network proxy to send notifications to Dingtalk. Set this option using ``hostname:port`` if you need to use a proxy. only supports https.

``dingtalk_proxy_login``: The DingTalk proxy auth username.

``dingtalk_proxy_pass``: The DingTalk proxy auth username.

``dingtalk_sign``: DingTalk HMAC secret, used for message authentication. See https://open.dingtalk.com/document/robots/customize-robot-security-settings for more information. Note that the algorithm provides authentication that *some* message was recently sent (within an hour) but does not authenticate the integrity of the current message itself. 

Discord
~~~~~~~

Discord will send notification to a Discord application. The body of the notification is formatted the same as with other alerters.

Required:

``discord_webhook_url``:  The webhook URL.

Optional:

``discord_emoji_title``: By default ElastAlert 2 will use the ``:warning:`` emoji when posting to the channel. You can use a different emoji per ElastAlert 2 rule. Any Apple emoji can be used, see http://emojipedia.org/apple/ . If discord_embed_icon_url parameter is provided, emoji is ignored.

``discord_proxy``: By default ElastAlert 2 will not use a network proxy to send notifications to Discord. Set this option using ``hostname:port`` if you need to use a proxy. only supports https.

``discord_proxy_login``: The Discord proxy auth username.

``discord_proxy_password``: The Discord proxy auth username.

``discord_embed_color``: embed color. By default ``0xffffff``.

``discord_embed_footer``: embed footer.

``discord_embed_icon_url``: You can provide icon_url to use custom image. Provide absolute address of the pciture.

Example usage::

    alert:
    - "discord"
    discord_webhook_url: "Your discord webhook url"
    discord_emoji_title: ":lock:"
    discord_embed_color: 0xE24D42
    discord_embed_footer: "Message sent by  from your computer"
    discord_embed_icon_url: "https://humancoders-formations.s3.amazonaws.com/uploads/course/logo/38/thumb_bigger_formation-elasticsearch.png"

Email
~~~~~

This alert will send an email. It connects to an smtp server located at ``smtp_host``, or localhost by default.
If available, it will use STARTTLS.

This alert requires one additional option:

``email``: An address or list of addresses to sent the alert to.

single address example::

  email: "one@domain"

or

multiple address example::

  email:
    - "one@domain"
    - "two@domain"

Optional:

``email_from_field``: Use a field from the document that triggered the alert as the recipient. If the field cannot be found,
the ``email`` value will be used as a default. Note that this field will not be available in every rule type, for example, if
you have ``use_count_query`` or if it's ``type: flatline``. You can optionally add a domain suffix to the field to generate the
address using ``email_add_domain``. It can be a single recipient or list of recipients. For example, with the following settings::

    email_from_field: "data.user"
    email_add_domain: "@example.com"

and a match ``{"@timestamp": "2017", "data": {"foo": "bar", "user": "qlo"}}``

an email would be sent to ``qlo@example.com``

``smtp_host``: The SMTP host to use, defaults to localhost.

``smtp_port``: The port to use. Defaults to port 25 when SSL is not used, or 465 when SSL is used.

``smtp_ssl``: Connect the SMTP host using TLS, defaults to ``false``. If ``smtp_ssl`` is not used, ElastAlert 2 will still attempt
STARTTLS.

``smtp_auth_file``: The path to a file which contains SMTP authentication credentials. The path can be either absolute or relative
to the given rule. It should be YAML formatted and contain two fields, ``user`` and ``password``. If this is not present,
no authentication will be attempted.

``smtp_cert_file``: Connect the SMTP host using the given path to a TLS certificate file, default to ``None``.

``smtp_key_file``: Connect the SMTP host using the given path to a TLS key file, default to ``None``.

``email_reply_to``: This sets the Reply-To header in the email. By default, the from address is ElastAlert@ and the domain will be set
by the smtp server.

``from_addr``: This sets the From header in the email. By default, the from address is ElastAlert@ and the domain will be set
by the smtp server.

``cc``: This adds the CC emails to the list of recipients. By default, this is left empty.

single address example::

  cc: "one@domain"

or

multiple address example::

  cc:
    - "one@domain"
    - "two@domain"

``bcc``: This adds the BCC emails to the list of recipients but does not show up in the email message. By default, this is left empty.

single address example::

  bcc: "one@domain"

or

multiple address example::

  bcc:
    - "one@domain"
    - "two@domain"

``email_format``: If set to 'html', the email's MIME type will be set to HTML, and HTML content should correctly render. If you use this,
you need to put your own HTML into ``alert_text`` and use ``alert_text_type: alert_text_jinja`` Or ``alert_text_type: alert_text_only``.

``assets_dir``: images dir. default to ``/tmp``.

``email_image_keys``: mapping between images keys.

``email_image_values``: mapping between images values

Example assets_dir, email_image_keys, email_image_values::

	assets_dir: "/opt/elastalert/email_images"
	email_image_keys: ["img1"]
	email_image_values: ["my_logo.png"]

Exotel
~~~~~~

Developers in India can use the Exotel alerter, which can send an alert to a mobile phone as an SMS from your ExoPhone. The SMS will contain both the alert name and the specified message body.

The alerter requires the following option:

``exotel_account_sid``: The SID of your Exotel account.

``exotel_auth_token``: The auth token associated with your Exotel account.

Instructions for finding the SID and auth token associated with your account can be found `on the Exotel website
<https://support.exotel.com/support/solutions/articles/3000023019-how-to-find-my-exotel-token-and-exotel-sid>`_.

``exotel_to_number``: The phone number to which you would like to send the alert.

``exotel_from_number``: The ExoPhone number from which the alert will be sent.

The alerter has one optional argument:

``exotel_message_body``: The contents of the SMS. If you don't specify this argument, only the rule name is sent.

Example usage::

    alert:
      - "exotel"
    exotel_account_sid: "Exotel Account SID"
    exotel_auth_token: "Exotel Auth token"
    exotel_to_number: "Exotel to number"
    exotel_from_number: "Exotel from number"

Gitter
~~~~~~

Gitter alerter will send a notification to a predefined Gitter channel. The body of the notification is formatted the same as with other alerters.

The alerter requires the following option:

``gitter_webhook_url``: The webhook URL that includes your auth data and the ID of the channel (room) you want to post to. Go to the Integration Settings
of the channel https://gitter.im/ORGA/CHANNEL#integrations , click 'CUSTOM' and copy the resulting URL.

Optional:

``gitter_msg_level``: By default the alert will be posted with the 'error' level. You can use 'info' if you want the messages to be black instead of red.

``gitter_proxy``: By default ElastAlert 2 will not use a network proxy to send notifications to Gitter. Set this option using ``hostname:port`` if you need to use a proxy. only supports https.

Example usage::

    alert:
      - "gitter"
    gitter_webhook_url: "Your Gitter Webhook URL"
    gitter_msg_level: "error"

GoogleChat
~~~~~~~~~~
GoogleChat alerter will send a notification to a predefined GoogleChat channel. The body of the notification is formatted the same as with other alerters.

The alerter requires the following options:

``googlechat_webhook_url``: The webhook URL that includes the channel (room) you want to post to. Go to the Google Chat website https://chat.google.com and choose the channel in which you wish to receive the notifications. Select 'Configure Webhooks' to create a new webhook or to copy the URL from an existing one. You can use a list of URLs to send to multiple channels.

Optional:

``googlechat_format``: Formatting for the notification. Can be either 'card' or 'basic' (default).

``googlechat_header_title``: Sets the text for the card header title. (Only used if format=card)

``googlechat_header_subtitle``: Sets the text for the card header subtitle. (Only used if format=card)

``googlechat_header_image``: URL for the card header icon. (Only used if format=card)

``googlechat_footer_kibanalink``: URL to Kibana to include in the card footer. (Only used if format=card)

``googlechat_proxy``: By default ElastAlert 2 will not use a network proxy to send notifications to GoogleChat. Set this option using ``hostname:port`` if you need to use a proxy. only supports https.

Graylog GELF
~~~~~~~~~~~~
GELF alerter will send a custom message to a Graylog GELF input (HTTP/TCP). Alert payload content you form with key-value pairs.

The alerter requires the following options:

``gelf_type``: Type of your Graylog GELF Input. How available 'http' or 'tcp'.

And in case of HTTP:

``gelf_endpoint``: Link to GELF HTTP Input as an example: 'http://example.com/gelf' (Only used if gelf_type=http)

Or next if selected TCP:

``gelf_host``: Graylog server address where Input launched. (Only used if gelf_type=tcp)

``gelf_port``: Port, specified for Input. (Only used if gelf_type=tcp)

``gelf_payload``: Main message body. Working as key-value, where the key is your custom name and value - data from elasticsearch message. Name of alert will write to beginning of the message.

Example usage::

    alert:
      - gelf
    gelf_type: http
    gelf_endpoint: http://example.com:12201/gelf
    gelf_payload:
      username: user
      src_ip: source_ip

Optional:

``gelf_log_level``: Standard syslog severity levels. By default set 5 (Notice)

``gelf_http_headers``: Additional headers. (Only used if gelf_type=http)

``gelf_ca_cert``: Path to custom CA certificate.

``gelf_http_ignore_ssl_errors``: Ignore ssl error. (Only used if gelf_type=http)

``gelf_timeout``: Custom timeout.

Grafana OnCall
~~~~~~~~~~~~~~

https://grafana.com/docs/oncall/latest/integrations/elastalert/

HTTP POST
~~~~~~~~~

This alert type will send results to a JSON endpoint using HTTP POST. The key names are configurable so this is compatible with almost any endpoint. By default, the JSON will contain all the items from the match, unless you specify http_post_payload, in which case it will only contain those items.

Required:

``http_post_url``: The URL to POST.

Optional:

``http_post_payload``: List of keys:values to use as the content of the POST. Example - ip:clientip will map the value from the clientip index of Elasticsearch to JSON key named ip. If not defined, all the Elasticsearch keys will be sent.

``http_post_static_payload``: Key:value pairs of static parameters to be sent, along with the Elasticsearch results. Put your authentication or other information here.

``http_post_headers``: Key:value pairs of headers to be sent as part of the request.

``http_post_proxy``: URL of proxy, if required. only supports https.

``http_post_all_values``: Boolean of whether or not to include every key value pair from the match in addition to those in http_post_payload and http_post_static_payload. Defaults to True if http_post_payload is not specified, otherwise False.

``http_post_timeout``: The timeout value, in seconds, for making the post. The default is 10. If a timeout occurs, the alert will be retried next time elastalert cycles.

``http_post_ca_certs``: Set this option to ``True`` or a path to a CA cert bundle or directory (eg: ``/etc/ssl/certs/ca-certificates.crt``) to validate the SSL certificate.

``http_post_ignore_ssl_errors``: By default ElastAlert 2 will verify SSL certificate. Set this option to ``True`` if you want to ignore SSL errors.

Example usage::

    alert: post
    http_post_url: "http://example.com/api"
    http_post_payload:
      ip: clientip
    http_post_static_payload:
      apikey: abc123
    http_post_headers:
      authorization: Basic 123dr3234

HTTP POST 2
~~~~~~~~~~~

This alert type will send results to a JSON endpoint using HTTP POST. The key names are configurable so this is compatible with almost any endpoint. By default, the JSON will contain all the items from the match, unless you specify http_post_payload, in which case it will only contain those items.
This alert is a more flexible version of the HTTP Post alerter.

Required:

``http_post2_url``: The URL to POST.

Optional:

``http_post2_payload``: A JSON string or list of keys:values to use for the payload of the HTTP Post. You can use {{ field }} (Jinja2 template) in the key and the value to reference any field in the matched events (works for nested ES fields and nested payload keys). If not defined, all the Elasticsearch keys will be sent. Ex: `"description_{{ my_field }}": "Type: {{ type }}\\nSubject: {{ title }}"`. When field names use dot notation or reserved characters, _data can be used to access these fields. If _data conflicts with your top level data, use jinja_root_name to change its name.

``http_post2_raw_fields``: List of keys:values to use as the content of the POST. Example - ip:clientip will map the value from the clientip field of Elasticsearch to JSON key named ip. This field overwrite the keys with the same name in `http_post2_payload`.

``http_post2_headers``: A JSON string or list of keys:values to use for as headers of the HTTP Post. You can use {{ field }} (Jinja2 template) in the key and the value to reference any field in the matched events (works for nested fields). Ex: `"Authorization": "{{ user }}"`. Headers `"Content-Type": "application/json"` and `"Accept": "application/json;charset=utf-8"` are present by default, you can overwrite them if you think this is necessary. When field names use dot notation or reserved characters, _data can be used to access these fields. If _data conflicts with your top level data, use jinja_root_name to change its name.

``http_post2_proxy``: URL of proxy, if required. only supports https.

``http_post2_all_values``: Boolean of whether or not to include every key value pair from the match in addition to those in http_post2_payload and http_post2_static_payload. Defaults to True if http_post2_payload is not specified, otherwise False.

``http_post2_timeout``: The timeout value, in seconds, for making the post. The default is 10. If a timeout occurs, the alert will be retried next time elastalert cycles.

``http_post2_ca_certs``: Set this option to ``True`` or a path to a CA cert bundle or directory (eg: ``/etc/ssl/certs/ca-certificates.crt``) to validate the SSL certificate.

``http_post2_ignore_ssl_errors``: By default ElastAlert 2 will verify SSL certificate. Set this option to ``True`` if you want to ignore SSL errors.

.. note:: Due to how values are rendered to JSON, the http_post2_headers and http_post2_payload fields require single quotes where quotes are required for Jinja templating. This only applies when using the YAML key:value pairs. Any quotes can be used with the new JSON string format. See below for examples of how to properly use quotes as well as an example of the new JSON string formatting.

Incorrect usage with double quotes::

    alert: post2
    http_post2_url: "http://example.com/api"
    http_post2_payload:
      # this will result in an error as " is escaped to \"
      description: 'hello {{ _data["name"] }}'
      # this will result in an error as " is escaped to \"
      state: '{{ ["low","medium","high","critical"][event.severity] }}'
    http_post2_headers:
      authorization: Basic 123dr3234
      X-custom-type: '{{type}}'

Correct usage with single quotes::

    alert: post2
    http_post2_url: "http://example.com/api"
    http_post2_payload:
      description: hello {{ _data['name'] }}
      state: "{{ ['low','medium','high','critical'][event.severity] }}"
    http_post2_headers:
      authorization: Basic 123dr3234
      X-custom-type: '{{type}}'

Example usage::

    alert: post2
    http_post2_url: "http://example.com/api"
    http_post2_payload:
      description: "An event came from IP {{clientip}}"
      username: "{{user.name}}"
    http_post2_raw_fields:
      ip: clientip
    http_post2_headers:
      authorization: Basic 123dr3234
      X-custom-type: {{type}}

Example usage with json string formatting::

    alert: post2
    jinja_root_name: _new_root
    http_post2_url: "http://example.com/api"
    http_post2_payload: |
      {
        "description": "An event came from IP {{ _new_root["client.ip"] }}",
        "username": "{{ _new_root['username'] }}"
        {%- for k, v in some_field.items() -%}
        ,"{{ k }}": "changed_{{ v }}"
        {%- endfor -%}
      }
    http_post2_raw_fields:
      ip: clientip
    http_post2_headers: |
      {
        "authorization": "Basic 123dr3234",
        "X-custom-{{key}}": "{{type}}"
      }

Indexer
~~~~~~~

Description: Creates a record in an arbitrary index within an Elasticsearch or OpenSearch index.

Indexer alerter can be used to create a new alert in existing Opensearch/Elasticsearch. The alerter supports
custom fields, and observables from the alert matches and rule data.

Required:

``indexer_alert_config``: Configuration options for the alert, see example below for structure.

``customFields`` Fields must be manually added, all of them will exist in the newly created index. You can set own field or use existing field fron match (see example below for structure).

``indexer_alerts_name``: The index to use for creating the new alert records.

One of below is required:

``indexer_connection``: Options the connection details to your server instance (see example below for the required syntax Example 1).

``indexer_config``: Options for loading the connection details to your server instance from a file (see example below for the required syntax Example 2).


Example 1 usage::

    alert: indexer

    indexer_connection:
      es_host: localhost
      es_port: es_port
      ssl_show_warn: False
      use_ssl: True
      verify_certs: False
      es_username: user
      es_password: password
      indexer_alerts_name: elastalert2               # You can create own config or use global config just added ``indexer_alerts_name`` in global config

    indexer_alert_config:
      #Existing fields from match alert
      message: message
      host.name: host.name
      event.action: event.action
      event.type: event.type
      winlog.computer_name: winlog.computer_name
      winlog.event_id: winlog.event_id
      winlog.task: winlog.task
      #Enrich existing event with additional fields
      customFields:
        - name: original_time
          value: "@timestamp"
        - name: severity
          value: high
        - name: risk_score
          value: 73
        - name: description
          value: General description.

Example 2 usage::

    alert: indexer

    indexer_config: /opt/elastalert/config/config.yaml       # Uses the ElastAlert 2 global config, with an added ``indexer_alerts_name`` parameter

    indexer_alert_config:
      #Existing fields from match alert
      message: message
      host.name: host.name
      event.action: event.action
      event.type: event.type
      winlog.computer_name: winlog.computer_name
      winlog.event_id: winlog.event_id
      winlog.task: winlog.task
      #Enrich existing event with additional fields
      customFields:
        - name: original_time
          value: "@timestamp"
        - name: severity
          value: high
        - name: risk_score
          value: 73
        - name: description
          value: General description.

IRIS
~~~~
The Iris alerter can be used to create a new alert or case in `Iris IRP System <https://dfir-iris.org>`_. The alerter supports adding tags, IOCs, and context from the alert matches and rule data.

The alerter requires the following option:

``iris_host``: Address of the Iris host. Exclude https:// For example: ``iris.example.com``.

``iris_api_token``: The API key of the user you created, which will be used to initiate alerts and cases on behalf of this user.

Optional:

``iris_customer_id``: This field represents the unique identifier of the customer for whom an incident/case will be created within the system. Configure and view the existing options in the section ``Advanced -> Customers`` of your IRIS instance. The default value is: ``1``

``iris_ca_cert``: Path to custom CA certificate.

``iris_ignore_ssl_errors``: Ignore ssl error. The default value is: ``False``.

``iris_description``: Description of the alert or case. If left blank and ``iris_type`` is ``alert`` (default value) description will automatically be generated utilizing the ``alert_text``, and optionally ``alert_text_args``/``alert_text_type``, field(s) to generate a description.

``iris_overwrite_timestamp``: Should the timestamp be overridden when creating an alert. By default, the alert's creation time will be the trigger time. If you want to use the event's timestamp as the ticket creation time, set this value to ``True``. Default value is ``False``.

``iris_type``: The type of object being created. It can be either ``alert`` or ``case``. The default value is ``alert``.

``iris_case_template_id``: Case template ID, if you want to apply a pre-prepared template.

``iris_alert_note``: Note for the alert.

``iris_alert_source``: Source of the alert. Default value is ``ElastAlert2``.

``iris_alert_tags``: List of tags.

``iris_alert_status_id``: The alert status of the alert, default value is ``2``. This parameter requires an integer input.

    Possible values:

    - ``1`` - Unspecified
    - ``2`` - New
    - ``3`` - Assigned
    - ``4`` - In progress
    - ``5`` - Pending
    - ``6`` - Closed
    - ``7`` - Merged.

``iris_alert_source_link``: Your custom link, if needed.

``iris_alert_severity_id``: The severity level of the alert, default value is ``1``. This parameter requires an integer input.

    Possible values:

    - ``1`` - Unspecified
    - ``2`` - Informational
    - ``3`` - Low
    - ``4`` - Medium
    - ``5`` - High
    - ``6`` - Critical.

``iris_alert_context``: Include information from the match into the alert context. Working as key-value, where the key is your custom name and value - data from elasticsearch message.

``iris_iocs``: Description of the IOC to be added.

Example usage ``iris_iocs``:

.. code-block:: yaml

    iris_iocs:
      - ioc_value: ip
        ioc_description: Suspicious IP address
        ioc_tlp_id: 2
        ioc_type_id: 76
        ioc_tags: ipv4, ip, suspicious
      - ioc_value: username
        ioc_description: Suspicious username
        ioc_tlp_id: 1
        ioc_type_id: 3
        ioc_tags: username

A few words about ``ioc_tlp_id`` and ``ioc_type_id``. ``ioc_tlp_id`` can be of three types: ``1 - red``, ``2 - amber``, ``3 - green``. There are numerous values for ``ioc_type_id``, and you can also add your custom ones. To find the ID for the type you are interested in, refer to your Iris instance's API at 'https://example.com/manage/ioc-types/list'.

You can find complete examples of rules in the repository under the 'examples' folder.

Jira
~~~~

The Jira alerter will open a ticket on Jira whenever an alert is triggered. You must have a service account for ElastAlert 2 to connect with.
The credentials of the service account are loaded from a separate file. Credentials can either be username and password or the Personal Access Token.
The ticket number will be written to the alert pipeline, and if it is followed by an email alerter, a link will be included in the email.

This alert requires four additional options:

``jira_server``: The hostname of the Jira server.

``jira_project``: The project to open the ticket under.

``jira_issuetype``: The type of issue that the ticket will be filed as. Note that this is case sensitive.

``jira_account_file``: The path to the file which contains Jira account credentials.

  For an example Jira account file, see ``examples/rules/jira_acct.yaml``. The account file is a YAML formatted file. 

  When using user/password authentication, or when using Jira Cloud the Jira account file must contain two fields:

  ``user``: The username to authenticate with Jira.

  ``password``: The password to authenticate with Jira. Jira cloud users must specify the Jira Cloud API token for this value.

  When using a Personal Access Token, such as when using a locally hosted Jira installation, the Jira account file must contain a single field:

  ``apikey``: The Personal Access Token for authenticating with Jira.

Optional:

``jira_parent``: Specify an existing ticket that will be used as a parent to create a new subtask in it

  For example, if you have this issue hierarchy:
    Epic
    Story, Task, Bug
    Subtask

  Then:
    As a parent issue, an epic can have stories, tasks, and bugs as subtask (child issues).
    As a parent issues, task, stories and bugs can have subtasks as subtask (child issues).
    A subtask can’t have any subtask (child issues).

  Example usage::

      jira_server: "https://example.atlassian.net/"
      jira_project: "XXX"
      jira_assignee: user@example.com
      jira_issuetype: "Sub-task"
      jira_parent: "XXX-3164"

``jira_assignee``: Assigns an issue to a user.

``jira_component``: The name of the component or components to set the ticket to. This can be a single string or a list of strings. This is provided for backwards compatibility and will eventually be deprecated. It is preferable to use the plural ``jira_components`` instead.

``jira_components``: The name of the component or components to set the ticket to. This can be a single string or a list of strings.

``jira_description``: Similar to ``alert_text``, this text is prepended to the Jira description.

``jira_label``: The label or labels to add to the Jira ticket.  This can be a single string or a list of strings. This is provided for backwards compatibility and will eventually be deprecated. It is preferable to use the plural ``jira_labels`` instead.

``jira_labels``: The label or labels to add to the Jira ticket.  This can be a single string or a list of strings.

``jira_priority``: The index of the priority to set the issue to. In the Jira dropdown for priorities, 0 would represent the first priority,
1 the 2nd, etc.

``jira_watchers``: A list of user names to add as watchers on a Jira ticket. This can be a single string or a list of strings.

``jira_bump_tickets``: If true, ElastAlert 2 search for existing tickets newer than ``jira_max_age`` and comment on the ticket with
information about the alert instead of opening another ticket. ElastAlert 2 finds the existing ticket by searching by summary. If the
summary has changed or contains special characters, it may fail to find the ticket. If you are using a custom ``alert_subject``,
the two summaries must be exact matches, except by setting ``jira_ignore_in_title``, you can ignore the value of a field when searching.
For example, if the custom subject is "foo occured at bar", and "foo" is the value field X in the match, you can set ``jira_ignore_in_title``
to "X" and it will only bump tickets with "bar" in the subject. Defaults to false.

``jira_ignore_in_title``: ElastAlert 2 will attempt to remove the value for this field from the Jira subject when searching for tickets to bump.
See ``jira_bump_tickets`` description above for an example.

``jira_max_age``: If ``jira_bump_tickets`` is true, the maximum age of a ticket, in days, such that ElastAlert 2 will comment on the ticket
instead of opening a new one. Default is 30 days.

``jira_bump_not_in_statuses``: If ``jira_bump_tickets`` is true, a list of statuses the ticket must **not** be in for ElastAlert 2 to comment on
the ticket instead of opening a new one. For example, to prevent comments being added to resolved or closed tickets, set this to 'Resolved'
and 'Closed'. This option should not be set if the ``jira_bump_in_statuses`` option is set.

Example usage::

    jira_bump_not_in_statuses:
      - Resolved
      - Closed

``jira_bump_in_statuses``: If ``jira_bump_tickets`` is true, a list of statuses the ticket *must be in* for ElastAlert 2 to comment on
the ticket instead of opening a new one. For example, to only comment on 'Open' tickets  -- and thus not 'In Progress', 'Analyzing',
'Resolved', etc. tickets -- set this to 'Open'. This option should not be set if the ``jira_bump_not_in_statuses`` option is set.

Example usage::

    jira_bump_in_statuses:
      - Open

``jira_bump_only``: Only update if a ticket is found to bump.  This skips ticket creation for rules where you only want to affect existing tickets.

Example usage::

    jira_bump_only: true

``jira_transition_to``: If ``jira_bump_tickets`` is true, Transition this ticket to the given Status when bumping. Must match the text of your Jira implementation's Status field.

Example usage::

    jira_transition_to: 'Fixed'



``jira_bump_after_inactivity``: If this is set, ElastAlert 2 will only comment on tickets that have been inactive for at least this many days.
It only applies if ``jira_bump_tickets`` is true. Default is 0 days.

Arbitrary Jira fields:

ElastAlert 2 supports setting any arbitrary Jira field that your Jira issue supports. For example, if you had a custom field, called "Affected User", you can set it by providing that field name in ``snake_case`` prefixed with ``jira_``.  These fields can contain primitive strings or arrays of strings. Note that when you create a custom field in your Jira server, internally, the field is represented as ``customfield_1111``. In ElastAlert 2, you may refer to either the public facing name OR the internal representation.

In addition, if you would like to use a field in the alert as the value for a custom Jira field, use the field name plus a # symbol in front. For example, if you wanted to set a custom Jira field called "user" to the value of the field "username" from the match, you would use the following.

Example::

    jira_user: "#username"

Example usage::

    jira_arbitrary_singular_field: My Name
    jira_arbitrary_multivalue_field:
      - Name 1
      - Name 2
    jira_customfield_12345: My Custom Value
    jira_customfield_9999:
      - My Custom Value 1
      - My Custom Value 2

Lark
~~~~~~~~

Lark alerter will send notification to a predefined bot in Lark application. The body of the notification is formatted the same as with other alerters.

Required:

``lark_bot_id``:  Lark bot id.

Optional:

``lark_msgtype``:  Lark msgtype, currently only ``text`` supported.

Example usage::

    alert:
      - "lark"
    lark_bot_id: "your lark bot id"
    lark_msgtype: "text"

Matrix Hookshot
~~~~~~~~~~~~~~~

The Matrix Hookshot alerter will send a notification to a Hookshot server that's already setup within the Matrix server. The body of the notification is formatted the same as with other alerters.

See the Hookshot Webhook documentation for more information: https://matrix-org.github.io/matrix-hookshot/latest/setup/webhooks.html#webhook-handling

The alerter requires the following option:

``matrixhookshot_webhook_url``: The webhook URL that was provided to you by the hookshot bot. Ex: https://XXXXX.com/webhook/6de1f483-5c4b-4bb8-784a-f09129f45225. You can also use a list of URLs to send to multiple webhooks.

Optional:

``matrixhookshot_username``: Optional username to prepend to the text body.

``matrixhookshot_text``: Override the default alert text with custom text formatting.

``matrixhookshot_html``: Specify HTML alert content to use instead of the default alert text.

``matrixhookshot_proxy``: By default ElastAlert 2 will not use a network proxy to send notifications to Hookshot. Set this option using ``hostname:port`` if you need to use a proxy. only supports https.

``matrixhookshot_ignore_ssl_errors``: By default ElastAlert 2 will verify SSL certificate. Set this option to ``True`` if you want to ignore SSL errors.

``matrixhookshot_timeout``: You can specify a timeout value, in seconds, for making communicating with Hookshot. The default is 10. If a timeout occurs, the alert will be retried next time ElastAlert 2 cycles.

``matrixhookshot_ca_certs``: Set this option to ``True`` or a path to a CA cert bundle or directory (eg: ``/etc/ssl/certs/ca-certificates.crt``) to validate the SSL certificate.

Mattermost
~~~~~~~~~~

Mattermost alerter will send a notification to a predefined Mattermost channel. The body of the notification is formatted the same as with other alerters.

The alerter requires the following option:

``mattermost_webhook_url``: The webhook URL. Follow the instructions on https://developers.mattermost.com/integrate/webhooks/incoming/ to create an incoming webhook on your Mattermost installation.

Optional:

``mattermost_proxy``: By default ElastAlert 2 will not use a network proxy to send notifications to Mattermost. Set this option using ``hostname:port`` if you need to use a proxy. only supports https.

``mattermost_ignore_ssl_errors``: By default ElastAlert 2 will verify SSL certificate. Set this option to ``True`` if you want to ignore SSL errors.

``mattermost_username_override``: By default Mattermost will use your username when posting to the channel. Use this option to change it (free text).

``mattermost_channel_override``: Incoming webhooks have a default channel, but it can be overridden. A public channel can be specified "#other-channel", and a Direct Message with "@username".

``mattermost_emoji_override``: By default ElastAlert 2 will use the ``:ghost:`` emoji when posting to the channel. You can use a different emoji per
ElastAlert 2 rule. Any Apple emoji can be used, see http://emojipedia.org/apple/ . If mattermost_icon_url_override parameter is provided, emoji is ignored.

``mattermost_icon_url_override``: By default ElastAlert 2 will use the ``:ghost:`` emoji when posting to the channel. You can provide icon_url to use custom image.
Provide absolute address of the pciture.

``mattermost_msg_pretext``: You can set the message attachment pretext using this option.

``mattermost_msg_color``: By default the alert will be posted with the 'danger' color. You can also use 'good', 'warning', or hex color code.

``mattermost_msg_fields``: You can add fields to your Mattermost alerts using this option. You can specify the title using `title` and the text value using `value`. Additionally you can specify whether this field should be a `short` field using `short: true`. If you set `args` and `value` is a formattable string, ElastAlert 2 will format the incident key based on the provided array of fields from the rule or match.
See https://developers.mattermost.com/integrate/reference/message-attachments/#fields for more information.

Example mattermost_msg_fields::

    mattermost_msg_fields:
      - title: Stack
        value: "{0} {1}" # interpolate fields mentioned in args
        short: false
        args: ["type", "msg.status_code"] # fields from doc
      - title: Name
        value: static field
        short: false

``mattermost_title``: Sets a title for the message, this shows up as a blue text at the start of the message. Defaults to "".

``mattermost_title_link``: You can add a link in your Mattermost notification by setting this to a valid URL. Requires mattermost_title to be set. Defaults to "".

``mattermost_footer``: Add a static footer text for alert. Defaults to "".

``mattermost_footer_icon``: A Public Url for a footer icon. Defaults to "".

``mattermost_image_url``: An optional URL to an image file (GIF, JPEG, PNG, BMP, or SVG). Defaults to "".

``mattermost_thumb_url``:  An optional URL to an image file (GIF, JPEG, PNG, BMP, or SVG) that is displayed as thumbnail. Defaults to "".

``mattermost_author_name``: An optional name used to identify the author. . Defaults to "".

``mattermost_author_link``: An optional URL used to hyperlink the author_name. Defaults to "".

``mattermost_author_icon``: An optional URL used to display a 16x16 pixel icon beside the author_name. Defaults to "".

``mattermost_attach_kibana_discover_url``: Enables the attachment of the ``kibana_discover_url`` to the mattermost notification. The config ``generate_kibana_discover_url`` must also be ``True`` in order to generate the url. Defaults to ``False``.

``mattermost_kibana_discover_color``: The color of the Kibana Discover url attachment. Defaults to ``#ec4b98``.

``mattermost_kibana_discover_title``: The title of the Kibana Discover url attachment. Defaults to ``Discover in Kibana``.

``mattermost_attach_opensearch_discover_url``: Enables the attachment of the ``opensearch_discover_url`` to the mattermost notification. The config ``generate_opensearch_discover_url`` must also be ``True`` in order to generate the url. Defaults to ``False``.

``mattermost_opensearch_discover_color``: The color of the Opensearch Discover url attachment. Defaults to ``#ec4b98``.

``mattermost_opensearch_discover_title``: The title of the Opensearch Discover url attachment. Defaults to ``Discover in opensearch``.

Example mattermost_attach_kibana_discover_url, mattermost_kibana_discover_color, mattermost_kibana_discover_title::

    # (Required)
    generate_kibana_discover_url: True
    kibana_discover_app_url: "http://localhost:5601/app/discover#/"
    kibana_discover_index_pattern_id: "4babf380-c3b1-11eb-b616-1b59c2feec54"
    kibana_discover_version: "7.15"

    # (Optional)
    kibana_discover_from_timedelta:
      minutes: 10
    kibana_discover_to_timedelta:
      minutes: 10

    # (Required)
    mattermost_attach_kibana_discover_url: True

    # (Optional)
    mattermost_kibana_discover_color: "#ec4b98"
    mattermost_kibana_discover_title: "Discover in Kibana"

Example mattermost_attach_opensearch_discover_url, mattermost_kibana_discover_color, mattermost_kibana_discover_title::

    # (Required)
    generate_opensearch_discover_url: True
    opensearch_discover_app_url: "http://localhost:5601/app/discover#/"
    opensearch_discover_index_pattern_id: "4babf380-c3b1-11eb-b616-1b59c2feec54"
    opensearch_discover_version: "2.11"

    # (Optional)
    opensearch_discover_from_timedelta:
      minutes: 10
    opensearch_discover_to_timedelta:
      minutes: 10

    # (Required)
    mattermost_attach_opensearch_discover_url: True

    # (Optional)
    mattermost_opensearch_discover_color: "#ec4b98"
    mattermost_opensearch_discover_title: "Discover in opensearch"


Microsoft Teams
~~~~~~~~~~~~~~~

Microsoft Teams alerter will send a notification to a predefined Microsoft Teams channel.

The alerter requires the following options:

``ms_teams_webhook_url``: The webhook URL that includes your auth data and the ID of the channel you want to post to. Go to the Connectors
menu in your channel and configure an Incoming Webhook, then copy the resulting URL. You can use a list of URLs to send to multiple channels.

Optional:

``ms_teams_alert_summary``: MS Teams use this value for notification title, defaults to `Alert Subject <https://elastalert2.readthedocs.io/en/latest/ruletypes.html#alert-subject>`_. You can set this value with arbitrary text if you don't want to use the default.

``ms_teams_theme_color``: By default the alert will be posted without any color line. To add color, set this attribute to a HTML color value e.g. ``#ff0000`` for red.

``ms_teams_proxy``: By default ElastAlert 2 will not use a network proxy to send notifications to MS Teams. Set this option using ``hostname:port`` if you need to use a proxy. only supports https.

``ms_teams_alert_fixed_width``: By default this is ``False`` and the notification will be sent to MS Teams as-is. Teams supports a partial Markdown implementation, which means asterisk, underscore and other characters may be interpreted as Markdown. Currently, Teams does not fully implement code blocks. Setting this attribute to ``True`` will enable line by line code blocks. It is recommended to enable this to get clearer notifications in Teams.

``ms_teams_alert_facts``: You can add additional facts to your MS Teams alerts using this field. Specify the title using `name` and a value for the field or arbitrary text using `value`. 

Example ms_teams_alert_facts::

    ms_teams_alert_facts:
      - name: Host
        value: monitor.host
      - name: Status
        value: monitor.status
      - name: What to do
        value: Page your boss

``ms_teams_attach_kibana_discover_url``: Enables the attachment of the ``kibana_discover_url`` to the MS Teams notification. The config ``generate_kibana_discover_url`` must also be ``True`` in order to generate the url. Defaults to ``False``.

``ms_teams_kibana_discover_title``: The title of the Kibana Discover url attachment. Defaults to ``Discover in Kibana``.

``ms_teams_attach_opensearch_discover_url``: Enables the attachment of the ``opensearch_discover_url`` to the MS Teams notification. The config ``generate_opensearch_discover_url`` must also be ``True`` in order to generate the url. Defaults to ``False``.

``ms_teams_opensearch_discover_title``: The title of the Opensearch Discover url attachment. Defaults to ``Discover in opensearch``.

Example ms_teams_attach_kibana_discover_url, ms_teams_kibana_discover_title::

    # (Required)
    generate_kibana_discover_url: True
    kibana_discover_app_url: "http://localhost:5601/app/discover#/"
    kibana_discover_index_pattern_id: "4babf380-c3b1-11eb-b616-1b59c2feec54"
    kibana_discover_version: "7.15"

    # (Optional)
    kibana_discover_from_timedelta:
      minutes: 10
    kibana_discover_to_timedelta:
      minutes: 10

    # (Required)
    ms_teams_attach_kibana_discover_url: True

    # (Optional)
    ms_teams_kibana_discover_title: "Discover in Kibana"

Example ms_teams_attach_opensearch_discover_url, ms_teams_opensearch_discover_title::

    # (Required)
    generate_opensearch_discover_url: True
    opensearch_discover_app_url: "http://localhost:5601/app/discover#/"
    opensearch_discover_index_pattern_id: "4babf380-c3b1-11eb-b616-1b59c2feec54"
    opensearch_discover_version: "7.15"

    # (Optional)
    opensearch_discover_from_timedelta:
      minutes: 10
    opensearch_discover_to_timedelta:
      minutes: 10

    # (Required)
    ms_teams_attach_opensearch_discover_url: True

    # (Optional)
    ms_teams_opensearch_discover_title: "Discover in opensearch"

``ms_teams_ca_certs``: Set this option to ``True`` or a path to a CA cert bundle or directory (eg: ``/etc/ssl/certs/ca-certificates.crt``) to validate the SSL certificate.

``ms_teams_ignore_ssl_errors``: By default ElastAlert 2 will verify SSL certificate. Set this option to ``True`` if you want to ignore SSL errors.

Example usage::

    alert:
      - "ms_teams"
    ms_teams_theme_color: "#6600ff"
    ms_teams_webhook_url: "MS Teams Webhook URL"

Microsoft Power Automate
~~~~~~~~~~~~~~~~~~~~~~~~

Microsoft Power Automate alerter will send a notification to a predefined Microsoft Teams channel.

The alerter requires the following options:

``ms_power_automate_webhook_url``: The webhook URL provided in Power Automate, `doc Microsoft <https://support.microsoft.com/en-us/office/post-a-workflow-when-a-webhook-request-is-received-in-microsoft-teams-8ae491c7-0394-4861-ba59-055e33f75498>`_. After creating the flow select your Teams channel under "Send each adaptive card". You can use a list of URLs to send to multiple channels.

``ms_power_automate_webhook_url_from_field``: Use a field from the document that triggered the alert as the webhook. If the field cannot be found, the ``ms_power_automate_webhook_url`` value will be used as a default. 

Optional:

``ms_power_automate_summary_text_size``: By default, is set to the value ``large``. This field supports the values, default, small, medium and extraLarge.

``ms_power_automate_body_text_size``: By default, this field is not set, and has the default behavior in MS Power Automate. This field supports the values, default, small, medium, large and extraLarge.

``ms_power_automate_alert_summary``: Microsoft Power Automate use this value for notification title, defaults to `alert_subject <https://elastalert2.readthedocs.io/en/latest/alerts.html#alert-subject>`_. You can set this value with arbitrary text if you don't want to use the default.

``ms_power_automate_proxy``: By default ElastAlert 2 will not use a network proxy to send notifications to MS Teams. Set this option using ``hostname:port`` if you need to use a proxy. only supports https.

``ms_power_automate_teams_card_width_full``: By default, this is ``False`` and the notification will be sent to MS Teams without rendering full width in Microsoft Teams. Setting this attribute to ``True`` will render the alert in full width. `doc feature <https://github.com/microsoft/AdaptiveCards/issues/8102>`_.

``ms_power_automate_alert_facts``: You can add additional facts to your MS Teams alerts using this field. Specify the title using `name` and a value for the field or arbitrary text using `value`. 

Example ms_power_automate_alert_facts::

    ms_power_automate_alert_facts:
      - name: Team
        value: Teste
      - name: Level
        value: Critical 

``ms_power_automate_kibana_discover_attach_url``: Enables the attachment of the ``kibana_discover_url`` to the MS Power Automate notification. The config ``generate_kibana_discover_url`` must also be ``True`` in order to generate the url. Defaults to ``False``.

``ms_power_automate_kibana_discover_title``: The title of the Kibana Discover url attachment. Defaults to ``Discover in Kibana``.

``ms_power_automate_kibana_discover_color``: By default, the alert will be published with the ``default`` type blue if not specified. If set to ``positive``, action is displayed with a positive style (typically the button becomes accent color), If set to ``destructive``, Action is displayed with a destructive style (typically the button becomes red)

``ms_power_automate_opensearch_discover_attach_url``: Enables the attachment of the ``opensearch_discover_url`` to the MS Teams notification. The config ``generate_opensearch_discover_url`` must also be ``True`` in order to generate the url. Defaults to ``False``.

``ms_power_automate_opensearch_discover_title``: The title of the Opensearch Discover url attachment. Defaults to ``Discover in opensearch``.

``ms_power_automate_opensearch_discover_color``: By default, the alert will be published with the ``default`` type blue if not specified. If set to ``positive``, action is displayed with a positive style (typically the button becomes accent color), If set to ``destructive``, Action is displayed with a destructive style (typically the button becomes red)

Example ms_power_automate_kibana_discover_attach_url, ms_power_automate_kibana_discover_title::

    # (Required)
    generate_kibana_discover_url: True
    kibana_discover_app_url: "http://localhost:5601/app/discover#/"
    kibana_discover_index_pattern_id: "4babf380-c3b1-11eb-b616-1b59c2feec54"
    kibana_discover_version: "8.13"

    # (Optional)
    kibana_discover_from_timedelta:
      minutes: 10
    kibana_discover_to_timedelta:
      minutes: 10

    # (Required)
    ms_power_automate_kibana_discover_attach_url: True

    # (Optional)
    ms_power_automate_kibana_discover_title: "Discover in Kibana"

Example ms_power_automate_opensearch_discover_attach_url, ms_power_automate_opensearch_discover_title::

    # (Required)
    generate_opensearch_discover_url: True
    opensearch_discover_app_url: "http://localhost:5601/app/discover#/"
    opensearch_discover_index_pattern_id: "4babf380-c3b1-11eb-b616-1b59c2feec54"
    opensearch_discover_version: "7.15"

    # (Optional)
    opensearch_discover_from_timedelta:
      minutes: 10
    opensearch_discover_to_timedelta:
      minutes: 10

    # (Required)
    ms_power_automate_opensearch_discover_attach_url: True

    # (Optional)
    ms_power_automate_opensearch_discover_title: "Discover in opensearch"

``ms_power_automate_ca_certs``: Set this option to ``True`` or a path to a CA cert bundle or directory (eg: ``/etc/ssl/certs/ca-certificates.crt``) to validate the SSL certificate.

``ms_power_automate_ignore_ssl_errors``: By default ElastAlert 2 will verify SSL certificate. Set this option to ``True`` if you want to ignore SSL errors.

Example usage::

  ms_power_automate_kibana_discover_attach_url: true
  ms_power_automate_kibana_discover_title: "See More"
  ms_power_automate_kibana_discover_color: 'destructive'
  ms_power_automate_teams_card_width_full: true

  ms_power_automate_alert_facts: 
    - name: Team
      value: Teste
    - name: Level
      value: Critical  

  alert:
    - ms_power_automate

  ms_power_automate_webhook_url: >-
    webhook 

OpsGenie
~~~~~~~~

OpsGenie alerter will create an alert which can be used to notify Operations people of issues or log information. An OpsGenie ``API``
integration must be created in order to acquire the necessary ``opsgenie_key`` rule variable. Currently the OpsGenieAlerter only creates
an alert, however it could be extended to update or close existing alerts.

It is necessary for the user to create an OpsGenie Rest HTTPS API `integration page <https://docs.opsgenie.com/docs/alert-api>`_ in order to create alerts.

The OpsGenie alert requires one option:

``opsgenie_key``: The randomly generated API Integration key created by OpsGenie.

Optional:

``opsgenie_account``: The OpsGenie account to integrate with.

``opsgenie_addr``: The OpsGenie URL to to connect against, default is ``https://api.opsgenie.com/v2/alerts``. If using the EU instance of Opsgenie, the URL needs to be ``https://api.eu.opsgenie.com/v2/alerts`` for requests to be successful. The address can be formatted with fields from the first match e.g "https://api.opsgenie.com/v2/alerts/{my_alias}/close?identifierType=alias"

``opsgenie_recipients``: A list OpsGenie recipients who will be notified by the alert.

``opsgenie_recipients_args``: Map of arguments used to format opsgenie_recipients.

``opsgenie_default_recipients``: List of default recipients to notify when the formatting of opsgenie_recipients is unsuccesful.

``opsgenie_teams``: A list of OpsGenie teams to notify (useful for schedules with escalation).

``opsgenie_teams_args``: Map of arguments used to format opsgenie_teams (useful for assigning the alerts to teams based on some data).

``opsgenie_default_teams``: List of default teams to notify when the formatting of opsgenie_teams is unsuccesful.

``opsgenie_tags``: A list of tags for this alert.

``opsgenie_message``: Set the OpsGenie message to something other than the rule name. The message can be formatted with fields from the first match e.g. "Error occurred for {app_name} at {timestamp}.".

``opsgenie_description``: Set the OpsGenie description to something other than the rule body. The message can be formatted with fields from the first match e.g. "Error occurred for {app_name} at {timestamp}.".

``opsgenie_alias``: Set the OpsGenie alias. The alias can be formatted with fields from the first match e.g "{app_name} error".

``opsgenie_subject``: A string used to create the title of the OpsGenie alert. Can use Python string formatting.

``opsgenie_subject_args``: A list of fields to use to format ``opsgenie_subject`` if it contains formaters.

``opsgenie_priority``: Set the OpsGenie priority level. Possible values are P1, P2, P3, P4, P5. Can be formatted with fields from the first match e.g "P{level}"

``opsgenie_details``: Map of custom key/value pairs to include in the alert's details. The value can sourced from either fields in the first match, environment variables, or a constant value.

``opsgenie_proxy``: By default ElastAlert 2 will not use a network proxy to send notifications to OpsGenie. Set this option using ``hostname:port`` if you need to use a proxy. only supports https.

``opsgenie_source``: Set the OpsGenie source, default is `ElastAlert`. Can be formatted with fields from the first match e.g "{source} {region}"

``opsgenie_entity``: Set the OpsGenie entity. Can be formatted with fields from the first match e.g "{host_name}"

Example usage::

    opsgenie_details:
      Author: 'Bob Smith'          # constant value
      Environment: '$VAR'          # environment variable
      Message: { field: message }  # field in the first match

Example opsgenie_details with kibana_discover_url::

    # (Required)
    generate_kibana_discover_url: True
    kibana_discover_app_url: "http://localhost:5601/app/discover#/"
    kibana_discover_index_pattern_id: "4babf380-c3b1-11eb-b616-1b59c2feec54"
    kibana_discover_version: "7.15"

    # (Optional)
    kibana_discover_from_timedelta:
      minutes: 10
    kibana_discover_to_timedelta:
      minutes: 10

    # (Required)
    opsgenie_details:
      Kibana Url: { field: kibana_discover_url }
      Message: { field: message }
      Testing: 'yes'

PagerDuty
~~~~~~~~~

PagerDuty alerter will trigger an incident to a predefined PagerDuty service. The body of the notification is formatted the same as with other alerters.

The alerter requires the following option:

``pagerduty_service_key``: Integration Key generated after creating a service with the 'Use our API directly' option at Integration Settings

``pagerduty_client_name``: The name of the monitoring client that is triggering this event.

``pagerduty_event_type``: Any of the following: `trigger`, `resolve`, or `acknowledge`. (Optional, defaults to `trigger`)

Optional:

``alert_subject``: If set, this will be used as the Incident description within PagerDuty. If not set, ElastAlert 2 will default to using the rule name of the alert for the incident.

``alert_subject_args``: If set, and  ``alert_subject`` is a formattable string, ElastAlert 2 will format the incident key based on the provided array of fields from the rule or match.

``pagerduty_incident_key``: If not set PagerDuty will trigger a new incident for each alert sent. If set to a unique string per rule PagerDuty will identify the incident that this event should be applied.
If there's no open (i.e. unresolved) incident with this key, a new one will be created. If there's already an open incident with a matching key, this event will be appended to that incident's log.

``pagerduty_incident_key_args``: If set, and ``pagerduty_incident_key`` is a formattable string, ElastAlert 2 will format the incident key based on the provided array of fields from the rule or match.

``pagerduty_proxy``: By default ElastAlert 2 will not use a network proxy to send notifications to PagerDuty. Set this option using ``hostname:port`` if you need to use a proxy. only supports https.

``pagerduty_ca_certs``: Set this option to ``True`` or a path to a CA cert bundle or directory (eg: ``/etc/ssl/certs/ca-certificates.crt``) to validate the SSL certificate.

``pagerduty_ignore_ssl_errors``: By default ElastAlert 2 will verify SSL certificate. Set this option to ``True`` if you want to ignore SSL errors.

V2 API Options (Optional):

These options are specific to the PagerDuty V2 API

See https://developer.pagerduty.com/api-reference/b3A6Mjc0ODI2Nw-send-an-event-to-pager-duty

``pagerduty_api_version``: Defaults to `v1`.  Set to `v2` to enable the PagerDuty V2 Event API.

``pagerduty_v2_payload_class``: Sets the class of the payload. (the event type in PagerDuty)

``pagerduty_v2_payload_class_args``: If set, and ``pagerduty_v2_payload_class`` is a formattable string, ElastAlert 2 will format the class based on the provided array of fields from the rule or match.

``pagerduty_v2_payload_component``: Sets the component of the payload. (what program/interface/etc the event came from)

``pagerduty_v2_payload_component_args``: If set, and ``pagerduty_v2_payload_component`` is a formattable string, ElastAlert 2 will format the component based on the provided array of fields from the rule or match.

``pagerduty_v2_payload_group``: Sets the logical grouping (e.g. app-stack)

``pagerduty_v2_payload_group_args``: If set, and ``pagerduty_v2_payload_group`` is a formattable string, ElastAlert 2 will format the group based on the provided array of fields from the rule or match.

``pagerduty_v2_payload_severity``: Sets the severity of the page. (defaults to `critical`, valid options: `critical`, `error`, `warning`, `info`)

``pagerduty_v2_payload_source``: Sets the source of the event, preferably the hostname or fqdn.

``pagerduty_v2_payload_source_args``: If set, and ``pagerduty_v2_payload_source`` is a formattable string, ElastAlert 2 will format the source based on the provided array of fields from the rule or match.

``pagerduty_v2_payload_custom_details``: List of keys:values to use as the content of the custom_details payload. For each key:value, it first attempts to map the provided value by checking if it exists as a key in an elastalert match. If a match is found, it assigns the corresponding value from the elastalert match. If no match is found, it then defaults to using the original provided value directly.

``pagerduty_v2_payload_include_all_info``: If True, this will include the entire Elasticsearch document as a custom detail field called "information" in the PagerDuty alert.

PagerTree
~~~~~~~~~

PagerTree alerter will trigger an incident to a predefined PagerTree integration url.

The alerter requires the following options:

``pagertree_integration_url``: URL generated by PagerTree for the integration.

``pagertree_proxy``: By default ElastAlert 2 will not use a network proxy to send notifications to PagerTree. Set this option using ``hostname:port`` if you need to use a proxy. only supports https.

Example usage::

    alert:
      - "pagertree"
    pagertree_integration_url: "PagerTree Integration URL"

Rocket.Chat
~~~~~~~~~~~

Rocket.Chat alerter will send a notification to a predefined channel. The body of the notification is formatted the same as with other alerters.
https://developer.rocket.chat/api/rest-api/methods/chat/postmessage

The alerter requires the following option:

``rocket_chat_webhook_url``: The webhook URL that includes your auth data and the ID of the channel (room) you want to post to. You can use a list of URLs to send to multiple channels.

Optional:

``rocket_chat_username_override``: By default Rocket.Chat will use username defined in Integration when posting to the channel. Use this option to change it (free text).

``rocket_chat_channel_override``: Incoming webhooks have a default channel, but it can be overridden. A public channel can be specified “#other-channel”, and a Direct Message with “@username”.

``rocket_chat_emoji_override``: By default ElastAlert 2 will use the :ghost: emoji when posting to the channel. You can use a different emoji per
ElastAlert 2 rule. Any Apple emoji can be used, see http://emojipedia.org/apple/ .

``rocket_chat_msg_color``: By default the alert will be posted with the ‘danger’ color. You can also use ‘good’ or ‘warning’ colors.

``rocket_chat_text_string``: Notification message you want to add.

``rocket_chat_proxy``: By default ElastAlert 2 will not use a network proxy to send notifications to Rocket.Chat. Set this option using ``hostname:port`` if you need to use a proxy. only supports https.

``rocket_chat_ca_certs``: Set this option to ``True`` or a path to a CA cert bundle or directory (eg: ``/etc/ssl/certs/ca-certificates.crt``) to validate the SSL certificate.

``rocket_chat_ignore_ssl_errors``: By default ElastAlert 2 will verify SSL certificate. Set this option to ``True`` if you want to ignore SSL errors.

``rocket_chat_timeout``: You can specify a timeout value, in seconds, for making communicating with Rocket.Chat. The default is 10. If a timeout occurs, the alert will be retried next time ElastAlert 2 cycles.

``rocket_chat_attach_kibana_discover_url``: Enables the attachment of the ``kibana_discover_url`` to the Rocket.Chat notification. The config ``generate_kibana_discover_url`` must also be ``True`` in order to generate the url. Defaults to ``False``.

``rocket_chat_kibana_discover_color``: The color of the Kibana Discover url attachment. Defaults to ``#ec4b98``.

``rocket_chat_kibana_discover_title``: The title of the Kibana Discover url attachment. Defaults to ``Discover in Kibana``.

``rocket_chat_attach_opensearch_discover_url``: Enables the attachment of the ``opensearch_discover_url`` to the Rocket.Chat notification. The config ``generate_opensearch_discover_url`` must also be ``True`` in order to generate the url. Defaults to ``False``.

``rocket_chat_opensearch_discover_color``: The color of the Opensearch Discover url attachment. Defaults to ``#ec4b98``.

``rocket_chat_opensearch_discover_title``: The title of the Opensearch Discover url attachment. Defaults to ``Discover in opensearch``.

Example rocket_chat_attach_kibana_discover_url, rocket_chat_kibana_discover_color, rocket_chat_kibana_discover_title::

    # (Required)
    generate_kibana_discover_url: True
    kibana_discover_app_url: "http://localhost:5601/app/discover#/"
    kibana_discover_index_pattern_id: "4babf380-c3b1-11eb-b616-1b59c2feec54"
    kibana_discover_version: "7.15"

    # (Optional)
    kibana_discover_from_timedelta:
      minutes: 10
    kibana_discover_to_timedelta:
      minutes: 10

    # (Required)
    rocket_chat_attach_kibana_discover_url: True

    # (Optional)
    rocket_chat_kibana_discover_color: "#ec4b98"
    rocket_chat_kibana_discover_title: "Discover in Kibana"

Example rocket_chat_attach_opensearch_discover_url, rocket_chat_opensearch_discover_color, rocket_chat_opensearch_discover_title::

    # (Required)
    generate_opensearch_discover_url: True
    opensearch_discover_app_url: "http://localhost:5601/app/discover#/"
    opensearch_discover_index_pattern_id: "4babf380-c3b1-11eb-b616-1b59c2feec54"
    opensearch_discover_version: "2.11"

    # (Optional)
    opensearch_discover_from_timedelta:
      minutes: 10
    opensearch_discover_to_timedelta:
      minutes: 10

    # (Required)
    rocket_chat_attach_opensearch_discover_url: True

    # (Optional)
    rocket_chat_opensearch_discover_color: "#ec4b98"
    rocket_chat_opensearch_discover_title: "Discover in opensearch"

``rocket_chat_alert_fields``: You can add additional fields to your Rocket.Chat alerts using this field. Specify the title using `title` and a value for the field using `value`. Additionally you can specify whether or not this field should be a `short` field using `short: true`.

Example rocket_chat_alert_fields::

    rocket_chat_alert_fields:
      - title: Host
        value: monitor.host
        short: true
      - title: Status
        value: monitor.status
        short: true
      - title: Zone
        value: beat.name
        short: true

Squadcast
~~~~~~~~~

Alerts can be sent to Squadcast using the `http post` method described above and Squadcast will process it and send Phone, SMS, Email and Push notifications to the relevant person(s) and let them take actions.

Configuration variables in rules YAML file::

    alert: post
    http_post_url: <ElastAlert 2 Webhook URL copied from Squadcast dashboard>
    http_post_static_payload:
      Title: <Incident Title>
    http_post_all_values: true

For more details, you can refer the `Squadcast documentation <https://support.squadcast.com/integrations/alert-source-integrations-native/elastalert>`_.

ServiceNow
~~~~~~~~~~

The ServiceNow alerter will create a new Incident in ServiceNow. The body of the notification is formatted the same as with other alerters.

The alerter requires the following options:

``servicenow_rest_url``: The ServiceNow RestApi url, this will look like `TableAPI <https://developer.servicenow.com/dev.do#!/reference/api/orlando/rest/c_TableAPI#r_TableAPI-POST>`_.

``username``: The ServiceNow Username to access the api.

``password``: The ServiceNow password to access the api.

``short_description``: The ServiceNow password to access the api.

``comments``: Comments to be attached to the incident, this is the equivilant of work notes.

``assignment_group``: The group to assign the incident to.

``category``: The category to attach the incident to, use an existing category.

``subcategory``: The subcategory to attach the incident to, use an existing subcategory.

``cmdb_ci``: The configuration item to attach the incident to.

``caller_id``: The caller id (email address) of the user that created the incident (elastalert@somewhere.com).


Optional:

``servicenow_proxy``: By default ElastAlert 2 will not use a network proxy to send notifications to ServiceNow. Set this option using ``hostname:port`` if you need to use a proxy. only supports https.

``servicenow_impact``: An integer 1, 2, or 3 representing high, medium, and low respectively. This measures the effect of an incident on business processes.

``servicenow_urgency``: An integer 1, 2, or 3 representing high, medium, and low respecitvely. This measures how long this incident can be delayed until there is a significant business impact.

Example usage::

    alert:
      - "servicenow"
    servicenow_rest_url: "servicenow rest url"
    username: "user"
    password: "password"
    short_description: "xxxxxx"
    comments: "xxxxxx"
    assignment_group: "xxxxxx"
    category: "xxxxxx"
    subcategory: "xxxxxx"
    cmdb_ci: "xxxxxx"
    caller_id: "xxxxxx"
    servicenow_impact: 1
    servicenow_urgency: 3

Arbitrary ServiceNow fields:

ElastAlert 2 supports setting any arbitrary ServiceNow field that your ServiceNow instance supports. Additional fields must be specified in a `service_now_additional_fields` stanza. For example, if you had a custom field, called "Affected User", you can set it by providing that field name and value. The field needs to be specified using the Column Name not the Display Name. Custom fields in ServiceNow usually have the prefix ``u_`` to distinguish them from out of the box fields. 

Example usage::

    service_now_additional_fields:
        u_affected_user: 'Sample User'
        u_affected_site: 'Sample Location'

Slack
~~~~~

Slack alerter will send a notification to a predefined Slack channel. The body of the notification is formatted the same as with other alerters.

The alerter requires the following option:

``slack_webhook_url``: The webhook URL that includes your auth data and the ID of the channel (room) you want to post to. Go to the Incoming Webhooks
section in your Slack account https://XXXXX.slack.com/services/new/incoming-webhook , choose the channel, click 'Add Incoming Webhooks Integration'
and copy the resulting URL. You can use a list of URLs to send to multiple channels.

Optional:

``slack_username_override``: By default Slack will use your username when posting to the channel. Use this option to change it (free text).

``slack_channel_override``: Incoming webhooks have a default channel, but it can be overridden. A public channel can be specified "#other-channel", and a Direct Message with "@username".

``slack_emoji_override``: By default ElastAlert 2 will use the ``:ghost:`` emoji when posting to the channel. You can use a different emoji per
ElastAlert 2 rule. Any Apple emoji can be used, see http://emojipedia.org/apple/ . If slack_icon_url_override parameter is provided, emoji is ignored.

``slack_icon_url_override``: By default ElastAlert 2 will use the ``:ghost:`` emoji when posting to the channel. You can provide icon_url to use custom image.
Provide absolute address of the pciture.

``slack_msg_color``: By default the alert will be posted with the 'danger' color. You can also use 'good' or 'warning' colors.

``slack_parse_override``: By default the notification message is escaped 'none'. You can also use 'full'.

``slack_text_string``: Notification message you want to add.

``slack_proxy``: By default ElastAlert 2 will not use a network proxy to send notifications to Slack. Set this option using ``hostname:port`` if you need to use a proxy. only supports https.

``slack_alert_fields``: You can add additional fields to your slack alerts using this field. Specify the title using `title` and a value for the field using `value`. Additionally you can specify whether or not this field should be a `short` field using `short: true`.

Example slack_alert_fields::

    slack_alert_fields:
      - title: Host
        value: monitor.host
        short: true
      - title: Status
        value: monitor.status
        short: true
      - title: Zone
        value: beat.name
        short: true

``slack_ignore_ssl_errors``: By default ElastAlert 2 will verify SSL certificate. Set this option to ``True`` if you want to ignore SSL errors.

``slack_title``: Sets a title for the message, this shows up as a blue text at the start of the message

``slack_title_link``: You can add a link in your Slack notification by setting this to a valid URL. Requires slack_title to be set.

``slack_timeout``: You can specify a timeout value, in seconds, for making communicating with Slack. The default is 10. If a timeout occurs, the alert will be retried next time ElastAlert 2 cycles.

``slack_attach_kibana_discover_url``: Enables the attachment of the ``kibana_discover_url`` to the slack notification. The config ``generate_kibana_discover_url`` must also be ``True`` in order to generate the url. Defaults to ``False``.

``slack_kibana_discover_color``: The color of the Kibana Discover url attachment. Defaults to ``#ec4b98``.

``slack_kibana_discover_title``: The title of the Kibana Discover url attachment. Defaults to ``Discover in Kibana``.

``slack_attach_opensearch_discover_url``: Enables the attachment of the ``opensearch_discover_url`` to the slack notification. The config ``generate_opensearch_discover_url`` must also be ``True`` in order to generate the url. Defaults to ``False``.

``slack_opensearch_discover_color``: The color of the Opensearch Discover url attachment. Defaults to ``#ec4b98``.

``slack_opensearch_discover_title``: The title of the Opensearch Discover url attachment. Defaults to ``Discover in Opensearch``.

Example slack_attach_kibana_discover_url, slack_kibana_discover_color, slack_kibana_discover_title::

    # (Required)
    generate_kibana_discover_url: True
    kibana_discover_app_url: "http://localhost:5601/app/discover#/"
    kibana_discover_index_pattern_id: "4babf380-c3b1-11eb-b616-1b59c2feec54"
    kibana_discover_version: "7.15"

    # (Optional)
    kibana_discover_from_timedelta:
      minutes: 10
    kibana_discover_to_timedelta:
      minutes: 10

    # (Required)
    slack_attach_kibana_discover_url: True

    # (Optional)
    slack_kibana_discover_color: "#ec4b98"
    slack_kibana_discover_title: "Discover in Kibana"

Example slack_attach_opensearch_discover_url, slack_opensearch_discover_color, slack_opensearch_discover_title::

    # (Required)
    generate_opensearch_discover_url: True
    opensearch_discover_app_url: "http://localhost:5601/app/discover#/"
    opensearch_discover_index_pattern_id: "4babf380-c3b1-11eb-b616-1b59c2feec54"
    opensearch_discover_version: "7.15"

    # (Optional)
    opensearch_discover_from_timedelta:
      minutes: 10
    opensearch_discover_to_timedelta:
      minutes: 10

    # (Required)
    slack_attach_opensearch_discover_url: True

    # (Optional)
    slack_opensearch_discover_color: "#ec4b98"
    slack_opensearch_discover_title: "Discover in opensearch"

``slack_ca_certs``: Set this option to ``True`` or a path to a CA cert bundle or directory (eg: ``/etc/ssl/certs/ca-certificates.crt``) to validate the SSL certificate.

``slack_footer``: Add a static footer text for alert. Defaults to "".

``slack_footer_icon``: A Public Url for a footer icon. Defaults to "".

``slack_image_url``: An optional URL to an image file (GIF, JPEG, PNG, BMP, or SVG). Defaults to "".

``slack_thumb_url``:  An optional URL to an image file (GIF, JPEG, PNG, BMP, or SVG) that is displayed as thumbnail. Defaults to "".

``slack_author_name``: An optional name used to identify the author. Defaults to "".

``slack_author_link``: An optional URL used to hyperlink the author_name. Defaults to "".

``slack_author_icon``: An optional URL used to display a 16x16 pixel icon beside the author_name. Defaults to "".

``slack_msg_pretext``: You can set the message attachment pretext using this option. Defaults to "".

``slack_attach_jira_ticket_url``: Add url to the jira ticket created. Only works if the Jira alert runs before Slack alert. Set the field to ``True`` in order to generate the url. Defaults to ``False``.

``slack_jira_ticket_color``: The color of the Jira Ticket url attachment. Defaults to ``#ec4b98``.

``slack_jira_ticket_title``: The title of the Jira Ticket url attachment. Defaults to ``Jira Ticket``.


SMSEagle
~~~~~~~~

SMSEagle alerter will send API requests to SMSEagle device and then forward it as an SMS or Call, depending on your configuration.

The alerter requires the following option:

``smseagle_url``: Address of your SMSEagle device, e.g. http://192.168.1.101

``smseagle_token``: API access token (per user, can be generated in menu Users > Access to API)

``smseagle_message_type``: Message/call type to send/queue. Available values: sms, ring, tts, tts_adv respectively for SMS, Ring call, TTS call and Advanced TTS call.

Requires one of:

``smseagle_to``: Phone number(s) to which you want to send a message

``smseagle_contacts``: Name(s) of contact(s) from the SMSEagle Phonebook to which you want to send a message

``smseagle_groups``: Name(s) of group(s) from the SMSEagle Phonebook to which you want to send a message

Optional:

``smseagle_duration``: Call duration, required for Ring, TTS and Advanced TTS call. Default value: 10

``smseagle_voice_id``: ID of the voice model, required for Advanced TTS call. Default value: 1

``smseagle_text``: Override notification text with a custom one

Example usage::

    alert:
      - "smseagle"
    smseagle_url: "https://192.168.1.101"
    smseagle_token: "123abc456def789"
    smseagle_message_type: "sms"
    smseagle_to: ["+123456789", "987654321"]
    smseagle_contacts: [2, 7]


Splunk On-Call (Formerly VictorOps)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Splunk On-Call (Formerly VictorOps) alerter will trigger an incident to a predefined Splunk On-Call (Formerly VictorOps) routing key. The body of the notification is formatted the same as with other alerters.

The alerter requires the following options:

``victorops_api_key``: API key generated under the 'REST Endpoint' in the Integrations settings.

``victorops_routing_key``: Splunk On-Call (Formerly VictorOps) routing key to route the alert to.

``victorops_message_type``: Splunk On-Call (Formerly VictorOps) field to specify severity level. Must be one of the following: INFO, WARNING, ACKNOWLEDGEMENT, CRITICAL, RECOVERY

Optional:

``victorops_entity_id``: The identity of the incident used by Splunk On-Call (Formerly VictorOps) to correlate incidents throughout the alert lifecycle. If not defined, Splunk On-Call (Formerly VictorOps) will assign a random string to each alert.

``victorops_entity_display_name``: Human-readable name of alerting entity to summarize incidents without affecting the life-cycle workflow. Will use ``alert_subject`` if not set.

``victorops_proxy``: By default ElastAlert 2 will not use a network proxy to send notifications to Splunk On-Call (Formerly VictorOps). Set this option using ``hostname:port`` if you need to use a proxy. only supports https.

Example usage::

    alert:
      - "victorops"
    victorops_api_key: "VictorOps API Key"
    victorops_routing_key: "VictorOps routing Key"
    victorops_message_type: "INFO"

Stomp
~~~~~

This alert type will use the STOMP protocol in order to push a message to a broker like ActiveMQ or RabbitMQ. The message body is a JSON string containing the alert details.
The default values will work with a pristine ActiveMQ installation.

The alerter requires the following options:

``stomp_hostname``: The STOMP host to use, defaults to ``localhost``.

``stomp_hostport``: The STOMP port to use, defaults to ``61613``.

``stomp_login``: The STOMP login to use, defaults to ``admin``.

``stomp_password``: The STOMP password to use, defaults to ``admin``.

Optional:

``stomp_destination``: The STOMP destination to use, defaults to ``/queue/ALERT``

The stomp_destination field depends on the broker, the /queue/ALERT example is the nomenclature used by ActiveMQ. Each broker has its own logic.

Example usage::

    alert:
      - "stomp"
    stomp_hostname: "localhost"
    stomp_hostport: "61613"
    stomp_login: "admin"
    stomp_password: "admin"
    stomp_destination: "/queue/ALERT"

Telegram
~~~~~~~~
Telegram alerter will send a notification to a predefined Telegram username or channel. The body of the notification is formatted the same as with other alerters.

The alerter requires the following two options:

``telegram_bot_token``: The token is a string along the lines of ``110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw`` that will be required to authorize the bot and send requests to the Bot API. You can learn about obtaining tokens and generating new ones in this document https://core.telegram.org/bots#6-botfather

``telegram_room_id``: Unique identifier for the target chat or username of the target channel using telegram chat_id (in the format "-xxxxxxxx")

Optional:

``telegram_api_url``: Custom domain to call Telegram Bot API. Default to api.telegram.org

``telegram_proxy``: By default ElastAlert 2 will not use a network proxy to send notifications to Telegram. Set this option using ``hostname:port`` if you need to use a proxy. only supports https.

``telegram_proxy_login``: The Telegram proxy auth username.

``telegram_proxy_pass``: The Telegram proxy auth password.

``telegram_parse_mode``: The Telegram parsing mode, which determines the format of the alert text body. Possible values are ``markdown``, ``markdownV2``, ``html``. Defaults to ``markdown``.

``telegram_thread_id``: Unique identifier for the target thread of supergroup/forum using telegram message_thread_id (Optional, positive integer value, no default).

Example usage::

    alert:
      - "telegram"
    telegram_bot_token: "bot_token"
    telegram_room_id: "chat_id"


Tencent SMS
~~~~~~~~~~~

Required:

``tencent_sms_secret_id``: ``SecretID`` is used to identify the API caller.

``tencent_sms_secret_key``: ``SecretKey`` is used to encrypt the string to sign that can be verified on the server. You should keep it private and avoid disclosure.

``tencent_sms_sdk_appid``: SMS application ID, which is the `SdkAppId` generated after an application is added in the `SMS console <https://console.cloud.tencent.com/smsv2>`_, such as 1400006666

``tencent_sms_to_number``: Target mobile number in the E.164 standard (+[country/region code][mobile number])

Example: +8613711112222, which has a + sign followed by 86 (country/region code) and then by 13711112222 (mobile number). Up to 200 mobile numbers are supported

``tencent_sms_template_id``: Template ID. You must enter the ID of an approved template, which can be viewed in the `SMS console <https://console.cloud.tencent.com/smsv2>`_. 

If you need to send SMS messages to global mobile numbers, you can only use a Global SMS template.

Optional:

``tencent_sms_sign_name``: Content of the SMS signature, which should be encoded in UTF-8. You must enter an approved signature, such as Tencent Cloud. The signature information can be viewed in the SMS console.
Note: this parameter is required for Mainland China SMS.

``tencent_sms_region``: Region parameter, which is used to identify the region(`Mainland China <https://intl.cloud.tencent.com/document/api/382/40466#region-list>`_ or
`Global <https://cloud.tencent.com/document/api/382/52071#.E5.9C.B0.E5.9F.9F.E5.88.97.E8.A1.A8>`_) to which the data you want to work with belongs.

``tencent_sms_template_parm``: The number of template parameters needs to be consistent with the number of variables of the template corresponding to TemplateId.  
this value format by `rfc6901 <https://datatracker.ietf.org/doc/html/rfc6901>`_

.. code-block:: json

    {
      "_index" : "tmec"
      "_type" : "fluentd",
      "_id" : "PeXLrnsBvusb3d0w6dUl",
      "_score" : 1.0,
      "_source" : {
        "kubernetes" : {
          "host" : "9.134.191.187",
          "pod_id" : "66ba4e5a-1ad2-4655-9a8e-cffb6b942559",
          "labels" : {
            "release" : "nginx",
            "pod-template-hash" : "6bd96d6f74"
          },
          "namespace_name" : "app",
          "pod_name" : "app.nginx-6bd96d6f74-2ts4x"
        },
        "time" : "2021-09-04T03:13:24.192875Z",
        "message" : "2021-09-03T14:34:08+0000|INFO|vector eps : 192.168.0.2:10000,",
      }
    }


.. code-block:: yaml

    tencent_sms_template_id: "1123835"
    tencent_sms_template_parm:
      - "/kubernetes/pod_name"




TheHive
~~~~~~~

TheHive alerter can be used to create a new alert in TheHive. The alerter supports adding tags,
custom fields, and observables from the alert matches and rule data.

Required:

``hive_connection``: The connection details to your instance (see example below for the required syntax).
Only ``hive_apikey`` is required, ``hive_host`` and ``hive_port`` default to ``http://localhost`` and
``9000`` respectively.

``hive_alert_config``: Configuration options for the alert, see example below for structure.

``source``: Text content to use for TheHive event's "source" field. See the optional ``source_args`` parameter for dynamically formatting this content with dynamic lookup values.

``type`` Text content to use for TheHive event's "type" field. See the optional ``type_args`` parameter for dynamically formatting this content with dynamic lookup values.

Optional:

``tags`` can be populated from the matched record, using the same syntax used in ``alert_text_args``.
If a record doesn't contain the specified value, the rule itself will be examined for the tag. If
this doesn't contain the tag either, the tag is attached without modification to the alert. For
aggregated alerts, all matches are examined individually, and tags generated for each one. All tags
are then attached to the same alert.

``customFields`` can also be populated from rule fields as well as matched results. Custom fields
are only populated once. If an alert is an aggregated alert, the custom field values will be populated
using the first matched record, before checking the rule. If neither matches, the ``customField.value``
will be used directly.

``hive_observable_data_mapping``: If needed, matched data fields can be mapped to TheHive
observable types using the same syntax as ``customFields``, described above. The algorithm used to populate
the observable value is similar to the one used to populate the ``tags``, including the behaviour for aggregated alerts.
The tlp, message, and tags fields are optional for each observable. If not specified, the tlp field is given a default value of 2.

``hive_proxies``: Proxy configuration.

``hive_verify``: Whether or not to enable SSL certificate validation. Defaults to False.

``description_args``: can be used to format the description field with additional rule and match field lookups. Note that the description will be initially populated from the ElastAlert 2 default ``alert_text`` fields, including any defined ``alert_text_args``. See the "Alert Content" section for more information on the default formatting.

``description_missing_value``: Text to replace any match field not found when formatting the ``description``. Defaults to ``<MISSING VALUE>``.

``source_args``: List of parameters to format into the ``source`` text content, with values originating from the first match event.

``title``: Text content to use for TheHive event's "title" field. This will override the default alert title generated from the ``alert_subject`` and associated arg parameters. See the "Alert Subject" section for more information on the default formatting.

``title_args``: List of additional args to format against the "title" content. If the title argument is not provided then these optional arguments will be formatted against the already formatted title generated from the ``alert_subject`` and related parameters. This means that a two-phased formatting potentially could be utilized in very specific configuration scenarios.  See the "Alert Subject" section for more information on the default formatting. The values will be used from the first match event.

``type_args``: List of parameters to format into the ``type`` text content, with values originating from the first match event.

Example usage::

    alert: hivealerter

    hive_connection:
      hive_host: http://localhost
      hive_port: <hive_port>
      hive_apikey: <hive_apikey>
      hive_proxies:
        http: ''
        https: ''

    hive_alert_config:
      customFields:
        - name: example
          type: string
          value: example
      follow: True
      severity: 2
      status: 'New'
      source: 'src-{}'
      source_args: [ data.source ]
      description_args: [ name, description]
      description: '{0} : {1}'
      tags: ['tag1', 'tag2']
      title: 'Title {}'
      title_args: [ data.title ]
      tlp: 3
      type: 'type-{}'
      type_args: [ data.type ]

    hive_observable_data_mapping:
      - domain: agent.hostname
        tlp: 1
        tags: ['tag1', 'tag2']
        message: 'agent hostname'
      - domain: response.domain
        tlp: 2
        tags: ['tag3']
      - ip: client.ip

Twilio
~~~~~~

The Twilio alerter will send an alert to a mobile phone as an SMS from your Twilio
phone number. The SMS will contain the alert name. You may use either Twilio SMS
or Twilio Copilot to send the message, controlled by the ``twilio_use_copilot``
option.

Note that when Twilio Copilot *is* used the ``twilio_message_service_sid``
option is required. Likewise, when *not* using Twilio Copilot, the
``twilio_from_number`` option is required.

The alerter requires the following options:

``twilio_account_sid``: The SID of your Twilio account.

``twilio_auth_token``: Auth token associated with your Twilio account.

``twilio_to_number``: The phone number where you would like to send the alert.

Either one of
 * ``twilio_from_number``: The Twilio phone number from which the alert will be sent.
 * ``twilio_message_service_sid``: The SID of your Twilio message service.

Optional:

``twilio_use_copilot``: Whether or not to use Twilio Copilot, False by default.

Example with Copilot usage::

    alert:
      - "twilio"
    twilio_use_copilot: True
    twilio_to_number: "0123456789"
    twilio_auth_token: "abcdefghijklmnopqrstuvwxyz012345"
    twilio_account_sid: "ABCDEFGHIJKLMNOPQRSTUVWXYZ01234567"
    twilio_message_service_sid: "ABCDEFGHIJKLMNOPQRSTUVWXYZ01234567"

Example with SMS usage::

    alert:
      - "twilio"
    twilio_to_number: "0123456789"
    twilio_from_number: "9876543210"
    twilio_auth_token: "abcdefghijklmnopqrstuvwxyz012345"
    twilio_account_sid: "ABCDEFGHIJKLMNOPQRSTUVWXYZ01234567"

Webex Webhook
~~~~~~~~~~~~~

Webex Webhook alerter will send notification to a predefined incoming webhook in Webex application. The body of the notification is formatted the same as with other alerters.

Official Webex incoming webhook documentation: https://apphub.webex.com/applications/incoming-webhooks-cisco-systems-38054-23307-75252

Required:

``webex_webhook_id``:  Webex webhook ID.
``webex_webhook_msgtype``:  Webex webhook message format. Can be ``text`` or ``markdown``. Defaults to ``text``.

Example usage::

    alert_text: "**{0}** - ALERT on host {1}"
    alert_text_args:
      - name
      - hostname
    alert:
      - webex_webhook
    alert_text_type: alert_text_only
    webex_webhook_id: "your webex incoming webhook id"
    webex_webhook: "markdown"

WorkWechat
~~~~~~~~~~

WorkWechat alerter will send notification to a predefined bot in WorkWechat application. The body of the notification is formatted the same as with other alerters.

Required:

``work_wechat_bot_id``:  WorkWechat bot id.
``work_wechat_msgtype``:  WorkWechat msgtype. default to ``text``. ``markdown``

Example usage::

    alert:
      - "workwechat"
    work_wechat_bot_id: "your workwechat bot id"
    work_wechat_msgtype: "text"

Zabbix
~~~~~~

Zabbix will send notification to a Zabbix server. The item in the host specified receive a 1 value for each hit. For example, if the elastic query produce 3 hits in the last execution of ElastAlert 2, three '1' (integer) values will be send from elastalert to Zabbix Server. If the query have 0 hits, any value will be sent.

Required:

``zbx_sender_host``: The address where zabbix server is running, defaults to ``'localhost'``.

``zbx_sender_port``: The port where zabbix server is listenning, defaults to ``10051``.

``zbx_host_from_field``: This field allows to specify ``zbx_host`` value from the available terms. Defaults to ``False``.

``zbx_host``: This field setup the host in zabbix that receives the value sent by ElastAlert 2.

``zbx_key``: This field setup the key in the host that receives the value sent by ElastAlert 2.

Example usage::

    alert:
      - "zabbix"
    zbx_sender_host: "zabbix-server"
    zbx_sender_port: 10051
    zbx_host: "test001"
    zbx_key: "sender_load1"

To specify ``zbx_host`` depending on the available elasticsearch field, zabbix alerter has ``zbx_host_from_field`` option.

Example usage::

    alert:
      - "zabbix"
    zbx_sender_host: "zabbix-server"
    zbx_sender_port: 10051
    zbx_host_from_field: True 
    zbx_host: "hostname"
    zbx_key: "sender_load1"

where ``hostname`` is the available elasticsearch field.

YZJ
~~~~~~~

YZJ will send notification to a YZJ application. The body of the notification is formatted the same as with other alerters.

Required:

``yzj_token``:  The request token.

Optional:

``yzj_webhook_url``:  The webhook URL.

``yzj_type``: Default 0, send text message. https://www.yunzhijia.com/opendocs/docs.html#/server-api/im/index?id=%e7%be%a4%e7%bb%84%e6%9c%ba%e5%99%a8%e4%ba%ba

``yzj_proxy``: By default ElastAlert 2 will not use a network proxy to send notifications to YZJ. Set this option using ``hostname:port`` if you need to use a proxy. only supports https.

``yzj_custom_loc``: The YZJ custom net location, include domain name and port, like: www.xxxx.com:80.


Example usage::

    alert:
    - "yzj"
    yzj_token: "token"


Flashduty
~~~~~~~~~~~~~

Flashduty alerter will send notification to a Flashduty application. The body of the notification formatted the same as with other alerters.

Required:

``flashduty_integration_key``:  Flashduty integration key.
``flashduty_title``:  Alert title , no more than 512 characters, will be truncated if exceeded. Default to ``ElastAlert Alert``.
``flashduty_event_status``:  Alert status. Can be ``Info``, ``Warning``, ``Critical``, ``Ok``. Defaults to ``Info``.


Example usage::

    alert_text: "**{0}** - ALERT on host {1}"
    alert_text_args:
      - name
      - hostname
    alert:
      - flashduty
    flashduty_integration_key: "xxx"
    flashduty_title: "elastalert"
    flashduty_event_status: "Warning"
    flashduty_alert_key: "abc"
    flashduty_description: "log error"
    flashduty_check: "Too many occurrences of error logs"
    flashduty_resource: "index_name"
    flashduty_service: "service_name"
    flashduty_metric: "The number of error logs is greater than 5"
    flashduty_group: "sre"
    flashduty_cluster: "k8s"
    flashduty_app: "app"
    flashduty_env: "dev"

 Please refer to the parameter definition: https://docs.flashcat.cloud/en/flashduty/elastalert2-integration-guide
