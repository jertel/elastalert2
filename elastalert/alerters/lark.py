import json
import warnings

import requests
from elastalert.alerts import Alerter, DateTimeEncoder
from elastalert.util import EAException, elastalert_logger
from requests import RequestException


class LarkAlerter(Alerter):
    """ Creates a Lark message for each alert """
    required_options = frozenset(['lark_bot_id'])

    def __init__(self, rule):
        super(LarkAlerter, self).__init__(rule)
        self.lark_bot_id = self.rule.get('lark_bot_id', None)
        self.lark_webhook_url = f'https://open.feishu.cn/open-apis/bot/v2/hook/{self.lark_bot_id}'
        self.lark_msg_type = self.rule.get('lark_msgtype', 'text')

    def alert(self, matches):
        title = self.create_title(matches)
        body = self.create_alert_body(matches)

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json;charset=utf-8'
        }

        payload = {
            'msg_type': self.lark_msg_type,
            "content": {
                "title": title,
                "text": body
            },
        }

        try:
            response = requests.post(
                self.lark_webhook_url,
                data=json.dumps(payload, cls=DateTimeEncoder),
                headers=headers)
            warnings.resetwarnings()
            response.raise_for_status()
        except RequestException as e:
            raise EAException("Error posting to lark: %s" % e)

        elastalert_logger.info("Trigger sent to lark")

    def get_info(self):
        return {
            "type": "lark",
            "lark_webhook_url": self.lark_webhook_url
        }
