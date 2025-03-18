import copy
import json
import requests

from elastalert.alerts import Alerter, DateTimeEncoder
from elastalert.util import EAException, elastalert_logger, lookup_es_key, expand_string_into_array
from requests.exceptions import RequestException


class MsPowerAutomateAlerter(Alerter):
    """ Creates a Microsoft Power Automate message for each alert """
    required_options = frozenset(['ms_power_automate_webhook_url'])

    def __init__(self, rule):
        super(MsPowerAutomateAlerter, self).__init__(rule)
        self.ms_power_automate_webhook_url = self.rule.get('ms_power_automate_webhook_url', None)
        if isinstance(self.ms_power_automate_webhook_url, str):
            self.ms_power_automate_webhook_url = [self.ms_power_automate_webhook_url]
        self.ms_power_automate_proxy = self.rule.get('ms_power_automate_proxy', None)
        self.ms_power_automate_alert_summary = self.rule.get('ms_power_automate_alert_summary', None)
        self.ms_power_automate_summary_text_size = self.rule.get('ms_power_automate_summary_text_size', 'large')
        self.ms_power_automate_body_text_size = self.rule.get('ms_power_automate_body_text_size', '')
        self.ms_power_automate_ca_certs = self.rule.get('ms_power_automate_ca_certs')
        self.ms_power_automate_ignore_ssl_errors = self.rule.get('ms_power_automate_ignore_ssl_errors', False)
        self.ms_power_automate_alert_facts = self.rule.get('ms_power_automate_alert_facts', '')
        self.ms_power_automate_kibana_discover_color = self.rule.get('ms_power_automate_kibana_discover_color', 'default')
        self.ms_power_automate_kibana_discover_attach_url = self.rule.get('ms_power_automate_kibana_discover_attach_url', False)
        self.ms_power_automate_kibana_discover_title = self.rule.get('ms_power_automate_kibana_discover_title', 'Discover in Kibana')
        self.ms_power_automate_opensearch_discover_color = self.rule.get('ms_power_automate_opensearch_discover_color', 'default')
        self.ms_power_automate_opensearch_discover_attach_url = self.rule.get('ms_power_automate_opensearch_discover_attach_url', False)
        self.ms_power_automate_opensearch_discover_title = self.rule.get('ms_power_automate_opensearch_discover_title', 'Discover in opensearch')
        self.ms_power_automate_teams_card_width_full = self.rule.get('ms_power_automate_teams_card_width_full', False)

    def populate_facts(self, matches):
        alert_facts = []
        for arg in self.ms_power_automate_alert_facts:
            arg = copy.copy(arg)
            matched_value = lookup_es_key(matches[0], arg['value'])
            arg['value'] = matched_value if matched_value is not None else arg['value']
            alert_facts.append(arg)
        return alert_facts

    def alert(self, matches):
        body = self.create_alert_body(matches)

        title = self.create_title(matches)
        summary = title if self.ms_power_automate_alert_summary is None else self.ms_power_automate_alert_summary
        # post to Power Automate
        headers = {'content-type': 'application/json'}

        if self.ms_power_automate_ca_certs:
            verify = self.ms_power_automate_ca_certs
        else:
            verify = not self.ms_power_automate_ignore_ssl_errors
        if self.ms_power_automate_ignore_ssl_errors:
            requests.packages.urllib3.disable_warnings()

        # set https proxy, if it was provided
        proxies = {'https': self.ms_power_automate_proxy} if self.ms_power_automate_proxy else None
        payload = {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": {
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "version": "1.4",
                        "body": [
                            {
                                "type": "TextBlock",
                                "text": summary,
                                "weight": "Bolder",
                                "wrap": True,
                                "size": self.ms_power_automate_summary_text_size
                            },
                            {
                                "type": "TextBlock",
                                "text": body,
                                "spacing": "Large",
                                "wrap": True
                            }
                        ],
                        "actions": []
                    }
                }
            ]
        }

        if self.ms_power_automate_body_text_size != '':
            payload['attachments'][0]['content']['body'][1]['size'] = self.ms_power_automate_body_text_size

        if self.ms_power_automate_teams_card_width_full:
            payload['attachments'][0]['content']['msteams'] = {
                "width": "Full"
            }

        if self.ms_power_automate_alert_facts != '':
            facts = self.populate_facts(matches)
            payload['attachments'][0]['content']['body'].append({
                "type": "FactSet",
                "facts": [{"title": fact['name'], "value": fact['value']} for fact in facts]
            })    
            
        if self.ms_power_automate_kibana_discover_attach_url:
            kibana_discover_url = lookup_es_key(matches[0], 'kibana_discover_url')
            if kibana_discover_url:
                payload['attachments'][0]['content']['actions'].append({
                    "type": "Action.OpenUrl",
                    "title": self.ms_power_automate_kibana_discover_title,
                    "url": kibana_discover_url,
                    "style": self.ms_power_automate_kibana_discover_color
                })    

        if self.ms_power_automate_opensearch_discover_attach_url:
            opensearch_discover_url = lookup_es_key(matches[0], 'opensearch_discover_url')
            if opensearch_discover_url:
                payload['attachments'][0]['content']['actions'].append({
                    "type": "Action.OpenUrl",
                    "title": self.ms_power_automate_opensearch_discover_title,
                    "url": opensearch_discover_url,
                    "style": self.ms_power_automate_opensearch_discover_color
                })                     
        urls = self.ms_power_automate_webhook_url
        if 'ms_power_automate_webhook_url_from_field' in self.rule:
            webhook = lookup_es_key(matches[0], self.rule['ms_power_automate_webhook_url_from_field'])
            if isinstance(webhook, str):
                urls = expand_string_into_array(webhook)

        for url in urls:
            try:
                response = requests.post(url, data=json.dumps(payload, cls=DateTimeEncoder),
                                         headers=headers, proxies=proxies, verify=verify)
                response.raise_for_status()
            except RequestException as e:
                raise EAException("Error posting to Power Automate: %s" % e)
        elastalert_logger.info("Alert sent to Power Automate")

    def get_info(self):
        return {'type': 'ms_power_automate',
                'ms_power_automate_webhook_url': self.ms_power_automate_webhook_url}
