import copy
import json
import requests
import warnings

from elastalert.alerts import Alerter, DateTimeEncoder
from elastalert.util import elastalert_logger, EAException, lookup_es_key
from requests.exceptions import RequestException


class SMSEagleAlerter(Alerter):
    required_options = set(['smseagle_url'])

    def __init__(self, rule):
        super(SMSEagleAlerter, self).__init__(rule)
        self.smseagle_url = self.rule.get('smseagle_url', None)
        if isinstance(self.smseagle_url, str):
            self.smseagle_url = [self.smseagle_url]
            
        self.smseagle_token = self.rule.get('smseagle_token', '')
        self.smseagle_message_type = self.rule.get('smseagle_message_type', '')
        self.smseagle_text = self.rule.get('smseagle_text', '')
        
        self.smseagle_to = self.rule.get('smseagle_to', '')
        self.smseagle_contacts = self.rule.get('smseagle_contacts', '')
        self.smseagle_groups = self.rule.get('smseagle_groups', '')
        
        self.smseagle_duration = self.rule.get('smseagle_duration', '')
        self.smseagle_voice_id = self.rule.get('smseagle_voice_id', '')

    def format_body(self, body):
        return body

    def get_aggregation_summary_text__maximum_width(self):
        width = super(SMSEagleAlerter, self).get_aggregation_summary_text__maximum_width()
        return min(width, 75)

    def get_aggregation_summary_text(self, matches):
        text = super(SMSEagleAlerter, self).get_aggregation_summary_text(matches)
        if text:
            text = '```\n{0}```\n'.format(text)
        return text

    def populate_fields(self, matches):
        alert_fields = []
        for arg in self.smseagle_alert_fields:
            arg = copy.copy(arg)
            arg['value'] = lookup_es_key(matches[0], arg['value'])
            alert_fields.append(arg)
        return alert_fields

#todo
    def alert(self, matches):
        body = self.create_alert_body(matches)

        body = self.format_body(body)
        headers = {
            'content-type': 'application/json',
            'access-token': self.smseagle_token
        }

        payload = {
            "message": body
        }
        
        if self.smseagle_to:
            payload['to'] = self.smseagle_to
            
        if self.smseagle_contacts:
            payload['contacts'] = self.smseagle_contacts
                    
        if self.smseagle_groups:
            payload['groups'] = self.smseagle_groups
                    
        if self.smseagle_message_type in ['ring', 'tts', 'tts_adv']:
            if self.smseagle_duration:
                payload['duration'] = self.smseagle_duration
            else:
                payload['duration'] = 10
            
        if self.smseagle_message_type == 'tts_adv':
            if self.smseagle_voice_id:
                payload['voice_id'] = self.smseagle_voice_id
            else:
                payload['voice_id'] = 1
                    
        if self.smseagle_text:
            payload['message'] = self.smseagle_text

        try:
            response = requests.post(
                smseagle_url,
                data=json.dumps(payload, cls=DateTimeEncoder),
                headers=headers
            warnings.resetwarnings()
            response.raise_for_status()
        except RequestException as e:
            raise EAException("Error forwarding to SMSEagle: %s" % e)
        elastalert_logger.info("Alert '%s' sent to SMSEagle" % self.rule['name'])

    def get_info(self):
        return {'type': 'smseagle',
                'smseagle_url': self.smseagle_url}
