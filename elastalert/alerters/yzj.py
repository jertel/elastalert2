import json
import warnings
from urllib.parse import urlunsplit, urlsplit

import requests
from requests import RequestException

from elastalert.alerts import Alerter, DateTimeEncoder
from elastalert.util import EAException, elastalert_logger


class YzjAlerter(Alerter):
    """ Creates a YZJ room message for each alert """
    required_options = frozenset(['yzj_token'])

    def __init__(self, rule):
        super(YzjAlerter, self).__init__(rule)
        self.yzj_token = self.rule.get('yzj_token', None)
        self.yzj_type = self.rule.get('yzj_type', 0)
        self.yzj_webhook_url = 'https://www.yunzhijia.com/gateway/robot/webhook/send?yzjtype=%s&yzjtoken=%s' % (self.yzj_type, self.yzj_token)
        self.yzj_proxy = self.rule.get('yzj_proxy', None)
        self.yzj_custom_loc = self.rule.get('yzj_custom_loc', None)

    def alert(self, matches):
        body = self.create_alert_body(matches)

        proxies = {'https': self.yzj_proxy} if self.yzj_proxy else None
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json;charset=utf-8'
        }

        if self.yzj_custom_loc is not None:
            part = urlsplit(self.yzj_webhook_url)
            custom_part = part._replace(netloc=self.yzj_custom_loc)
            self.yzj_webhook_url = urlunsplit(custom_part)

        payload = {
            'content': body
        }

        try:
            response = requests.post(self.yzj_webhook_url, data=json.dumps(payload, cls=DateTimeEncoder),
                                     headers=headers,
                                     proxies=proxies)
            warnings.resetwarnings()
            response.raise_for_status()
        except RequestException as e:
            raise EAException("Error posting to yzj: %s" % e)

        elastalert_logger.info("Trigger sent to YZJ")

    def get_info(self):
        return {
            "type": "yzj",
            "yzj_webhook_url": self.yzj_webhook_url
        }
