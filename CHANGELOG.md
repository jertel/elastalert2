# 2.TBD.TBD

## Breaking changes
- None

## New features
- None

## Other changes
- None

# 2.26.0

## Breaking changes
- None

## New features
- Now supporting Elasticsearch 9 and OpenSearch 3 - [#1682](https://github.com/jertel/elastalert2/pull/1682) - @jertel

## Other changes
- Removed specific version requirement for Elastic Kibana and OpenSearch Discover - [#1682](https://github.com/jertel/elastalert2/pull/1682) - @jertel
- If `--end` argument falls in the past then at least one full run cycle will now complete before exiting - [#1694](https://github.com/jertel/elastalert2/pull/1694) - @nkormakov
- Add support for a `ES_VERSION` environment variable to override the Elasticsearch version - [#1690](https://github.com/jertel/elastalert2/pull/1690) - @fabian-heib

# 2.25.0

## Breaking changes
- [Helm] An unlikely breaking change could occur if this chart was previously deployed with namespace overrides. Deploy to a pre-prod environment before proceeding with production. - [#1662](https://github.com/jertel/elastalert2/pull/1662) - @lepouletsuisse

## New features
- [ServiceNow] Include arbitrary fields in ServiceNow tickets by including a `service_now_additional_fields` configuration stanza. - [#1670](https://github.com/jertel/elastalert2/pull/1670) - @mitchell-es
- [SMSEagle] New SMSEagle alerter - [#1671](https://github.com/jertel/elastalert2/pull/1671) - @marcin-smseagle

## Other changes
- [Helm] Fix `--namespace` and `namespaceOverride` value in Helm charts - [#1662](https://github.com/jertel/elastalert2/pull/1662) - @lepouletsuisse
- [Pager Duty] Expand `pagerduty_v2_payload_custom_details` to allow defaulting to value of provided key:value pair if the value is not found as a key in an elastalert match. - [#1674](https://github.com/jertel/elastalert2/pull/1674) - @mark-trellix

# 2.24.0

## Breaking changes
- None

## New features
- [MicrosoftPowerAutomate] Add support for 'ms_power_automate_webhook_url_from_field' option to dynamically select the webhook URL from the match. - [#1623](https://github.com/jertel/elastalert2/pull/1623) - @aizerin
- Add Webex Incoming Webhook alerter - [#1635](https://github.com/jertel/elastalert2/pull/1635) - @dennis-trapp
- Support jinja2 templates in `alertmanager_labels` and `alertmanager_annotations` - [#1642](https://github.com/jertel/elastalert2/pull/1642) - @tgxworld
- [Helm] Add support of update strategy in the deployment [#1646](https://github.com/jertel/elastalert2/pull/1646) - @efazenda
- Add Flashduty alerter - [#1649](https://github.com/jertel/elastalert2/pull/1649) - @pijiang3

## Other changes
- Fix `schema.yaml` to support Kibana 8.17 - [#1631](https://github.com/jertel/elastalert2/pull/1631) - @vpiserchia
- [Helm] Clarified documentation around rootRulesFolder - @jertel
- [IRIS] Fix `iris.py` to overcome a description overwriting bug - [#1643](https://github.com/jertel/elastalert2/pull/1643) - @jmolletAMNH
- Add `metric_<metric_key>_formatted` and `metric_agg_value_formatted` to metric aggregation when using compound query keys - [#1647](https://github.com/jertel/elastalert2/pull/1647) - @dennis-trapp
- Remove lineNotifyAlerter [#1638](https://github.com/jertel/elastalert2/pull/1638) - @nsano-rururu
- Fixed an issue where the test-docker command would cause an error when running old docker-compose [#1638](https://github.com/jertel/elastalert2/pull/1638) - @nsano-rururu

# 2.23.0

## Breaking changes
- None

## New features
- [Helm] Add optional liveness and readiness probe - [#1604](https://github.com/jertel/elastalert2/pull/1604) - @aizerin
- Add `include_rule_params_in_matches` rule parameter to enable copying of specific rule params into match data - [#1605](https://github.com/jertel/elastalert2/pull/1605) - @jertel
- [Helm] Add `--prometheus_addr` command line parameter to allow binding the Prometheus metrics server on a different host address - [#1608](https://github.com/jertel/elastalert2/pull/1608) - @tgxworld
- Support YZJ general robots - [#1641](https://github.com/jertel/elastalert2/pull/1641) - @innerpeacez

## Other changes
- [Docs] Add missing documentation of the `aggregation_alert_time_compared_with_timestamp_field` option. - [#1588](https://github.com/jertel/elastalert2/pull/1588) - @nicolasnovelli
- Fix linter error reporting about return type assignation in `elastalert/test_rule.py`. - [#1594](https://github.com/jertel/elastalert2/pull/1594) - @thican
- Add support for Kibana 8.17 for Kibana Discover - [#1597](https://github.com/jertel/elastalert2/pull/1597) - @nsano-rururu
- Resolve runtime deprecation warnings related to Elastic's 8.16 range filter changes - [#1599](https://github.com/jertel/elastalert2/pull/1599) - @jertel
- Resolve test deprecation warnings related to prettytable enum changes - [#1599](https://github.com/jertel/elastalert2/pull/1599) - @jertel
- Upgrade dependency pylint to 3.3.3 (build) - [#1599](https://github.com/jertel/elastalert2/pull/1599) - @jertel
- Upgrade dependency pytest to 8.3.4 (build) - [#1599](https://github.com/jertel/elastalert2/pull/1599) - @jertel
- Upgrade dependency pytest-cov to 6.0.0 (build) - [#1599](https://github.com/jertel/elastalert2/pull/1599) - @jertel
- Upgrade dependency sphinx to 8.1.3 (build)  - [#1599](https://github.com/jertel/elastalert2/pull/1599) - @jertel
- Upgrade dependency sphinx_rtd_theme to 3.0.2 (build) - [#1599](https://github.com/jertel/elastalert2/pull/1599) - @jertel
- Upgrade dependency tox to 4.23.2 (build) - [#1599](https://github.com/jertel/elastalert2/pull/1599) - @jertel
- Upgrade dependency apscheduler to 3.11.0 - [#1599](https://github.com/jertel/elastalert2/pull/1599) - @jertel
- Upgrade dependency boto3 to 1.35.92 - [#1599](https://github.com/jertel/elastalert2/pull/1599) - @jertel
- Upgrade dependency cffi to 1.17.1 - [#1599](https://github.com/jertel/elastalert2/pull/1599) - @jertel
- Upgrade dependency croniter to 6.0.0 - [#1599](https://github.com/jertel/elastalert2/pull/1599) - @jertel
- Upgrade dependency jinja2 to 3.1.5 - [#1599](https://github.com/jertel/elastalert2/pull/1599) - @jertel
- Upgrade dependency jira to 3.8.0 - [#1599](https://github.com/jertel/elastalert2/pull/1599) - @jertel
- Upgrade dependency jsonpointer to 3.0.0 - [#1599](https://github.com/jertel/elastalert2/pull/1599) - @jertel
- Upgrade dependency jsonschema to 4.23.0 - [#1599](https://github.com/jertel/elastalert2/pull/1599) - @jertel
- Upgrade dependency prettytable to 3.12.0 - [#1599](https://github.com/jertel/elastalert2/pull/1599) - @jertel
- Upgrade dependency prometheus-client to 0.21.1 - [#1599](https://github.com/jertel/elastalert2/pull/1599) - @jertel
- Upgrade dependency pyyaml to 6.0.2 - [#1599](https://github.com/jertel/elastalert2/pull/1599) - @jertel
- Upgrade dependency requests to 2.32.3 - [#1599](https://github.com/jertel/elastalert2/pull/1599) - @jertel
- Upgrade dependency stomp.py to 8.2.0 - [#1599](https://github.com/jertel/elastalert2/pull/1599) - @jertel
- Upgrade dependency tencentcloud-sdk-python to 3.0.1295 - [#1599](https://github.com/jertel/elastalert2/pull/1599) - @jertel
- Upgrade dependency twilio to 9.4.1 - [#1599](https://github.com/jertel/elastalert2/pull/1599) - @jertel
- [Spike] Fixes spike rule error when no data exists in the current time window - [#1605](https://github.com/jertel/elastalert2/pull/1605) - @jertel
- [Spike] Fixes spike rule error when no data exists in the reference time window - [#1610](https://github.com/jertel/elastalert2/pull/1610) - @jertel

# 2.22.0

## Breaking changes
- Note that version 2.21 upgraded Python to 3.13 and unintentionally dropped support for Python 3.12. This release, restores support for Python 3.12, while continuing to use Python 3.13 in the official ElastAlert 2 Docker image. Python 3.12 support will be dropped in a future release. - [#1585](https://github.com/jertel/elastalert2/pull/1585) - @jertel

## New features
- None

## Other changes
- None

# 2.21.0

## Breaking changes
- Be aware that this version dropped support for Python 3.12. It was re-added in the following release due to some distributions not yet supporting Python 3.13.

## New features
- [Notifications] System error notifications can now be delivered via the same set of alerters as rule alerts - [#1546](https://github.com/jertel/elastalert2/pull/1546) - @jertel
- [Notifications] New config option `notify_all_errors` supports all system errors, including loss of data connectivity - [#1546](https://github.com/jertel/elastalert2/pull/1546) - @jertel

## Other changes
- [Docs] Mention the two available Spike-rule metrics that are add into the match record - [#1542](https://github.com/jertel/elastalert2/pull/1542) - @ulmako
- [OpsGenie] Corrected spelling of the `opsgenie_default_receipients` configuration option to `opsgenie_default_recipients`. Both variations will continue to work and a warning message will notify affected users. [#1539](https://github.com/jertel/elastalert2/pull/1539) - @lstyles
- [OpsGenie] Prevent templated `opsgenie_teams` and `opsgenie_recipients` from being overwritten with evaluated values first time an alert is sent. [#1540](https://github.com/jertel/elastalert2/issues/1540) [#1539](https://github.com/jertel/elastalert2/pull/1539) - @lstyles
- [OpsGenie] Updated configuration schema with missing OpsGenie alerter properties. [#1543](https://github.com/jertel/elastalert2/pull/1543) - @lstyles
- [Docs] Add missing documentation of the timestamp_field option - [#1544](https://github.com/jertel/elastalert2/pull/1544) - @apollolv
- Add support for Kibana 8.14/8.15/8.16 for Kibana Discover - [#1547](https://github.com/jertel/elastalert2/pull/1547),[#1582](https://github.com/jertel/elastalert2/pull/1582) - @nsano-rururu, @jertel
- Upgrade pylint 3.1.0 to 3.3.1, pytest 8.0.2 to 8.3.3, pytest-cov 4.1.0 to 5.0.0, pytest-xdist 3.5.0 to 3.6.1, sphinx 7.2.6 to 8.0.2, sphinx_rtd_theme 2.0.0 to 3.0.1, tox 4.13.0 to 4.21.2  - [#1550](https://github.com/jertel/elastalert2/pull/1550) - @nsano-rururu
- Upgrade to Python 3.13 - [#1551](https://github.com/jertel/elastalert2/pull/1551) - @nsano-rururu
- [OpsGenie] Support dynamic `opsgenie_addr` values - [#1563](https://github.com/jertel/elastalert2/pull/1563) - @mohamedelema17

# 2.20.0

## Breaking changes
- Drop python3.9, python3.10, python3.11 from `python_requires` - [#1528](https://github.com/jertel/elastalert2/pull/1528) - @kmurphy4
- [IRIS] Updated alert_title to leverage ElastAlert built-in ``create_title`` function. Updated alert_description to use ElastAlert2 built-in function ``create_alert_body`` if alert_description is not set within the rule - [#1532](https://github.com/jertel/elastalert2/pull/1532) - @bvirgilioamnh

## New features
- [MS Power Automate] New Alert Channel with Microsoft Power Automate - [#1505](https://github.com/jertel/elastalert2/pull/1505)  [#1513](https://github.com/jertel/elastalert2/pull/1513) [#1519](https://github.com/jertel/elastalert2/pull/1519) - @marssilva, @jertel
- [Matrix Hookshot] New Alerter for sending alerts to Matrix via Hookshot - [#1525](https://github.com/jertel/elastalert2/pull/1525) - @jertel

## Other changes
- [Indexer] Fixed fields types error on instance indexer_alert_config in schema.yml - [#1499](https://github.com/jertel/elastalert2/pull/1499) - @olehpalanskyi
- [IRIS] Changed alert_source field from static 'ElastAlert2' value to field iris_alert_source value with default of 'ElastAlert2' - [#1531](https://github.com/jertel/elastalert2/pull/1531) - @bvirgilioamnh
- [IRIS] Fixed NoneType error raised in issue [#1457](https://github.com/jertel/elastalert2/issues/1457) - [#1533](https://github.com/jertel/elastalert2/pull/1533) - @bvirgilioamnh


# 2.19.0

## Breaking changes
- None

## New features
- Add indexer alerter - [#1451](https://github.com/jertel/elastalert2/pull/1451) - @olehpalanskyi

## Other changes
- [Docs] Fixed typo in Alerta docs with incorrect number of seconds in a day. - @jertel
- Update GitHub actions to avoid running publish workflows on forked branches. - @jertel
- Rewrite `_find_es_dict_by_key` per [discussion #1450](https://github.com/jertel/elastalert2/discussions/1450) for fieldnames literally ending in `.keyword` [#1459](https://github.com/jertel/elastalert2/pull/1459) - @jmacdone @jertel

# 2.18.0

## Breaking changes
- Renamed PR #1193's `fields` common rule option to `include_fields` due to collision with `new_term` rule type's existing `field` parameter - [#1408](https://github.com/jertel/elastalert2/pull/1408) - @jertel

## New features
- [Jira] Add ability to create a subtask, etc of an existing parent - [#1417](https://github.com/jertel/elastalert2/pull/1417) - @olehpalanskyi

## Other changes
- [workwechat] add workwechat msgtype - [#1369](https://github.com/jertel/elastalert2/pull/1369) - @bitqiu
- [Pager Duty] Add options: pagerduty_ca_certs, pagerduty_ignore_ssl_errors - [#1418](https://github.com/jertel/elastalert2/pull/1418) - @kexin-zhai
- Add support for Kibana 8.13 for Kibana Discover - [#1423](https://github.com/jertel/elastalert2/pull/1423) - @nsano-rururu
- Support DingTalk robot, add sign security settings - [#1485](https://github.com/jertel/elastalert2/pull/1485) - @innerpeacez

# 2.17.0

## Breaking changes
- None

## New features
- Add workwechat alerter - [#1367](https://github.com/jertel/elastalert2/pull/1367) - @wufeiqun

## Other changes
- [IRIS] Remove empty IOC in alerts that are not accepted by the API - [#1374](https://github.com/jertel/elastalert2/pull/1374) - @yaksnip425
- Upgrade boto3 to 1.34.54 - [#1388](https://github.com/jertel/elastalert2/pull/1388) - @jertel
- Upgrade croniter to 2.0.2 - [#1388](https://github.com/jertel/elastalert2/pull/1388) - @jertel
- Upgrade jinja2 to 3.1.3 - [#1388](https://github.com/jertel/elastalert2/pull/1388) - @jertel
- Upgrade jira to 3.6.0 - [#1388](https://github.com/jertel/elastalert2/pull/1388) - @jertel
- Upgrade jsonschema to 4.21.1 - [#1388](https://github.com/jertel/elastalert2/pull/1388) - @jertel
- Upgrade prettytable to 3.10.0 - [#1388](https://github.com/jertel/elastalert2/pull/1388) - @jertel
- Upgrade prometheus-client to 0.20.0 - [#1388](https://github.com/jertel/elastalert2/pull/1388) - @jertel
- Upgrade pylint to 3.1.0 - [#1388](https://github.com/jertel/elastalert2/pull/1388) - @jertel
- Upgrade pytest to 8.0.2 - [#1388](https://github.com/jertel/elastalert2/pull/1388) - @jertel
- Upgrade python-dateutil to 2.9.0.post0 - [#1388](https://github.com/jertel/elastalert2/pull/1388) - @jertel
- Upgrade tencentcloud-sdk-python to 3.0.1098 - [#1388](https://github.com/jertel/elastalert2/pull/1388) - @jertel
- Upgrade tox to 4.13.0 - [#1388](https://github.com/jertel/elastalert2/pull/1388) - @jertel
- Upgrade twilio to 8.13.0 - [#1388](https://github.com/jertel/elastalert2/pull/1395) - @jertel
- Removed explicit tzlocal lib dependency - [#1388](https://github.com/jertel/elastalert2/pull/1388) - @jertel

# 2.16.0

## Breaking changes
- None

## New features
- [Telegram] Added new telegram_thread_id setting for sending alerts to different threads of supergroup/forum. - [#1319](https://github.com/jertel/elastalert2/pull/1319) - @polshe-v
- Support hourly index patterns - [#1328](https://github.com/jertel/elastalert2/pull/1328) - @jmacdone

## Other changes
- Update setup.py & requirements.txt & requirements-dev.txt - [#1316](https://github.com/jertel/elastalert2/pull/1316) - @nsano-rururu
- [Docs] Clarify how to reference query_key values in flatline alerts - [#1320](https://github.com/jertel/elastalert2/pull/1320) - @jertel
- Fix percentiles aggregation type in Spike Metric Aggregation rules - [#1323](https://github.com/jertel/elastalert2/pull/1323) - @jertel
- [Docs] Extend FAQ / troubleshooting section with information on Elasticsearch RBAC - [#1324](https://github.com/jertel/elastalert2/pull/1324) - @chr-b
- Upgrade to Python 3.12 - [#1327](https://github.com/jertel/elastalert2/pull/1327) - @jertel
- Correction in IRIS and GELF alerter [#1331](https://github.com/jertel/elastalert2/pull/1331) - @malinkinsa
- Fix handing of compound_query_key values - [#1330](https://github.com/jertel/elastalert2/pull/1330) - @jmacdone
- Fix handing raw_query_key and query_key values ending with .keyword- [#1330](https://github.com/jertel/elastalert2/pull/1330) - @jmacdone
- [Docs] Fix broken search function caused by sphinx upgrade a few releases ago - [#1332](https://github.com/jertel/elastalert2/pull/1332) - @jertel
- [Docs] Fix mismatch for parameter iris_customer_id - [1334](https://github.com/jertel/elastalert2/pull/1334) @malinkinsa
- [IRIS] Make parameter iris_customer_id optional with default value - [1334](https://github.com/jertel/elastalert2/pull/1334) @malinkinsa
- (Re)Implement `skip_invalid` to continue loading rules if one is invalid - [#1338](https://github.com/jertel/elastalert2/pull/1338) - @jertel
- [Docs] Refactor the docs structure for improved ease-of-use - [#1337](https://github.com/jertel/elastalert2/pull/1337) - @jertel
- [Email] Refactor SMTP cert/key usage to support Python 3.12 - [#1341](https://github.com/jertel/elastalert2/pull/1341) - @jertel
- [IRIS] Fix schema.yaml(iris_url to iris_host) - [#1346](https://github.com/jertel/elastalert2/pull/1346) - @nsano-rururu
- [IRIS] Fix issue with document with nested json inside. See [#1348](https://github.com/jertel/elastalert2/discussions/1348) - [#1352](https://github.com/jertel/elastalert2/pull/1352) - @malinkinsa
- [Docs] Clarify `jinja_template_path` documentation - [20a05f9](https://github.com/jertel/elastalert2/commit/20a05f995f566f8719d6e4bf7b8a3977c7ab9e23) - @jertel
- Add support for Kibana 8.12 for Kibana Discover - [#1364](https://github.com/jertel/elastalert2/pull/1364) - @nsano-rururu
- Upgrade pylint 3.0.2 to 3.0.3, pytest 7.4.3 to 8.0.0, sphinx_rtd_theme 1.3.0 to 2.0.0, tox 4.11.3 to 4.12.1 - [#1365](https://github.com/jertel/elastalert2/pull/1365) - @nsano-rururu

# 2.15.0

## Breaking changes
- None

## New features
- [Iris] Alerter added - [#1301](https://github.com/jertel/elastalert2/pull/1301) - @malinkinsa 
- [Opensearch] Add the possibility to generate an opensearch discovery url - [#1310](https://github.com/jertel/elastalert2/pull/1310) - @luffynextgen

## Other changes
- Refactored FlatlineRule to make it more extensible - [#1291](https://github.com/jertel/elastalert2/pull/1291) - @rundef 
- Add support for Kibana 8.11 for Kibana Discover - [#1305](https://github.com/jertel/elastalert2/pull/1305) - @nsano-rururu
- Update docs - [#1311](https://github.com/jertel/elastalert2/pull/1311) - @nsano-rururu

# 2.14.0

## Breaking changes
- None

## New features
- 'summary_table_type' property now supports 'html' format for aggregation tables - [#1260](https://github.com/jertel/elastalert2/pull/1260) - @jertel 
- [Helm] Add support for custom deployment annotations - [#1271](https://github.com/jertel/elastalert2/pull/1271) - @victorpugin 

## Other changes
- [Helm] Expose minReadySeconds parameter to assist in detecting failed deployments - [#1243](https://github.com/jertel/elastalert2/pull/1243) - @alexku7 
- [Helm] Fix commonLabels indentation for the deployment template - [#1250](https://github.com/jertel/elastalert2/pull/1250) - @dan-duffy 
- Add support for Kibana 8.10 for Kibana Discover - [#1277](https://github.com/jertel/elastalert2/pull/1277) - @nsano-rururu
- Upgrade pylint 2.17.4 to 2.17.5, pytest 7.3.1 to 7.4.2, sphinx 6.2.1 to 7.2.6, sphinx_rtd_theme 1.2.2 to 1.3.0 - [#1278](https://github.com/jertel/elastalert2/pull/1278) - @nsano-rururu
- Fix issue with aggregated alerts not being sent - [#1285](https://github.com/jertel/elastalert2/pull/1285) - @jertel
- Add support for [Lark](https://www.larksuite.com/en_us/) alerter - [#1282](https://github.com/jertel/elastalert2/pull/1282) - @seanyinx

# 2.13.2

## Breaking changes
- None

## New features
- None

## Other changes
- [Helm] Fix chart indentation issue introduced in 2.13.1 - [#1239](https://github.com/jertel/elastalert2/pull/1239) - @jertel

# 2.13.1

## Breaking changes
- None

## New features
- None

## Other changes
- [Helm] Add support for generating rule config from a directory of rules, during chart deployment - [#1236](https://github.com/jertel/elastalert2/pull/1236) - @mehrdad-khojastefar 
- [AlertManager] Fix typo with new feature released in 2.13.0 - [#1237](https://github.com/jertel/elastalert2/pull/1237) - @eveningcafe

# 2.13.0

## Breaking changes
- None

## New features
- [Alertmanager] Add alertmanager resolve timeout configuration option - [#1187](https://github.com/jertel/elastalert2/pull/1187) - @eveningcafe

## Other changes
- [Docs] Clarify docs to state that alert_time_limit should not be 0 - [#1208](https://github.com/jertel/elastalert2/pull/1208) - @jertel
- Add support for Kibana 8.9 for Kibana Discover - [#1224](https://github.com/jertel/elastalert2/pull/1224) - @nsano-rururu
- Remove docker image pin to outdated "buster" debian release - [24f794a](https://github.com/jertel/elastalert2/commit/24f794a) - @jertel

# 2.12.0

## Breaking changes
- None

## New features
- Add initial support for EQL - [#1189](https://github.com/jertel/elastalert2/pull/1189) - @jertel
- Add `fields` parameter to rules to be able to pull in runtimes fields, and more. [#1193](https://github.com/jertel/elastalert2/pull/1193) - @Goggin
- Add EQL support to elastalert-test-rule utility - [#1195](https://github.com/jertel/elastalert2/pull/1195) - @jertel

## Other changes
- Add support for Kibana 8.8 for Kibana Discover - [#1184](https://github.com/jertel/elastalert2/pull/1184) - @nsano-rururu
- Upgrade pylint 2.17.0 to 2.17.4, pytest 7.2.2 to 7.3.1, pytest-xdist 3.2.0 to 3.3.1, sphinx 6.1.3 to 6.2.1, sphinx_rtd_theme == 1.2.2 - [#1194](https://github.com/jertel/elastalert2/pull/1194) - @nsano-rururu
- Upgrade to Tox 4 - [#1196](https://github.com/jertel/elastalert2/pull/1196) - @jertel
- Log message when exiting due to --end param being in the past - [#1199](https://github.com/jertel/elastalert2/pull/1199) - @jertel

# 2.11.0

## Breaking changes
- None

## New features
- None

## Other changes
- [Kubernetes] Fix mistake introduced in #1141 related to initContainers - [#1145](https://github.com/jertel/elastalert2/pull/1145) - @aturpin1789
- Add support for Kibana 8.7 for Kibana Discover - [#1153](https://github.com/jertel/elastalert2/pull/1153) - @nsano-rururu
- [Docs] Add documentation for accessing subfields of array items - [#1166](https://github.com/jertel/elastalert2/pull/1166) - @jertel

# 2.10.1

## Breaking changes
- None

## New features
- None

## Other changes
- Corrected alert bug when both top_count_keys and query_key are specified in a rule - [#1128](https://github.com/jertel/elastalert2/pull/1128) - @jertel
- Fixed docker-compose detection logic from recent PR - [#1128](https://github.com/jertel/elastalert2/pull/1128) - @jertel
- Upgrade pylint 2.15.5 to 2.17.0, pytest 7.2.0 to 7.2.2, pytest-xdist 3.1.0 to 3.2.0, sphinx 5.3.0 to 6.1.3, tox 3.27.1 to 3.28.0 - [#1131](https://github.com/jertel/elastalert2/pull/1131) - @nsano-rururu
- Update Docs & FAQ(disable_rules_on_error, es_conn_timeout) - [#1133](https://github.com/jertel/elastalert2/pull/1133) - @nsano-rururu
- [Kubernetes] Add extraInitContainers value to helm chart - [#1141](https://github.com/jertel/elastalert2/pull/1141) - @aturpin1789

# 2.10.0

## Breaking changes
- [Alerta] All matches will now be sent with the alert - [#1068](https://github.com/jertel/elastalert2/pull/1068) - @dakotacody
- Renamed the `overwrites` parameter to `overrides` in the load_conf method of config.py - [#1100](https://github.com/jertel/elastalert2/pull/1100) - @akusei

## New features
- [Graylog GELF] Alerter added. [#1050](https://github.com/jertel/elastalert2/pull/1050) - @malinkinsa
- [TheHive] Format `title`, `type`, and `source` with dynamic lookup values - [#1092](https://github.com/jertel/elastalert2/pull/1092) - @fandigunawan
- [HTTP POST2] `http_post2_payload` and `http_post2_headers` now support multiline JSON strings for better control over jinja templates - [#1104](https://github.com/jertel/elastalert2/pull/1104) - @akusei
- [HTTP POST2] This alerter now supports the use of `jinja_root_name` - [#1104](https://github.com/jertel/elastalert2/pull/1104) - @akusei
- [Rule Testing] The data file passed with `--data` can now contain a single JSON document or a list of JSON objects - [#1104](https://github.com/jertel/elastalert2/pull/1104) - @akusei

## Other changes
- [Docs] Clarify Jira Cloud authentication configuration - [94f7e8c](https://github.com/jertel/elastalert2/commit/94f7e8cc98d59a00349e3b23acd8a8549c80dbc8) - @jertel
- Update minimum versions for third-party dependencies in requirements.txt and setup.py - [#1051](https://github.com/jertel/elastalert2/pull/1051) - @nsano-rururu
- [Docs] Clarify `import` support for list of files - [#1075](https://github.com/jertel/elastalert2/pull/1075) - @sqrooted
- Add support for Kibana 8.6 for Kibana Discover - [#1080](https://github.com/jertel/elastalert2/pull/1080) - @nsano-rururu
- Modify schema to allow string and boolean for `*_ca_certs` to allow for one to specify a cert bundle for SSL certificate verification - [#1082](https://github.com/jertel/elastalert2/pull/1082) - @goggin
- Fix UnicodeEncodeError in PagerDutyAlerter - [#1091](https://github.com/jertel/elastalert2/pull/1091) - @nsano-rururu
- The scan_entire_timeframe setting, when used with use_count_query or use_terms_query will now scan entire timeframe on subsequent rule runs - [#1097](https://github.com/jertel/elastalert2/pull/1097) - @rschirin
- Add new unit tests to cover changes in the HTTP POST2 alerter - [#1104](https://github.com/jertel/elastalert2/pull/1104) - @akusei
- [Docs] Updated HTTP POST2 documentation to outline changes with payloads, headers and multiline JSON strings - [#1104](https://github.com/jertel/elastalert2/pull/1104) - @akusei
- [HTTP POST2] Additional error checking around rendering and dumping payloads/headers to JSON - [#1104](https://github.com/jertel/elastalert2/pull/1104) - @akusei

# 2.9.0

## Breaking changes
- None

## New features
- Add `realert_key` option to silence groups of alerts - [#1004](https://github.com/jertel/elastalert2/pull/1004) - @goggin

## Other changes
- Upgrade pylint 2.15.3 to 2.15.5, pytest 7.1.3 to 7.2.0, pytest-xdist 2.5.0 to 3.0.2, sphinx 5.2.3 to 5.3.0, tox 3.26.0 to 3.27.0 - [#988](https://github.com/jertel/elastalert2/pull/988) - @nsano-rururu
- Upgrade to Python 3.11 - [#989](https://github.com/jertel/elastalert2/pull/989) - @jertel
- Add support for Kibana 8.5 for Kibana Discover - [#993](https://github.com/jertel/elastalert2/pull/993) - @nsano-rururu
- [Amazon SNS] Fix Amazon SNS Alerter - [#1003](https://github.com/jertel/elastalert2/pull/1003) - @nsano-rururu
- [Mattermost] Add mattermost_emoji_override - [#1011](https://github.com/jertel/elastalert2/pull/1011) - @nsano-rururu
- Add support for disabling verification of SSL certificate for the Kibana Shorten URL API - [#1013](https://github.com/jertel/elastalert2/pull/1013) - @BenJeau

# 2.8.0

## Breaking changes
- None

## New features
- Adding the optional timestamp_to_datetime_format_expr rule parameter, allowing custom modification of the Elasticsearch timestamp string before parsing it into datetime. - [#978](https://github.com/jertel/elastalert2/pull/978) - @thpiron

## Other changes
- Upgrade pylint 2.15.2 to 2.15.3 and pytest-cov 3.0.0 to 4.0.0 and sphinx 5.1.1 to 5.2.3; Add Google Chat proxy support - [#972](https://github.com/jertel/elastalert2/pull/972) - @nsano-rururu
- Fix Jira assign issue - [#974](https://github.com/jertel/elastalert2/pull/974) - @jorge-gyant
- [Kubernetes] Add extraContainers value to helm chart - [#975](https://github.com/jertel/elastalert2/pull/975) - @Kasape
- [docs] Updated index configuration documentation - [#979](https://github.com/jertel/elastalert2/pull/979) - @nsano-rururu
- [Kubernetes] Change 'metrics' to 'metrics.enabled' in helm chart documentation - [#981](https://github.com/jertel/elastalert2/pull/981) - @Kasape

# 2.7.0

## Breaking changes
- None

## New features
- [Telegram] Added new telegram_parse_mode setting to switch between markdown and html body formats. - [#924](https://github.com/jertel/elastalert2/pull/924) - @polshe-v

## Other changes
- Pin package version of `exotel` to `0.1.5` - [#931](https://github.com/jertel/elastalert2/pull/931)
- Add support for Kibana 8.4 for Kibana Discover - [#935](https://github.com/jertel/elastalert2/pull/935) - @nsano-rururu
- Upgrade pylint 2.14.5 to 2.15.2 and tox 3.25.1 to 3.26.0 and sphinx 5.0.2 to 5.1.1 - [#937](https://github.com/jertel/elastalert2/pull/937) - @nsano-rururu
- Upgrade pytest 7.1.2 to 7.1.3 - [#941](https://github.com/jertel/elastalert2/pull/941) - @nsano-rururu

# 2.6.0

## Breaking changes
- When using HTTP POST 2, it is no longer necessary to pre-escape strings (should they contain control chars) from events in elastic search which are replaced by the jinja2 template.

- [Kubernetes] [Breaking] Reconfigure metrics to follow prometheus operator nomenclature. `metrics` value, now control the addition of metrics endpoint (command argument), the creation of a service to expose the metrics endpoint and the (optional) creation of prometheus-operator objects: serviceMonitor and prometheurRules to match implementations of other charts. The labels of the chart have been modified, so you'll need to uninstall and reinstall the chart for the upgrade to work. - [#902](https://github.com/jertel/elastalert2/pull/902) - @PedroMSantosD

## New features
- [Kubernetes] Chart is now able to create a service for the metrics, and optional  prometheus-operator custom resources serviceMonitor and  prometheusRule. - [#902](https://github.com/jertel/elastalert2/pull/902) - @PedroMSantosD

## Other changes
- Upgrade pylint 2.13.8 to 2.14.3, Upgrade sphinx 4.5.0 to 5.0.2 - [#891](https://github.com/jertel/elastalert2/pull/891) - @nsano-rururu
- Add support for Kibana 8.3 for Kibana Discover - [#897](https://github.com/jertel/elastalert2/pull/897) - @nsano-rururu
- Fix internal json decode error in HTTP POST 2 if values from ES event contain control chars (e.g. newline) and are used in the jinja2 template - [#898](https://github.com/jertel/elastalert2/pull/898) - @ddurham2
- Upgrade pylint 2.14.3 to 2.14.5 and tox 3.25.0 to 3.25.1 - [#911](https://github.com/jertel/elastalert2/pull/911) - @nsano-rururu

# 2.5.1

## Breaking changes
- None

## New features
- None

## Other changes
- Upgrade stomp 8.0.0 to 8.0.1 - [#832](https://github.com/jertel/elastalert2/pull/832) - @jertel
- Add support for Kibana 8.2 for Kibana Discover, Upgrade Pytest 7.1.1 to 7.1.2, Upgrade pylint 2.13.5 to 2.13.8, Upgrade Jinja2 3.1.1 to 3.1.2 - [#840](https://github.com/jertel/elastalert2/pull/840) - @nsano-rururu
- Add the possibility to use rule and match fields in the description of TheHive alerts - [#855](https://github.com/jertel/elastalert2/pull/855) - @luffynextgen
- Fix missing colon on schema.yml and add unit test on it - [#866](https://github.com/jertel/elastalert2/pull/866) - @Isekai-Seikatsu
- Add the possibility to use tags, message and tlp level in TheHive observables [#873](https://github.com/jertel/elastalert2/pull/873) - @luffynextgen
- Support OpenSearch 2.x - [#880](https://github.com/jertel/elastalert2/pull/880) - @jertel

# 2.5.0

## Breaking changes
- Remove Simple Alerter - [#793](https://github.com/jertel/elastalert2/pull/793) - @nsano-rururu

## New features
- Add support for Kibana 8.1 for Kibana Discover - [#763](https://github.com/jertel/elastalert2/pull/763) - @nsano-rururu
- [MS Teams] Add arbitrary text value support for Facts - [#790](https://github.com/jertel/elastalert2/pull/790) - @iamxeph
- [MS Teams] Use alert_subject as ms_teams_alert_summary if ms_teams_alert_summary is not set - [#802](https://github.com/jertel/elastalert2/pull/802) - @iamxeph
- [Mattermost] List support for mattermost_channel_override - [#809](https://github.com/jertel/elastalert2/pull/809) - @nsano-rururu
- [Zabbix] Add the ability to specify `zbx_host` from available elasticsearch field - [#820](https://github.com/jertel/elastalert2/pull/820) - @timeforplanb123

## Other changes
- [Docs] Update FAQ ssl_show_warn - [#764](https://github.com/jertel/elastalert2/pull/764) - @nsano-rururu
- [Docs] Update FAQ telegram and Amazon SNS - [#765](https://github.com/jertel/elastalert2/pull/765) - @nsano-rururu
- Upgrade Pytest 7.0.1 to 7.1.1 - [#776](https://github.com/jertel/elastalert2/pull/776) - @nsano-rururu
- [Kubernetes] Add support for automatic SMTP mail server credential management - [#780](https://github.com/jertel/elastalert2/pull/780) - @lusson-luo
- Upgrade sphinx 4.4.0 to 4.5.0 - [#782](https://github.com/jertel/elastalert2/pull/782) - @nsano-rururu
- Upgrade pylint 2.12.2 to 2.13.2 - [#783](https://github.com/jertel/elastalert2/pull/783) - @nsano-rururu
- Upgrade jinja2 3.0.3 to 3.1.1 - [#784](https://github.com/jertel/elastalert2/pull/784) - @nsano-rururu
- Update schema.yaml(Alertmanager, Spike, Flatline, New Term, Metric Aggregation, Percentage Match) - [#789](https://github.com/jertel/elastalert2/pull/789) - @nsano-rururu
- Upgrade pylint 2.13.2 to 2.13.3 - [#792](https://github.com/jertel/elastalert2/pull/792) - @nsano-rururu
- Upgrade pylint 2.13.3 to 2.13.4 - [#801](https://github.com/jertel/elastalert2/pull/801) - @nsano-rururu
- Fix SpikeRule - [#804](https://github.com/jertel/elastalert2/pull/804) - @nsano-rururu
- [Kubernetes] Add scanSubdirectories (defaults to true) as an option in Helm Chart - [#805](https://github.com/jertel/elastalert2/pull/805) - @louzadod
- Upgrade pylint 2.13.4 to 2.13.5 - [#808](https://github.com/jertel/elastalert2/pull/808) - @nsano-rururu
- Update documentation on Cloud ID support - [#810](https://github.com/jertel/elastalert2/pull/810) - @ferozsalam
- Upgrade tox 3.24.5 to 3.25.0 - [#813](https://github.com/jertel/elastalert2/pull/813) - @nsano-rururu
- [Kubernetes] Add support to specify rules directory - [#816](https://github.com/jertel/elastalert2/pull/816) @SBe
- Fix HTTP POST 2 alerter for nested payload keys - [#823](https://github.com/jertel/elastalert2/pull/823) - @lepouletsuisse
- [Kubernetes] Expose prometheus metrics to kubernetes pod service discovery mechanism - [#827](https://github.com/jertel/elastalert2/pull/827) - @PedroMSantosD

# 2.4.0

## Breaking changes
- Add support for Elasticsearch 8, remove support for Elasticsearch 6 and below - [#744](https://github.com/jertel/elastalert2/pull/744) - @ferozsalam, @jertel, and @nsano-rururu
  WARNING! Read the [ES 8 upgrade notes](https://elastalert2.readthedocs.io/en/latest/recipes/faq.html#does-elastalert-2-support-elasticsearch-8) BEFORE upgrading your cluster to Elasticsearch 8. Failure to do so can result in your cluster no longer starting and unable to rollback to 7.x.
- Kibana dashboard integration has been removed, as it only was supported with older versions of Elasticsearch and Kibana. Per the above breaking change those older versions are no longer supported by ElastAlert 2.
- Dockerfile refactor for app home and user home to be the same directory (/opt/elastalert/). Before app home is /opt/elastalert/ and user home is /opt/elastalert/elastalert. After app home and user home are the same /opt/elastalert/ - [#656](https://github.com/jertel/elastalert2/pull/656)

## New features
- [MS Teams] Kibana Discover URL and Facts - [#660](https://github.com/jertel/elastalert2/pull/660) - @thib12
- Add support for Kibana 7.17 for Kibana Discover - [#695](https://github.com/jertel/elastalert2/pull/695) - @nsano-rururu
- Added a fixed name metric_agg_value to MetricAggregationRule match_body - [#697](https://github.com/jertel/elastalert2/pull/697) - @iamxeph

## Other changes
- Load Jinja template when loading an alert - [#654](https://github.com/jertel/elastalert2/pull/654) - @thib12
- Upgrade tox 3.24.4 to 3.24.5 - [#655](https://github.com/jertel/elastalert2/pull/655) - @nsano-rururu
- Upgrade sphinx 4.3.2 to 4.4.0 - [#661](https://github.com/jertel/elastalert2/pull/661) - @nsano-rururu
- [Docs] Fix Running Docker container - [#674](https://github.com/jertel/elastalert2/pull/674) - @nsano-rururu 
- [Exotel] Added exotel_message_body to schema.yaml - [#685](https://github.com/jertel/elastalert2/pull/685) - @nsano-rururu
- Upgrade Pytest 6.2.5 to 7.0.0 - [#696](https://github.com/jertel/elastalert2/pull/696) - @nsano-rururu
- python-dateutil version specification change - [#704](https://github.com/jertel/elastalert2/pull/704) - @nsano-rururu
- Update minimum versions for third-party dependencies in requirements.txt and setup.py - [#705](https://github.com/jertel/elastalert2/pull/705) - @nsano-rururu
- [Docs] Document updates for Alerts and email addresses etc - [#706](https://github.com/jertel/elastalert2/pull/706) - @nsano-rururu
- [Docs] Update of RuleType Configuration Cheat Sheet - [#707](https://github.com/jertel/elastalert2/pull/707) - @nsano-rururu
- Upgrade Pytest 7.0.0 to 7.0.1 - [#710](https://github.com/jertel/elastalert2/pull/710) - @nsano-rururu
- Fixing jira_transition_to schema bug. Change property type from boolean to string - [#721](https://github.com/jertel/elastalert2/pull/721) - @toxisch
- Begin Elasticsearch 8 support - ElastAlert 2 now supports setup with fresh ES 8 instances, and works with some alert types - [#731](https://github.com/jertel/elastalert2/pull/731) - @ferozsalam
- Enable dynamic setting of rules volume in helm chart - [#732](https://github.com/jertel/elastalert2/pull/732) - @ChrisFraun
- Do not install tests via pip install - [#733](https://github.com/jertel/elastalert2/pull/733) - @buzzdeee
- [Docs] Add Elasticsearch 8 support documentation - [#735](https://github.com/jertel/elastalert2/pull/735) - @ferozsalam
- Remove download_dashboard - [#740](https://github.com/jertel/elastalert2/pull/740) - @nsano-rururu
- [Docs] Added documentation for metric|spike aggregation rule types for percentiles - [e682ea8](https://github.com/jertel/elastalert2/commit/e682ea8113bf9f413b6339e6803b5262881f2b30)- @jertel
- [Jira] Add support for Jira authentication via Personal Access Token - [#750](https://github.com/jertel/elastalert2/pull/750) - @buzzdeee
- [Docs] Update docs Negation, and, or - [#754](https://github.com/jertel/elastalert2/pull/754) - @nsano-rururu
- Remove call to `print` from elastalert.py - [#755](https://github.com/jertel/elastalert2/pull/755) - @ferozsalam
- [Docs] Added dingtalk_proxy, dingtalk_proxy_login, dingtalk_proxy_pass to docs - [#756](https://github.com/jertel/elastalert2/pull/756) - @nsano-rururu

# 2.3.0

## Breaking changes
- [Kubernetes] The helm chart repository has changed. The new repository is located at https://jertel.github.io/elastalert2/. This was necessary due to the previous chart museum hosting service, Bonzai Cloud, terminating it's chart hosting service on January 21, 2022. - @jertel

## New features
- Add metric_agg_script to MetricAggregationRule [#558](https://github.com/jertel/elastalert2/pull/558) - @dequis
- [Alertmanager] Add support for basic authentication - [#575](https://github.com/jertel/elastalert2/pull/575) - @nsano-rururu
- Add support for Kibana 7.16 for Kibana Discover - [#612](https://github.com/jertel/elastalert2/pull/612) - @nsano-rururu
- [MS Teams] Add support for disabling verification of SSL certificate - [#628](https://github.com/jertel/elastalert2/pull/628) - @nsano-rururu

## Other changes
- sphinx 4.2.0 to 4.3.0 and tzlocal==2.1 - [#561](https://github.com/jertel/elastalert2/pull/561) - @nsano-rururu
- jinja2 3.0.1 to 3.0.3 - [#562](https://github.com/jertel/elastalert2/pull/562) - @nsano-rururu
- Fix `get_rule_file_hash` TypeError - [#566](https://github.com/jertel/elastalert2/pull/566) - @JeffAshton
- Ensure `schema.yaml` stream closed - [#567](https://github.com/jertel/elastalert2/pull/567) - @JeffAshton
- Fixing `import` bugs & memory leak in `RulesLoader`/`FileRulesLoader` - [#580](https://github.com/jertel/elastalert2/pull/580) - @JeffAshton
- sphinx 4.3.0 to 4.3.1 - [#588](https://github.com/jertel/elastalert2/pull/588) - @nsano-rururu
- pytest-xdist 2.4.0 to 2.5.0 - [#615](https://github.com/jertel/elastalert2/pull/615) - @nsano-rururu
- sphinx 4.3.1 to 4.3.2 - [#618](https://github.com/jertel/elastalert2/pull/618) - @nsano-rururu
- Remove unused parameter boto-profile - [#622](https://github.com/jertel/elastalert2/pull/622) - @nsano-rururu
- [Docs] Include Docker example; add additional FAQs - [#623](https://github.com/jertel/elastalert2/pull/623) - @nsano-rururu
- Add support for URL shortening with Kibana 7.16+ - [#633](https://github.com/jertel/elastalert2/pull/633) - @jertel
- [example] URL correction of information about Elasticsearch - [#642](https://github.com/jertel/elastalert2/pull/642) - @nsano-rururu
- pylint 2.11.1 to 2.12.2 - [#651](https://github.com/jertel/elastalert2/pull/651) - @nsano-rururu

# 2.2.3

## Breaking changes
- None

## New features
- [Alertmanager] Added support for Alertmanager - [#503](https://github.com/jertel/elastalert2/pull/503) - @nsano-rururu
- Add summary_table_max_rows optional configuration to limit rows in summary tables - [#508](https://github.com/jertel/elastalert2/pull/508) - @mdavyt92
- Added support for shortening Kibana Discover URLs using Kibana Shorten URL API - [#512](https://github.com/jertel/elastalert2/pull/512) - @JeffAshton
- Added new alerter `HTTP Post 2` which allow more flexibility to build the body/headers of the request. - [#530](https://github.com/jertel/elastalert2/pull/530) - @lepouletsuisse
- [Slack] Added new option to include url to jira ticket if it is created in the same pipeline. - [#547](https://github.com/jertel/elastalert2/pull/547) - @hugefarsen
- Added support for multi ElasticSearch instances. - [#548](https://github.com/jertel/elastalert2/pull/548) - @buratinopy

## Other changes
- [Docs] Add exposed metrics documentation - [#498](https://github.com/jertel/elastalert2/pull/498) - @thisisxgp
- [Tests] Fix rules_test.py - [#499](https://github.com/jertel/elastalert2/pull/499) - @nsano-rururu
- Upgrade to Python 3.10 and Sphinx 4.2.0 - [#501](https://github.com/jertel/elastalert2/pull/501) - @jertel
- max_scrolling_count now has a default value of 990 to avoid stack overflow crashes - [#509](https://github.com/jertel/elastalert2/pull/509) - @jertel
- Update pytest 6.2.5, pytest-cov 3.0.0, pytest-xdist 2.4.0, pylint<2.12, tox 3.24.4 - [#511](https://github.com/jertel/elastalert2/pull/511) - @nsano-rururu
- Added a check on the value of the path "rules_folder" to make sure it exists - [#519](https://github.com/jertel/elastalert2/pull/519) - @AntoineBlaud
- [OpsGenie] Fix tags on subsequent alerts - [#537](https://github.com/jertel/elastalert2/pull/537) - @jertel

# 2.2.2

## Breaking changes
- None

## New features
- Added support for markdown style formatting of aggregation tables - [#415](https://github.com/jertel/elastalert2/pull/415) - @Neuro-HSOC
- [OpsGenie] Add support for custom description - [#457](https://github.com/jertel/elastalert2/pull/457), [#460](https://github.com/jertel/elastalert2/pull/460) - @nickbabkin
- [Tencent SMS] Added support for Tencent SMS - [#470](https://github.com/jertel/elastalert2/pull/470) - @liuxingjun
- Add support for Kibana 7.15 for Kibana Discover - [#481](https://github.com/jertel/elastalert2/pull/481) - @nsano-rururu
- Begin working toward support of OpenSearch (beta) [#483](https://github.com/jertel/elastalert2/pull/483) @nbrownus

## Other changes
- [Rule Test] Fix issue related to --start/--end/--days params - [#424](https://github.com/jertel/elastalert2/pull/424), [#433](https://github.com/jertel/elastalert2/pull/433) - @thican
- [TheHive] Reduce risk of sourceRef collision for Hive Alerts by using full UUID -[#513](https://github.com/jertel/elastalert2/pull/513) - @fwalloe
- Changed the wording of ElastAlert to ElastAlert 2 and Update FAQ -[#446](https://github.com/jertel/elastalert2/pull/446) - @nsano-rururu
- Add missing show_ssl_warn and silence_qk_value params to docs - [#469](https://github.com/jertel/elastalert2/pull/469) - @jertel
- [OpsGenie] Clarify documentation for URL endpoint to use in European region - [#475](https://github.com/jertel/elastalert2/pull/475) - @nsano-rururu
- [Docs] The documentation has been updated as the name of Amazon Elasticsearch Service has changed to Amazon OpenSearch Service. - [#478](https://github.com/jertel/elastalert2/pull/478) - @nsano-rururu
- [Tests] Improve test coverage of tencentsms.py - [#479](https://github.com/jertel/elastalert2/pull/479) - @liuxingjun
- [Docs] Tidy Exotel documentation - [#488](https://github.com/jertel/elastalert2/pull/488) - @ferozsalam

# 2.2.1

## Breaking changes
- None

## New features
- None

## Other changes
- Fixed typo in default setting accidentally introduced in [#407](https://github.com/jertel/elastalert2/pull/407) - [#413](https://github.com/jertel/elastalert2/pull/413) - @perceptron01

# 2.2.0

## Breaking changes
- [VictorOps] Changed `state_message` and `entity_display_name` values to be taken from an alert rule. - [#329](https://github.com/jertel/elastalert2/pull/329) - @ChristophShyper
  - Potentially a breaking change if the alert subject changes due to the new default behavior.
- Change metric/percentage rule types to store query_key as dict, instead of string, for consistency with other rule types. [#340](https://github.com/jertel/elastalert2/issues/340) - @AntoineBlaud

## New features
- [Kubernetes] Adding Image Pull Secret to Helm Chart - [#370](https://github.com/jertel/elastalert2/pull/370) - @robrankin
- Apply percentage_format_string to match_body percentage value; will appear in new percentage_formatted key - [#387](https://github.com/jertel/elastalert2/pull/387) - @iamxeph
- Add support for Kibana 7.14 for Kibana Discover - [#392](https://github.com/jertel/elastalert2/pull/392) - @nsano-rururu
- Add metric_format_string optional configuration for Metric Aggregation to format aggregated value - [#399](https://github.com/jertel/elastalert2/pull/399) - @iamxeph
- Make percentage_format_string support format() syntax in addition to old %-formatted syntax - [#403](https://github.com/jertel/elastalert2/pull/403) - @iamxeph
- Add custom_pretty_ts_format option to provides a way to define custom format of timestamps printed by pretty_ts() function - [#407](https://github.com/jertel/elastalert2/pull/407) - @perceptron01

## Other changes
- [Tests] Improve test code coverage - [#331](https://github.com/jertel/elastalert2/pull/331) - @nsano-rururu
- [Docs] Upgrade Sphinx from 4.0.2 to 4.1.2- [#332](https://github.com/jertel/elastalert2/pull/332) [#343](https://github.com/jertel/elastalert2/pull/343) [#344](https://github.com/jertel/elastalert2/pull/344) [#369](https://github.com/jertel/elastalert2/pull/369) - @nsano-rururu
- Ensure hit count returns correct value for newer ES clusters - [#333](https://github.com/jertel/elastalert2/pull/333) - @jeffashton
- [Tests] Upgrade Tox from 3.23.1 to 3.24.1 - [#345](https://github.com/jertel/elastalert2/pull/345) [#388](https://github.com/jertel/elastalert2/pull/388)  - @nsano-rururu
- Upgrade Jinja from 2.11.3 to 3.0.1 - [#350](https://github.com/jertel/elastalert2/pull/350) - @mrfroggg
- [Tests] Add test code. Changed ubuntu version of Dockerfile-test from latest to 21.10. - [#354](https://github.com/jertel/elastalert2/pull/354) - @nsano-rururu
- Remove Python 2.x compatibility code - [#354](https://github.com/jertel/elastalert2/pull/354) - @nsano-rururu
- [Docs] Added Chatwork proxy settings to documentation - [#360](https://github.com/jertel/elastalert2/pull/360) - @nsano-rururu
- Add settings to schema.yaml(Chatwork proxy, Dingtalk proxy) - [#361](https://github.com/jertel/elastalert2/pull/361) - @nsano-rururu
- [Docs] Tidy Twilio alerter documentation - [#363](https://github.com/jertel/elastalert2/pull/363) - @ferozsalam
- [Tests] Improved test coverage for opsgenie.py 96% to 100% - [#364](https://github.com/jertel/elastalert2/pull/364) - @nsano-rururu
- [Docs] Update mentions of JIRA to Jira - [#365](https://github.com/jertel/elastalert2/pull/365) - @ferozsalam
- [Docs] Tidy Datadog alerter documentation - [#380](https://github.com/jertel/elastalert2/pull/380) - @ferozsalam

# 2.1.2
## Breaking changes
- None

## New features
- [Rocket.Chat] Add support for generating Kibana Discover URLs to Rocket.Chat alerter - [#260](https://github.com/jertel/elastalert2/pull/260) - @nsano-rururu
- [Jinja] Provide rule key/values as possible Jinja data inputs - [#281](https://github.com/jertel/elastalert2/pull/281) - @mrfroggg
- [Kubernetes] Add securityContext and podSecurityContext to Helm chart - [#289](https://github.com/jertel/elastalert2/pull/289) - @lepouletsuisse
- [Rocket.Chat] Add options: rocket_chat_ca_certs, rocket_chat_ignore_ssl_errors, rocket_chat_timeout - [#302](https://github.com/jertel/elastalert2/pull/302) - @nsano-rururu
- [Jinja] Favor match keys over colliding rule keys when resolving Jinja vars; also add alert_text_jinja unit test - [#311](https://github.com/jertel/elastalert2/pull/311) - @mrfroggg
- [Opsgenie] Added possibility to specify source and entity attrs - [#315](https://github.com/jertel/elastalert2/pull/315) - @konstantin-kornienko
- [ServiceNow] Add support for `servicenow_impact` and `servicenow_urgency` parameters for ServiceNow alerter - [#316](https://github.com/jertel/elastalert2/pull/316) - @randolph-esnet
- [Jinja] Add Jinja support to alert_subject - [#318](https://github.com/jertel/elastalert2/pull/318) - @mrfroggg
@lepouletsuisse
- Metrics will now include time_taken, representing the execution duration of the rule - [#324](https://github.com/jertel/elastalert2/pull/324) - @JeffAshton

## Other changes
- [Prometheus] Continue fix for prometheus wrapper writeback function signature - [#256](https://github.com/jertel/elastalert2/pull/256) - @greut
- [Stomp] Improve exception handling in alerter - [#261](https://github.com/jertel/elastalert2/pull/261) - @nsano-rururu
- [AWS] Improve exception handling in Amazon SES and SNS alerters - [#264](https://github.com/jertel/elastalert2/pull/264) - @nsano-rururu
- [Docs] Clarify documentation for starting ElastAlert 2 - [#265](https://github.com/jertel/elastalert2/pull/265) - @ferozsalam
- Add exception handling for unsupported operand type - [#266](https://github.com/jertel/elastalert2/pull/266) - @nsano-rururu
- [Docs] Improve documentation for Python build requirements - [#267](https://github.com/jertel/elastalert2/pull/267) - @nsano-rururu
- [DataDog] Correct alerter logging - [#268](https://github.com/jertel/elastalert2/pull/268) - @nsano-rururu
- [Docs] Correct parameter code documentation for main ElastAlert runner - [#269](https://github.com/jertel/elastalert2/pull/269) - @ferozsalam
- [Command] alerter will now fail during init instead of during alert if given invalid command setting - [#270](https://github.com/jertel/elastalert2/pull/270) - @nsano-rururu
- [Docs] Consolidate all examples into a new examples/ sub folder - [#271](https://github.com/jertel/elastalert2/pull/271) - @ferozsalam
- [TheHive] Add example rule with Kibana Discover URL and query values in alert text - [#276](https://github.com/jertel/elastalert2/pull/276) - @markus-nclose
- Upgrade pytest-xdist from 2.2.1 to 2.3.0; clarify HTTPS support in docs; Add additional logging - [#283](https://github.com/jertel/elastalert2/pull/283) - @nsano-rururu
- [Tests] Add more alerter test coverage - [#284](https://github.com/jertel/elastalert2/pull/284) - @nsano-rururu
- [Tests] Improve structure and placement of test-related files in project tree - [#287](https://github.com/jertel/elastalert2/pull/287) - @ferozsalam
- Only attempt to adjust timezone if timezone is set to a non-empty string - [#288](https://github.com/jertel/elastalert2/pull/288) - @ferozsalam
- [Kubernetes] Deprecated `podSecurityPolicy` feature in Helm Chart as [it's deprecated in Kubernetes 1.21](https://kubernetes.io/blog/2021/04/06/podsecuritypolicy-deprecation-past-present-and-future/) - [#289](https://github.com/jertel/elastalert2/pull/289) - @lepouletsuisse
- [Slack] Fix slack_channel_override schema - [#291](https://github.com/jertel/elastalert2/pull/291) - @JeffAshton
- [Rocket.Chat] Fix rocket_chat_channel_override schema - [#293](https://github.com/jertel/elastalert2/pull/293) - @nsano-rururu
- [Tests] Increase code coverage - [#294](https://github.com/jertel/elastalert2/pull/294) - @nsano-rururu
- [Docs] Added Kibana Discover sample - [#295](https://github.com/jertel/elastalert2/pull/295) - @nsano-rururu
- [AWS] Remove deprecated boto_profile setting - [#299](https://github.com/jertel/elastalert2/pull/299) - @nsano-rururu
- [Slack] Correct slack_alert_fields schema definition - [#300](https://github.com/jertel/elastalert2/pull/300) - @nsano-rururu
- [Tests] Correct code coverage to eliminate warnings - [#301](https://github.com/jertel/elastalert2/pull/301) - @nsano-rururu
- Eliminate unnecessary calls to Elasticsearch - [#303](https://github.com/jertel/elastalert2/pull/303) - @JeffAshton
- [Zabbix] Fix timezone parsing - [#304](https://github.com/jertel/elastalert2/pull/304) - @JeffAshton
- Improve logging of scheduler - [#305](https://github.com/jertel/elastalert2/pull/305) - @JeffAshton
- [Jinja] Update Jinja from 2.11.3 to 3.0.1; Improve handling of colliding variables - [#311](https://github.com/jertel/elastalert2/pull/311) - @mrfroggg
- [TheHive] Force observable artifacts to be strings - [#313](https://github.com/jertel/elastalert2/pull/313) - @pandvan
- Upgrade pylint from <2.9 to <2.10 - [#314](https://github.com/jertel/elastalert2/pull/314) - @nsano-rururu
- [ChatWork] Enforce character limit - [#319](https://github.com/jertel/elastalert2/pull/319) - @nsano-rururu
- [LineNotify] Enforce character limit - [#320](https://github.com/jertel/elastalert2/pull/320) - @nsano-rururu
- [Discord] Remove trailing backticks from alert body - [#321](https://github.com/jertel/elastalert2/pull/321) - @nsano-rururu
- Redirecting warnings to logging module - [#325](https://github.com/jertel/elastalert2/pull/325) - @JeffAshton

# 2.1.1

## Breaking changes
- None

## New features
- Add support for RocketChat - [#182](https://github.com/jertel/elastalert2/pull/182) - @nsano-rururu
- Expose rule scheduler properties as configurable settings - [#192](https://github.com/jertel/elastalert2/pull/192) - @jertel
- Exclude empty observables from TheHive requests - [#193](https://github.com/jertel/elastalert2/pull/193) - @LaZyDK
- Ensure TheHive tags are converted to strings before submitting TheHive request - [#206](https://github.com/jertel/elastalert2/pull/206) - @LaZyDK
- Add support for Elasticsearch API key authentication - [#208](https://github.com/jertel/elastalert2/pull/208) - @vbisserie
- Add support for Elasticsearch 7.13 for building Kibana Discover URLs - [#212](https://github.com/jertel/elastalert2/pull/212) - @nsano-rururu
- Follow symbolic links when traversing rules folder for rule files - [#214](https://github.com/jertel/elastalert2/pull/214) - @vbisserie
- Support optional suppression of SSL log warnings when http-posting alerts - [#222](https://github.com/jertel/elastalert2/pull/222) - @nsano-rururu
- Add support for inclusion of Kibana Discover URLs in MatterMost messages - [#239](https://github.com/jertel/elastalert2/pull/239) - @nsano-rururu
- Add support for inclusion of alert Title in MatterMost messages - [#246](https://github.com/jertel/elastalert2/pull/246) - @nsano-rururu

## Other changes
- Speed up unit tests by adding default parallelism - [#164](https://github.com/jertel/elastalert2/pull/164) - @ferozsalam
- Remove unused writeback_alias and fix --patience argument - [#167](https://github.com/jertel/elastalert2/pull/167) - @mrfroggg
- Fix Bearer token auth in initialisation script - [#169](https://github.com/jertel/elastalert2/pull/169) - @ferozsalam
- Finish refactoring alerters and tests into individual files - [#175, et al](https://github.com/jertel/elastalert2/pull/175) - @ferozsalam
- Improve HTTP POST alert documentation - [#178](https://github.com/jertel/elastalert2/pull/178) - @nsano-rururu
- Upgrade Sphinx from 3.5.4 to 4.0.2 - [#179](https://github.com/jertel/elastalert2/pull/179) - @nsano-rururu
- Fix Sphinx dependency version - [#181](https://github.com/jertel/elastalert2/pull/181) - @ferozsalam
- Switch to absolute imports - [#198](https://github.com/jertel/elastalert2/pull/198) - @ferozsalam
- Encode JSON output before writing test data - [#215](https://github.com/jertel/elastalert2/pull/215) - @vbisserie
- Update pytest from 6.0.0 to 6.2.4 - [#223](https://github.com/jertel/elastalert2/pull/223/files) - @nsano-rururu
- Ensure ChatWork alerter fails to initialize if missing required args - [#224](https://github.com/jertel/elastalert2/pull/224) - @nsano-rururu
- Ensure DataDog alerter fails to initialize if missing required args - [#225](https://github.com/jertel/elastalert2/pull/225) - @nsano-rururu
- Ensure DingTalk alerter fails to initialize if missing required args - [#226](https://github.com/jertel/elastalert2/pull/226) - @nsano-rururu
- Ensure Zabbix alerter fails to initialize if missing required args - [#227](https://github.com/jertel/elastalert2/pull/227) - @nsano-rururu
- MS Teams alerter no longer requires ms_teams_alert_summary arg - [#228](https://github.com/jertel/elastalert2/pull/228) - @nsano-rururu
- Improve Gitter alerter by explicitly specifying arg names  - [#230](https://github.com/jertel/elastalert2/pull/230) - @nsano-rururu
- Add more alerter test code coverage - [#231](https://github.com/jertel/elastalert2/pull/231) - @nsano-rururu
- Upgrade pytest-cov from 2.12.0 to 2.12.1 - [#232](https://github.com/jertel/elastalert2/pull/232) - @nsano-rururu
- Migrate away from external test mock dependency - [#233](https://github.com/jertel/elastalert2/pull/233) - @nsano-rururu
- Improve ElastAlert 2 documentation relating to running scenarios - [#234](https://github.com/jertel/elastalert2/pull/234) - @ferozsalam
- Improve test coverage and correct dict lookup syntax for alerter init functions - [#235](https://github.com/jertel/elastalert2/pull/235) - @nsano-rururu
- Fix schema bug with MatterMost alerts - [#239](https://github.com/jertel/elastalert2/pull/239) - @nsano-rururu
- Fix prometheus wrapper writeback function signature - [#253](https://github.com/jertel/elastalert2/pull/253) - @greut

# 2.1.0

## Breaking changes
- TheHive alerter refactoring - [#142](https://github.com/jertel/elastalert2/pull/142) - @ferozsalam  
  - See the updated documentation for changes required to alert formatting
- Dockerfile refactor for performance and size improvements - [#102](https://github.com/jertel/elastalert2/pull/102) - @jgregmac
	- Dockerfile base image changed from `python/alpine` to `python/slim-buster` to take advantage of pre-build python wheels, accelerate build times, and reduce image size. If you have customized an image, based on jertel/elastalert2, you may need to make adjustments.
	- Default base path changed to `/opt/elastalert` in the Dockerfile and in Helm charts. Update your volume binds accordingly.
	- Dockerfile now runs as a non-root user "elastalert". Ensure your volumes are accessible by this non-root user.
	- System packages removed from the Dockerfile: All dev packages, cargo, libmagic. Image size reduced to 250Mb.
	- `tmp` files and dev packages removed from the final container image.

## New features
- Support for multiple rules directories and fix `..data` Kubernetes/Openshift recursive directories in FileRulesLoader [#157](https://github.com/jertel/elastalert2/pull/157) - @mrfroggg
- Support environment variable substition in yaml files - [#149](https://github.com/jertel/elastalert2/pull/149) - @archfz
- Update schema.yaml and enhance documentation for Email alerter - [#144](https://github.com/jertel/elastalert2/pull/144) - @nsano-rururu
- Default Email alerter to use port 25, and require http_post_url for HTTP Post alerter - [#143](https://github.com/jertel/elastalert2/pull/143) - @nsano-rururu
- Support extra message features for Slack and Mattermost - [#140](https://github.com/jertel/elastalert2/pull/140) - @nsano-rururu
- Support a footer in alert text - [#133](https://github.com/jertel/elastalert2/pull/133) - @nsano-rururu
- Added support for alerting via Amazon Simple Email System (SES) - [#105](https://github.com/jertel/elastalert2/pull/105) - @nsano-rururu

## Other changes
- Begin alerter refactoring to split large source code files into smaller files - [#161](https://github.com/jertel/elastalert2/pull/161) - @ferozsalam
- Update contribution guidelines with additional instructions for local testing - [#147](https://github.com/jertel/elastalert2/pull/147), [#148](https://github.com/jertel/elastalert2/pull/148) - @ferozsalam
- Add more unit test coverage - [#108](https://github.com/jertel/elastalert2/pull/108) - @nsano-rururu
- Update documentation: describe limit_execution, correct alerters list - [#107](https://github.com/jertel/elastalert2/pull/107) - @fberrez
- Fix issue with testing alerts that contain Jinja templates - [#101](https://github.com/jertel/elastalert2/pull/101) - @jertel
- Updated all references of Elastalert to use the mixed case ElastAlert, as that is the most prevalent formatting found in the documentation.

# 2.0.4

## Breaking changes
- None

## New features
- Update python-dateutil requirement from <2.7.0,>=2.6.0 to >=2.6.0,<2.9.0 - [#96](https://github.com/jertel/elastalert2/pull/96) - @nsano-rururu
- Update pylint requirement from <2.8 to <2.9 - [#95](https://github.com/jertel/elastalert2/pull/95) - @nsano-rururu
- Pin ES library to 7.0.0 due to upcoming newer library conflicts - [#90](https://github.com/jertel/elastalert2/pull/90) - @robrankin
- Re-introduce CHANGELOG.md to project - [#88](https://github.com/jertel/elastalert2/pull/88) - @ferozsalam
- Add option for suppressing TLS warnings - [#87](https://github.com/jertel/elastalert2/pull/87) - @alvarolmedo
- Add support for Twilio Copilot - [#86](https://github.com/jertel/elastalert2/pull/86) - @cdmastercom
- Support bearer token authentication with ES - [#85](https://github.com/jertel/elastalert2/pull/85) - @StribPav
- Add support for statsd metrics - [#83](https://github.com/jertel/elastalert2/pull/83) - @eladamitpxi
- Add support for multiple imports of rules via recursive import - [#83](https://github.com/jertel/elastalert2/pull/83) - @eladamitpxi
- Specify search size of 0 to improve efficiency of searches - [#82](https://github.com/jertel/elastalert2/pull/82) - @clyfish
- Add alert handler to create Datadog events - [#81](https://github.com/jertel/elastalert2/pull/81) - @3vanlock

## Other changes

- Added missing Helm chart config.yaml template file.
- Update .gitignore with more precise rule for /config.yaml file.
- Now publishing container images to both DockerHub and to GitHub Packages for redundancy.
- Container images are now built and published via GitHub actions instead of relying on DockerHub's automated builds.
- Update PIP library description and Helm chart description to be consistent.
- Continue updates to change references from _ElastAlert_ to _ElastAlert 2_
