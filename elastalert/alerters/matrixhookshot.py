import copy
import json
import requests
import warnings

from elastalert.alerts import Alerter, DateTimeEncoder
from elastalert.util import elastalert_logger, EAException, lookup_es_key
from requests.exceptions import RequestException


class MatrixHookshotAlerter(Alerter):
    """ Creates a Matrix Hookshot room message for each alert """
    required_options = frozenset(['matrixhookshot_webhook_url'])

    def __init__(self, rule):
        super(MatrixHookshotAlerter, self).__init__(rule)
        self.matrixhookshot_webhook_url = self.rule.get('matrixhookshot_webhook_url', None)
        if isinstance(self.matrixhookshot_webhook_url, str):
            self.matrixhookshot_webhook_url = [self.matrixhookshot_webhook_url]
        self.matrixhookshot_proxy = self.rule.get('matrixhookshot_proxy', None)
        self.matrixhookshot_username = self.rule.get('matrixhookshot_username', '')
        self.matrixhookshot_text = self.rule.get('matrixhookshot_text', '')
        self.matrixhookshot_html = self.rule.get('matrixhookshot_html', '')
        self.matrixhookshot_ignore_ssl_errors = self.rule.get('matrixhookshot_ignore_ssl_errors', False)
        self.matrixhookshot_timeout = self.rule.get('matrixhookshot_timeout', 10)
        self.matrixhookshot_ca_certs = self.rule.get('matrixhookshot_ca_certs')

    def format_body(self, body):
        # https://matrix-org.github.io/matrix-hookshot/latest/setup/webhooks.html
        return body

    def get_aggregation_summary_text__maximum_width(self):
        width = super(MatrixHookshotAlerter, self).get_aggregation_summary_text__maximum_width()
        # Reduced maximum width for prettier MatrixHookshot display.
        return min(width, 75)

    def get_aggregation_summary_text(self, matches):
        text = super(MatrixHookshotAlerter, self).get_aggregation_summary_text(matches)
        if text:
            text = '```\n{0}```\n'.format(text)
        return text

    def alert(self, matches):
        body = self.create_alert_body(matches)

        body = self.format_body(body)
        # post to matrixhookshot
        headers = {'content-type': 'application/json'}
        # set https proxy, if it was provided
        proxies = {'https': self.matrixhookshot_proxy} if self.matrixhookshot_proxy else None
        payload = {
            'text': body
        }
        if self.matrixhookshot_username:
            payload['username'] = self.matrixhookshot_username
        if self.matrixhookshot_html:
            payload['html'] = self.matrixhookshot_html
        if self.matrixhookshot_text:
            payload['text'] = self.matrixhookshot_text

        for url in self.matrixhookshot_webhook_url:
            try:
                if self.matrixhookshot_ca_certs:
                    verify = self.matrixhookshot_ca_certs
                else:
                    verify = not self.matrixhookshot_ignore_ssl_errors
                if self.matrixhookshot_ignore_ssl_errors:
                    requests.packages.urllib3.disable_warnings()
                response = requests.post(
                    url, data=json.dumps(payload, cls=DateTimeEncoder),
                    headers=headers, verify=verify,
                    proxies=proxies,
                    timeout=self.matrixhookshot_timeout)
                warnings.resetwarnings()
                response.raise_for_status()
            except RequestException as e:
                raise EAException("Error posting to matrixhookshot: %s" % e)
        elastalert_logger.info("Alert '%s' sent to MatrixHookshot" % self.rule['name'])

    def get_info(self):
        return {'type': 'matrixhookshot' }
