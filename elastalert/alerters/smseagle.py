import copy
import json
import requests
import warnings

from elastalert.alerts import Alerter, DateTimeEncoder
from elastalert.util import elastalert_logger, EAException, lookup_es_key
from requests.exceptions import RequestException


class SMSEagleAlerter(Alerter):
    required_options = frozenset(['smseagle_url', 'smseagle_token', 'smseagle_message_type'])

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
    
    def get_message_type_endpoint(message_type):
        match message_type:
            case 'sms':
                return '/messages/sms'
            case 'ring':
                return '/calls/ring'
            case 'tts':
                return '/calls/tts'
            case 'tts_adv':
                return '/calls/tts_advanced'

    def format_body(self, body):
        return body
        
    def create_alert_body(self, matches):
        body = self.get_aggregation_summary_text(matches)
        if self.rule.get('alert_text_type') != 'aggregation_summary_only':
            for match in matches:
                body += str(BasicMatchString(self.rule, match))
                if len(matches) > 1:
                    body += '\n----------------------------------------\n'
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

    def alert(self, matches):
        body = self.create_alert_body(matches)

        body = self.format_body(body)
        headers = {
            'content-type': 'application/json',
            'access-token': self.smseagle_token
        }
        
        endpoint = self.get_message_type_endpoint(smseagle_message_type)

        payload = {
            "message": body
        }
        
        if not self.smseagle_to and not smseagle_contacts and not smseagle_groups:
            raise EAException("Error forwarding to SMSEagle: Missing recipients")
        
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

        for url in self.smseagle_url:
            try:
                response = requests.post(
                    url+endpoint,
                    data=json.dumps(payload, cls=DateTimeEncoder),
                    headers=headers
                )
                warnings.resetwarnings()
                response.raise_for_status()
                
                elastalert_logger.debug('Response: {0}'.format(r))
                if response.status_code != 200:
                    elastalert_logger.info("Error response from {0} \nAPI Response: {1}".format(url+endpoint, response))
            except RequestException as e:
                raise EAException("Error forwarding to SMSEagle: %s" % e)                               
        elastalert_logger.info("Alert '%s' sent to SMSEagle" % self.rule['name'])

    def get_info(self):
        ret = {'type': 'smseagle'}
        
        if self.smseagle_to:
            ret['to'] = self.smseagle_to
            
        if self.smseagle_contacts:
            ret['contacts'] = self.smseagle_contacts
                    
        if self.smseagle_groups:
            ret['groups'] = self.smseagle_groups
            
        ret['url'] = self.smseagle_url+self.get_message_type_endpoint(self.smseagle_message_type)
            
        return ret
