import datetime
import hashlib
import json

import requests
from requests.exceptions import RequestException

from elastalert.alerts import Alerter
from elastalert.util import EAException, elastalert_logger, lookup_es_key, ts_to_dt

SMSTUNNEL_URL = 'https://smstunnel.io/api/v1/sms/send'
SMSTUNNEL_CROP_NOTE = '\n(message cropped due to SMS limit)'


class SMSTunnelAlerter(Alerter):
    """ Sends an alert as one text to one number through the SMSTunnel API """
    required_options = frozenset(['smstunnel_api_key', 'smstunnel_to'])

    def __init__(self, rule):
        super(SMSTunnelAlerter, self).__init__(rule)
        self.smstunnel_api_key = self.rule.get('smstunnel_api_key', None)
        self.smstunnel_to = self.rule.get('smstunnel_to', None)
        self.smstunnel_device_id = self.rule.get('smstunnel_device_id', None)
        self.smstunnel_proxy = self.rule.get('smstunnel_proxy', None)
        self.smstunnel_timeout = self.rule.get('smstunnel_timeout', 10)
        self.smstunnel_max_length = self.rule.get('smstunnel_max_length', 1600)

    def get_alert_time(self):
        """ The alert's original time: a datetime at first, a string when ElastAlert retries it """
        try:
            return ts_to_dt(self.pipeline['alert_time']).astimezone(datetime.timezone.utc)
        except (KeyError, TypeError, ValueError, OverflowError):
            return None

    def get_idempotency_key(self, alert_time, matches):
        """ The same for every retry of this alert, and different for any other alert """
        group = None
        if self.rule.get('aggregation_key'):
            # Aggregated alerts of one rule can share an alert_time
            try:
                group = lookup_es_key(matches[0], self.rule['aggregation_key'])
            except (KeyError, IndexError, TypeError):
                group = '_missing'
        parts = [self.rule['name'], alert_time.isoformat(), self.smstunnel_to, self.smstunnel_device_id, group]
        return 'elastalert-' + hashlib.sha256(json.dumps(parts, default=str).encode()).hexdigest()

    def create_text(self, matches):
        body = self.create_alert_body(matches).strip()
        # Counted in UTF-16 units, as a phone counts them: an emoji takes two
        limit = self.smstunnel_max_length
        encoded = body.encode('utf-16-le', 'surrogatepass')
        if len(encoded) > limit * 2:
            note = SMSTUNNEL_CROP_NOTE if limit > len(SMSTUNNEL_CROP_NOTE) else ''
            kept = encoded[:(limit - len(note)) * 2]
            body = kept.decode('utf-16-le', 'ignore') + note
        return body

    def alert(self, matches):
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': self.smstunnel_api_key
        }
        alert_time = self.get_alert_time()
        if alert_time:
            # Every retry of this alert carries the same key: for 24 hours the API answers a retry with the
            # first answer instead of sending a second text
            headers['Idempotency-Key'] = self.get_idempotency_key(alert_time, matches)

        payload = {
            'to': self.smstunnel_to,
            'message': self.create_text(matches)
        }
        if self.smstunnel_device_id:
            payload['deviceId'] = self.smstunnel_device_id
        proxies = {'https': self.smstunnel_proxy} if self.smstunnel_proxy else None

        try:
            # requests would pass the X-API-Key header on to the target of a redirect
            response = requests.post(SMSTUNNEL_URL, json=payload, headers=headers, proxies=proxies,
                                     timeout=self.smstunnel_timeout, allow_redirects=False)
            response.raise_for_status()
        except RequestException as e:
            raise EAException("Error posting SMSTunnel alert: %s. Details: %s"
                              % (e, "" if e.response is None else e.response.text))

        try:
            answer = response.json()
        except ValueError:
            answer = None
        if not isinstance(answer, dict) or answer.get('success') is not True:
            raise EAException("Error posting SMSTunnel alert: the API did not confirm the text (HTTP %s). Details: %s"
                              % (response.status_code, response.text))

        elastalert_logger.info("Alert '%s' sent to SMSTunnel" % self.rule['name'])

    def get_info(self):
        return {'type': 'smstunnel'}
