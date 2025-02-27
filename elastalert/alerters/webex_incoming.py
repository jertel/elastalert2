import json
import warnings

import requests
from elastalert.alerts import Alerter, DateTimeEncoder
from elastalert.util import EAException, elastalert_logger
from requests import RequestException


class WebexIncomingAlerter(Alerter):
    """Creates a Webex Incoming Webook message for each alert"""

    required_options = frozenset(["webex_incoming_webhook_id"])

    def __init__(self, rule):
        super(WebexIncomingAlerter, self).__init__(rule)
        self.webex_incoming_webhook_id = self.rule.get(
            "webex_incoming_webhook_id", None
        )
        self.webex_incoming_webhook_url = f"https://webexapis.com/v1/webhooks/incoming/{self.webex_incoming_webhook_id}"
        self.webex_incoming_msgtype = self.rule.get("webex_incoming_msgtype", "text")

    def alert(self, matches):
        title = self.create_title(matches)
        body = self.create_alert_body(matches)

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json;charset=utf-8",
        }

        if self.webex_incoming_msgtype == "markdown":
            payload = {"markdown": body}
        elif self.webex_incoming_msgtype == "text":
            payload = {"text": body}

        try:
            response = requests.post(
                self.webex_incoming_webhook_url,
                data=json.dumps(payload, cls=DateTimeEncoder),
                headers=headers,
            )
            warnings.resetwarnings()
            response.raise_for_status()
        except RequestException as e:
            raise EAException("Error posting to webex: %s" % e)

        elastalert_logger.info("Trigger sent to webex")

    def get_info(self):
        return {
            "type": "webex_incoming",
            "webex_incoming_webhook_url": self.webex_incoming_webhook_url,
        }
