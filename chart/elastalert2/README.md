
# ElastAlert 2 Helm Chart for Kubernetes

An ElastAlert 2 helm chart is available, and can be installed into an existing Kubernetes cluster by following the instructions below.

Inspiration for optional serviceMonitor and prometheusRules objects, along with source code for calculating and implementing labels on the chart, ported from  https://github.com/bitnami/charts/tree/master/bitnami/thanos/templates

## Installing the Chart

Add the elastalert2 repository to your Helm configuration:

```console
helm repo add elastalert2 https://jertel.github.io/elastalert2/
```

Next, install the chart with a release name, such as _elastalert2_:

```console
helm install elastalert2 elastalert2/elastalert2
```

The command deploys ElastAlert 2 on the Kubernetes cluster in the default configuration. The [configuration](#configuration) section lists the parameters that can be configured during installation.

See the comment in the default `values.yaml` for specifying a `writebackIndex` for ES 5.x.

If necessary, open Dev Tools on Kibana and send the below request to avoid errors like `RequestError: TransportError(400, u'search_phase_execution_exception', u'No mapping found for [alert_time] in order to sort on')`

```
PUT /elastalert/_mapping/elastalert
{
  "properties": {
      "alert_time": {"type": "date"}
  }
}
```

## Uninstalling the Chart

To uninstall/delete the ElastAlert 2 deployment:

```console
helm delete elastalert2 --purge
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Configuration

| Parameter                                    | Description                                                                                                                   | Default                                                  |
|----------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------|
| `image.repository`                           | docker image                                                                                                                  | jertel/elastalert2                                       |
| `image.tag`                                  | docker image tag                                                                                                              | 2.5.1                                                    |
| `image.pullPolicy`                           | image pull policy                                                                                                             | IfNotPresent                                             |
| `image.pullSecret`                           | image pull secret                                                                                                             | ""                                                       |
| `podAnnotations`                             | Annotations to be added to pods                                                                                               | {}                                                       |
| `podSecurityContext`                         | Configurable podSecurityContext for pod execution environment                                                                 | {"runAsUser": 1000, "runAsGroup": 1000, "fsGroup": 1000} |
| `securityContext`                            | Allows you to set the securityContext for the container                                                                       | {"runAsNonRoot": true, "runAsUser": 1000}                |
| `command`                                    | command override for container                                                                                                | `NULL`                                                   |
| `args`                                       | args override for container                                                                                                   | `NULL`                                                   |
| `replicaCount`                               | number of replicas to run                                                                                                     | 1                                                        |
| `rulesFolder`                                | Locaton of rules directory. Usefull when you have one docker image and different set on rules per environemnt. For example development can reside in `/opt/elastalert/develop` and production in `/opt/elastalert/production`.                                                                                                     | /opt/elastalert/rules                                                       |
| `elasticsearch.host`                         | elasticsearch endpoint to use                                                                                                 | elasticsearch                                            |
| `elasticsearch.port`                         | elasticsearch port to use                                                                                                     | 9200                                                     |
| `elasticsearch.useSsl`                       | whether or not to connect to es_host using SSL                                                                                | False                                                    |
| `elasticsearch.username`                     | Username for ES with basic auth                                                                                               | `NULL`                                                   |
| `elasticsearch.password`                     | Password for ES with basic auth                                                                                               | `NULL`                                                   |
| `elasticsearch.credentialsSecret`            | Specifies an existing secret to be used for the ES username/password auth                                                     | `NULL`                                                   |
| `elasticsearch.credentialsSecretUsernameKey` | The key in elasticsearch.credentialsSecret that stores the ES password auth                                                   | `NULL`                                                   |
| `elasticsearch.credentialsSecretPasswordKey` | The key in elasticsearch.credentialsSecret that stores the ES username auth                                                   | `NULL`                                                   |
| `elasticsearch.verifyCerts`                  | whether or not to verify TLS certificates                                                                                     | True                                                     |
| `elasticsearch.clientCert`                   | path to a PEM certificate to use as the client certificate                                                                    | `NULL`                                                   |
| `elasticsearch.clientKey`                    | path to a private key file to use as the client key                                                                           | `NULL`                                                   |
| `elasticsearch.caCerts`                      | path to a CA cert bundle to use to verify SSL connections                                                                     | `NULL`                                                   |
| `elasticsearch.certsVolumes`                 | certs volumes, required to mount ssl certificates when elasticsearch has tls enabled                                          | `NULL`                                                   |
| `elasticsearch.certsVolumeMounts`            | mount certs volumes, required to mount ssl certificates when elasticsearch has tls enabled                                    | `NULL`                                                   |
| `extraConfigOptions`                         | Additional options to propagate to all rules, cannot be `alert`, `type`, `name` or `index`                                    | `{}`                                                     |
| `secretConfigName`                           | name of the secret which holds the ElastAlert config. **Note:** this will completely overwrite the generated config           | `NULL`                                                   |
| `secretRulesName`                            | name of the secret which holds the ElastAlert rules. **Note:** this will overwrite the generated rules                        | `NULL`                                                   |
| `secretRulesList`                            | a list of rules to enable from the secret                                                                                     | []                                                       |
| `optEnv`                                     | Additional pod environment variable definitions                                                                               | []                                                       |
| `extraVolumes`                               | Additional volume definitions                                                                                                 | []                                                       |
| `extraVolumeMounts`                          | Additional volumeMount definitions                                                                                            | []                                                       |
| `serviceAccount.create`                      | Specifies whether a service account should be created.                                                                        | `true`                                                   |
| `serviceAccount.name`                        | Service account to be used. If not set and `serviceAccount.create` is `true`, a name is generated using the fullname template |                                                          |
| `serviceAccount.annotations`                 | ServiceAccount annotations                                                                                                    |                                                          |
| `podSecurityPolicy.create`                   | [DEPRECATED] Create pod security policy resources                                                                             | `false`                                                  |
| `resources`                                  | Container resource requests and limits                                                                                        | {}                                                       |
| `rulesVolumeName`                            | Specifies the rules volume to be mounted. Can be changed for mounting a custom rules folder via the extraVolumes parameter, instead of using the default rules configMap or secret rule mounting method.                                                                                 | "rules"                                                  |
| `rules`                                      | Rule and alert configuration for ElastAlert 2                                                                                 | {} example shown in values.yaml                          |
| `runIntervalMins`                            | Default interval between alert checks, in minutes                                                                             | 1                                                        |
| `realertIntervalMins`                        | Time between alarms for same rule, in minutes                                                                                 | `NULL`                                                   |
| `scanSubdirectories`                        | Enable/disable subdirectory scanning for rules                                                                                 | `true`                                                   |
| `alertRetryLimitMins`                        | Time to retry failed alert deliveries, in minutes                                                                             | 2880 (2 days)                                            |
| `bufferTimeMins`                             | Default rule buffer time, in minutes                                                                                          | 15                                                       |
| `writebackIndex`                             | Name or prefix of elastalert index(es)                                                                                        | elastalert                                               |
| `nodeSelector`                               | Node selector for deployment                                                                                                  | {}                                                       |
| `affinity`                                   | Affinity specifications for the deployed pod(s)                                                                               | {}                                                       |
| `tolerations`                                | Tolerations for deployment                                                                                                    | []                                                       |
| `smtp_auth.username`                         | Optional SMTP mail server username. If the value is not empty, the smtp_auth secret will be created automatically.       | `NULL`                                                   |
| `smtp_auth.password`                         | Optional SMTP mail server passwpord. This must be specified if the above field, `smtp_auth.username` is also specified.      | `NULL`                                                   |
| `metrics`                         | Enable elastalert prometheus endpoint, add prometheus.io annotations to pod and create a service pointing to the port for prometheus to scrape the metrics      | `false`                                                   |
| `metrics.prometheusPort`                         | If "metrics" is set to true, prometheus metrics will be exposed by the pod on this port.       | `8080`                                                   |
| `metrics.prometheusPortName`                         | Name of the port where metrics are exposed    | `http-alt`                                                   |
| `metrics.prometheusScrapeAnnotations`                         | If metrics are enabled, annotations to add to the pod for prometheus configuration. prometheus.io/port is also added during the prometheusPort and prometheusPortName values |  `{prometheus.io/scrape: "true" prometheus.io/path: "/"}`                                   |
| `metrics.serviceMonitor.enabled`                         | If metrics are enabled, create a serviceMonitor custom resource for prometheus-operator to detect and configure the metrics endpoint on prometheus.  |  `false` |
| `metrics.serviceMonitor.labels`                         | Labels to add to the prometheusRule object for prometheus-operator to detect it, when deployed on a namespace different from the one where prometheus-operator is running. |  `{}` |
| `metrics.serviceMonitor.metricRelabelings`                         | List of prometheus metric relabeling configs to apply to scrape. Example: drop python_gc metrics or alter pod name |  `[]` |
| `metrics.prometheusRule.enabled`                         | If metrics are enabled, create a prometheusRule custom resource for prometheus-operator |  `false` |
| `metrics.prometheusRule.additionalLabels`                         | Labels to add to the prometheusRule object for prometheus-operator to detect it, when deployed on a namespace different from the one where prometheus-operator is running. |  `{}` |
| `metrics.prometheusRule.rules`                         | Group of alerting and/or recording rules to add to the prometheus configuration, example Alerting rules for pod down, or for file descriptors. Should be added as multiline Yaml string |  `` |
