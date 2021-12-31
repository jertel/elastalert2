import copy
import json
import requests
import warnings
import os

from elastalert.alerts import Alerter, DateTimeEncoder
from elastalert.util import elastalert_logger, EAException, lookup_es_key
from requests.exceptions import RequestException
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackSdkAlerter(Alerter):
    """ Creates a Slack room message for each alert """
    required_options = frozenset(['slacksdk_channel_id'])

    def __init__(self, rule):
        super(SlackSdkAlerter, self).__init__(rule)
        self.slacksdk_channel_id = self.rule.get('slacksdk_channel_id', None)
        if isinstance(self.slacksdk_channel_id, str):
            self.slacksdk_channel_id = [self.slacksdk_channel_id]

        self.slacksdk_msg_color = self.rule.get('slacksdk_msg_color', 'danger')
        self.slacksdk_thread_text = self.rule.get('slacksdk_thread_text', None)

        # slack kibana discovery button
        self.slacksdk_kibana_button = self.rule.get('slacksdk_kibana_button', False)
        self.slacksdk_kibana_button_text = self.rule.get('slacksdk_kibana_button_text', ':kibana: Kibana')

    def _render_thread_text(self, matches):
        thread_text = ""
        for match in matches:
            template_values = self.rule | match
            thread_text += self.rule.get("thread_jinja_template").render(template_values | {self.rule['jinja_root_name']: template_values})
        return thread_text

    def alert(self, matches):
        body = self.create_alert_body(matches)
        client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

        attachements = [
            {
                "color": self.slacksdk_msg_color,
                "fallback": body,
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{self.rule['name']}*"
                        }
                    },  
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": body
                        }
                    }
                ]
            }
        ]

        if self.slacksdk_kibana_button:
            kibana_discover_url = lookup_es_key(matches[0], 'kibana_discover_url')
            if kibana_discover_url:
                attachements[0]["blocks"].append(
                     {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": self.slacksdk_kibana_button_text,
                                    "emoji": True
                                },
                                "url": kibana_discover_url
                            }
                        ]
                    }
                )

        for channel in self.slacksdk_channel_id:
            try:
                message = client.chat_postMessage(
                    channel=channel,
                    attachments = attachements
                )
                if self.slacksdk_thread_text:
                    thread = client.chat_postMessage(
                        channel=channel,
                        text=self._render_thread_text(matches),
                        thread_ts=message["ts"]
                    )
            except SlackApiError as e:
                raise EAException("Error posting to Slack (SDK): %s" % e)

        elastalert_logger.info("Alert '%s' sent to Slack (SDK)" % self.rule['name'])
        
    def get_info(self):
        return {'type': 'slacksdk'}
