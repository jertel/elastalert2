import requests
from requests import RequestException
import json

from elastalert.alerts import Alerter, BasicMatchString
from elastalert.util import EAException, elastalert_logger


class LineMessageAPIAlerter(Alerter):
    """Creates a LINE Messaging API for each alert"""
    required_option = frozenset(['line_channel_access_token', 'line_to'])

    def __init__(self, rule):
        super(LineMessageAPIAlerter, self).__init__(rule)

        self.line_channel_access_token = self.rule.get('line_channel_access_token')
        self.line_to = self.rule.get('line_to')

    def alert(self, matches):
        body = ''
        for match in matches:
            body += str(BasicMatchString(self.rule, match))
            if len(matches) > 1:
                body += '\n----------------------------------------\n'

        if len(body) > 4800:
            body = body[:4700] + '\n\n(message cropped due to LINE limit)'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.line_channel_access_token)
        }

        payload = {
            'to': self.line_to,
            'messages': [
                {
                    'type': 'text',
                    'text': body
                }
            ]
        }

        try:
            response = requests.post(
                'https://api.line.me/v2/bot/message/push',
                headers=headers,
                data=json.dumps(payload)
            )
            response.raise_for_status()
        except RequestException as e:
            raise EAException('Error posting to LINE Messaging API: %s' % e)

        elastalert_logger.info('Alert sent to LINE Messaging API')

    def get_info(self):
        return {
            'type': 'line',
            'line_to': self.line_to,
            'line_channel_access_token': self.line_channel_access_token
        }
