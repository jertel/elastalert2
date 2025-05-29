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
    
    def get_message_type_endpoint(self, message_type):
        match message_type:
            case 'ring':
                return '/calls/ring'
            case 'tts':
                return '/calls/tts'
            case 'tts_adv':
                return '/calls/tts_advanced'
            case _:
                return '/messages/sms'

    def alert(self, matches):
        body = self.create_alert_body(matches)

        headers = {
            'content-type': 'application/json',
            'access-token': self.smseagle_token
        }
        
        endpoint = self.get_message_type_endpoint(self.smseagle_message_type)

        payload = {
            "text": body
        }
        
        if not self.smseagle_to and not self.smseagle_contacts and not self.smseagle_groups:
            raise EAException("Error posting SMSEagle alert: Missing recipients")
        
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
            payload['text'] = self.smseagle_text

        for url in self.smseagle_url:
            try:
                response = requests.post(
                    url+endpoint,
                    json=payload,
                    headers=headers
                )
                warnings.resetwarnings()
                response.raise_for_status()
                
                elastalert_logger.debug('Response: {0}'.format(response))
            except RequestException as e:
                raise EAException("Error posting SMSEagle alert: %s" % e)                               
        elastalert_logger.info("Alert '%s' sent to SMSEagle" % self.rule['name'])

    def get_info(self):
        return {'type': 'smseagle',
        'smseagle_webhook_url': self.smseagle_url}
            
        return ret
