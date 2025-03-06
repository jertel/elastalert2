import json
import warnings

import requests
from elastalert.alerts import Alerter, DateTimeEncoder
from elastalert.util import EAException, elastalert_logger
from requests import RequestException


class WebexWebhookAlerter(Alerter):
    """Creates a Webex Incoming Webook message for each alert"""

    required_options = frozenset(["webex_webhook_id"])

    def __init__(self, rule):
        super(WebexWebhookAlerter, self).__init__(rule)
        self.webex_webhook_id = self.rule.get(
            "webex_webhook_id", None
        )
        self.webex_webhook_url = f"https://webexapis.com/v1/webhooks/incoming/{self.webex_webhook_id}"
        self.webex_webhook_msgtype = self.rule.get("webex_webhook_msgtype", "text")

    def alert(self, matches):
        body = self.create_alert_body(matches)

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json;charset=utf-8",
        }

        payload = {"text": body}

        if self.webex_webhook_msgtype == "markdown":
            payload = {"markdown": body}

        try:
            response = requests.post(
                self.webex_webhook_url,
                data=json.dumps(payload, cls=DateTimeEncoder),
                headers=headers,
            )
            warnings.resetwarnings()
            response.raise_for_status()
        except RequestException as e:
            raise EAException("Error posting to webex_webhook: %s" % e)

        elastalert_logger.info("Trigger sent to webex_webhook")

    def get_info(self):
        return {
            "type": "webex_webhook",
            "webex_webhook_msgtype": self.webex_webhook_msgtype,
            "webex_webhook_url": self.webex_webhook_url,
        }
