import json
import warnings

import requests
from elastalert.alerts import Alerter, DateTimeEncoder
from elastalert.util import EAException, elastalert_logger
from requests import RequestException


class WorkWechatAlerter(Alerter):
    """ Creates a WorkWechat message for each alert """
    required_options = frozenset(['work_wechat_bot_id'])

    def __init__(self, rule):
        super(WorkWechatAlerter, self).__init__(rule)
        self.work_wechat_bot_id = self.rule.get('work_wechat_bot_id', None)
        self.work_wechat_webhook_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={self.work_wechat_bot_id}'
        self.work_wechat_msg_type = 'text'

    def alert(self, matches):
        title = self.create_title(matches)
        body = self.create_alert_body(matches)

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json;charset=utf-8'
        }

        payload = {
            'msgtype': self.work_wechat_msg_type,
            "text": {
                "content": body
            },
        }

        try:
            response = requests.post(
                self.work_wechat_webhook_url,
                data=json.dumps(payload, cls=DateTimeEncoder),
                headers=headers)
            warnings.resetwarnings()
            response.raise_for_status()
        except RequestException as e:
            raise EAException("Error posting to workwechat: %s" % e)

        elastalert_logger.info("Trigger sent to workwechat")

    def get_info(self):
        return {
            "type": "workwechat",
            "work_wechat_webhook_url": self.work_wechat_webhook_url
        }
