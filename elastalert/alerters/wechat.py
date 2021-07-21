import json
import datetime

import requests
from requests.exceptions import RequestException
from requests.auth import HTTPProxyAuth

from elastalert.alerts import Alerter
from elastalert.util import elastalert_logger, EAException


class WechatAlerter(Alerter):
    required_options = frozenset(['wechat_corp_id', 'wechat_secret', 'wechat_agent_id'])

    def __init__(self, *args):
        super(WechatAlerter, self).__init__(*args)
        self.wechat_corp_id = self.rule.get('wechat_corp_id', '')
        self.wechat_secret = self.rule.get('wechat_secret', '')
        self.wechat_agent_id = self.rule.get('wechat_agent_id', '')
        self.wechat_msgtype = self.rule.get('wechat_msgtype', 'text')
        self.wechat_to_party = self.rule.get('wechat_to_party', None)
        self.wechat_to_user = self.rule.get('wechat_to_user', None)
        self.wechat_to_tag = self.rule.get('wechat_to_tag', None)
        self.wechat_textcard_url = self.rule.get('wechat_textcard_url', 'null_url')
        self.wechat_enable_duplicate_check = self.rule.get('wechat_enable_duplicate_check', 0)
        self.wechat_duplicate_check_interval = self.rule.get('wechat_duplicate_check_interval', 1800)

        self.wechat_proxy = self.rule.get('wechat_proxy', None)
        self.wechat_proxy_login = self.rule.get('wechat_proxy_login', None)
        self.wechat_proxy_password = self.rule.get('wechat_proxy_pass', None)
        self.proxies = {'https': self.wechat_proxy} if self.wechat_proxy else None
        self.auth = HTTPProxyAuth(self.wechat_proxy_login, self.wechat_proxy_password) if self.wechat_proxy_login else None

        self.wechat_access_token = ''
        self.wechat_token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'
        self.wechat_message_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'
        self.expires_in = datetime.datetime.now() - datetime.timedelta(seconds=3600)

    def get_token(self):
        if self.expires_in >= datetime.datetime.now() and self.wechat_access_token:
            return

        try:
            response = requests.get(self.wechat_token_url.format(self.wechat_corp_id,
                                    self.wechat_secret), proxies=self.proxies, auth=self.auth)
            response.raise_for_status()
        except RequestException as e:
            raise EAException('Get wechat access_token failed , stacktrace:%s' % e)

        token_json = response.json()

        if 'access_token' not in token_json:
            raise EAException('Get wechat access_token failed, cause :%s' % response.text())

        self.wechat_access_token = token_json['access_token']
        self.expires_in = datetime.datetime.now() + datetime.timedelta(seconds=token_json['expires_in'])

    def format_body(self, body):
        return body.encode('utf8')

    def alert(self, matches):
        if not self.wechat_to_user and not self.wechat_to_party and not self.wechat_to_tag:
            raise EAException('All wechat_to_user & wechat_to_party & wechat_to_tag invalid.')

        self.get_token()
        headers = {'content-type': 'application/json'}
        title = self.create_title(matches)
        body = self.create_alert_body(matches)

        # message was cropped, see: https://work.weixin.qq.com/api/doc/90000/90135/90236
        if len(body) > 2048:
            body = body[:2045] + "..."

        payload = {
            'touser': self.wechat_to_user or '',
            'toparty': self.wechat_to_party or '',
            'totag': self.wechat_to_tag or '',
            'agentid': self.wechat_agent_id,
            'enable_duplicate_check': self.wechat_enable_duplicate_check,
            'duplicate_check_interval': self.wechat_duplicate_check_interval
        }

        if self.wechat_msgtype == 'text':
            payload['msgtype'] = 'text'
            payload['text'] = {
                'content': body
            }
        elif self.wechat_msgtype == 'textcard':
            payload['msgtype'] = 'textcard'
            payload['textcard'] = {
                'title': title,
                'description': body,
                'url': self.wechat_textcard_url
            }
        elif self.wechat_msgtype == 'markdown':
            payload['msgtype'] = 'markdown'
            payload['markdown'] = {
                'content': body
            }

        try:
            response = requests.post(self.wechat_message_url.format(self.wechat_access_token), data=json.dumps(
                payload, ensure_ascii=False), headers=headers, proxies=self.proxies, auth=self.auth)
            response.raise_for_status()
        except RequestException as e:
            raise EAException('Error sending wechat msg: %s' % e)
        elastalert_logger.info('Alert sent to wechat.')

    def get_info(self):
        return {'type': 'wechat'}
