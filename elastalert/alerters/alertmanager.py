import json
import warnings

from datetime import datetime, timedelta, timezone
import requests
from jinja2 import Template, TemplateSyntaxError
from requests import RequestException
from requests.auth import HTTPBasicAuth

from elastalert.alerts import Alerter, DateTimeEncoder
from elastalert.util import EAException, elastalert_logger, lookup_es_key


class AlertmanagerAlerter(Alerter):
    """ Sends an alert to Alertmanager """

    required_options = frozenset({'alertmanager_hosts'})

    def __init__(self, rule):
        super(AlertmanagerAlerter, self).__init__(rule)
        self.api_version = self.rule.get('alertmanager_api_version', 'v1')
        self.hosts = self.rule.get('alertmanager_hosts')
        self.alertname = self.rule.get('alertmanager_alertname', self.rule.get('name'))
        self.labels = self.rule.get('alertmanager_labels', dict())
        self.annotations = self.rule.get('alertmanager_annotations', dict())
        self.fields = self.rule.get('alertmanager_fields', dict())
        self.title_labelname = self.rule.get('alertmanager_alert_subject_labelname', 'summary')
        self.body_labelname = self.rule.get('alertmanager_alert_text_labelname', 'description')
        self.proxies =self.rule.get('alertmanager_proxy', None)
        self.ca_certs = self.rule.get('alertmanager_ca_certs')
        self.ignore_ssl_errors = self.rule.get('alertmanager_ignore_ssl_errors', False)
        self.timeout = self.rule.get('alertmanager_timeout', 10)
        self.alertmanager_basic_auth_login = self.rule.get('alertmanager_basic_auth_login', None)
        self.alertmanager_basic_auth_password = self.rule.get('alertmanager_basic_auth_password', None)
        if 'alertmanager_resolve_time' in rule:
            self.resolve_timeout = timedelta(**rule['alertmanager_resolve_time'])
        else:
            self.resolve_timeout = None
        self.jinja_root_name = self.rule.get('jinja_root_name', None)

    @staticmethod
    def _json_or_string(obj):
        """helper to encode non-string objects to JSON"""
        if isinstance(obj, str):
            return obj
        return json.dumps(obj, cls=DateTimeEncoder)

    def _render_jinja_templates(self, templates, context):
        """Helper method to render Jinja2 templates."""
        rendered = {}
        for key, template_str in templates.items():
            try:
                jinja_template = Template(template_str)
                rendered[key] = jinja_template.render(context)
            except TemplateSyntaxError as e:
                raise ValueError(f"Alertmanager: The template provided by key '{key}' has an invalid Jinja2 syntax. "
                                f"Please check your template syntax: {e}")
        return rendered

    def alert(self, matches):
        headers = {'content-type': 'application/json'}
        proxies = {'https': self.proxies} if self.proxies else None
        auth = HTTPBasicAuth(self.alertmanager_basic_auth_login, self.alertmanager_basic_auth_password) if self.alertmanager_basic_auth_login else None

        resolved_labels = {}

        if self.jinja_root_name:
            context = matches[0] | {self.jinja_root_name: matches[0]}
        else:
            context = matches[0]

        resolved_labels = self._render_jinja_templates(self.labels, context)

        resolved_labels.update({
            label: self._json_or_string(lookup_es_key(matches[0], term))
            for label, term in self.fields.items()})
        resolved_labels.update(
            alertname=self.alertname,
            elastalert_rule=self.rule.get('name'))

        resolved_annotations = {}
        resolved_annotations = self._render_jinja_templates(self.annotations, context)

        resolved_annotations.update({
            self.title_labelname: self.create_title(matches),
            self.body_labelname: self.create_alert_body(matches)})

        payload = {
            'annotations': resolved_annotations,
            'labels': resolved_labels
        }

        if self.resolve_timeout is not None:
            end_time = self.now() + self.resolve_timeout
            payload['endsAt'] = end_time.isoformat()

        for host in self.hosts:
            try:
                url = '{}/api/{}/alerts'.format(host, self.api_version)

                if self.ca_certs:
                    verify = self.ca_certs
                else:
                    verify = not self.ignore_ssl_errors
                if self.ignore_ssl_errors:
                    requests.packages.urllib3.disable_warnings()

                response = requests.post(
                    url,
                    data=json.dumps([payload], cls=DateTimeEncoder),
                    headers=headers,
                    verify=verify,
                    proxies=proxies,
                    timeout=self.timeout,
                    auth=auth
                )

                warnings.resetwarnings()
                response.raise_for_status()
            except RequestException as e:
                raise EAException("Error posting to Alertmanager: %s" % e)
        elastalert_logger.info("Alert sent to Alertmanager")

    def get_info(self):
        return {'type': 'alertmanager'}

    def now(self):
        return datetime.now(timezone.utc)
