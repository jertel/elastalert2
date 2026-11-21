import datetime
import hashlib
import json
import re

import requests
from requests.exceptions import RequestException

from elastalert.alerts import Alerter
from elastalert.util import EAException, elastalert_logger, lookup_es_key, ts_now, ts_to_dt

SMSTUNNEL_URL = 'https://smstunnel.io/api/v1/sms/send'
SMSTUNNEL_TIMEOUT = 10
SMSTUNNEL_MAX_LENGTH = 1600
SMSTUNNEL_CROP_NOTE = '\n(message cropped due to SMS limit)'
# The API remembers an Idempotency-Key for 24 hours, while ElastAlert retries a failed alert for
# alert_time_limit (2 days by default). Past this age a retry could send the text a second time.
SMSTUNNEL_MAX_ALERT_AGE = datetime.timedelta(hours=23)


class SMSTunnelAlerter(Alerter):
    """ Sends an alert as one text to one number through the SMSTunnel API """
    required_options = frozenset(['smstunnel_api_key', 'smstunnel_to'])

    def __init__(self, rule):
        super(SMSTunnelAlerter, self).__init__(rule)
        self.smstunnel_api_key = self.rule.get('smstunnel_api_key', None)
        self.smstunnel_to = self.rule.get('smstunnel_to', None)
        self.smstunnel_device_id = self.rule.get('smstunnel_device_id', None)

        # Checked here and not in schema.yaml, whose error would print the number in the log
        if not isinstance(self.smstunnel_to, str) or not re.fullmatch(r'\+[1-9][0-9]{6,14}', self.smstunnel_to):
            raise EAException('smstunnel_to must be exactly one number in international format, '
                              'as a quoted string such as "+14155550123"')
        if not isinstance(self.smstunnel_api_key, str) or not re.fullmatch(r'[\x21-\x7e]+', self.smstunnel_api_key):
            raise EAException('smstunnel_api_key must be a single API key without spaces')

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
        # A system error notification (notify_alert) carries the whole failed rule, secrets included
        matches = [{'timestamp': match['timestamp'], 'message': match['message']}
                   if set(match) == {'timestamp', 'message', 'rule'} else match for match in matches]
        body = self.create_alert_body(matches).strip()
        # Counted in UTF-16 units, as a phone counts them: an emoji takes two. 1600 units are at most 24 SMS
        # parts, while 1600 emoji would be 48, more than Android lets an app send in a minute.
        encoded = body.encode('utf-16-le', 'surrogatepass')
        if len(encoded) > SMSTUNNEL_MAX_LENGTH * 2:
            kept = encoded[:(SMSTUNNEL_MAX_LENGTH - len(SMSTUNNEL_CROP_NOTE)) * 2]
            body = kept.decode('utf-16-le', 'ignore') + SMSTUNNEL_CROP_NOTE
        return body

    def alert(self, matches):
        alert_time = self.get_alert_time()
        if alert_time and ts_now() - alert_time > SMSTUNNEL_MAX_ALERT_AGE:
            raise EAException('Error posting SMSTunnel alert: not sending an alert older than 23 hours, '
                              'because an earlier attempt may already have sent it')

        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': self.smstunnel_api_key
        }
        if alert_time:
            headers['Idempotency-Key'] = self.get_idempotency_key(alert_time, matches)

        payload = {
            'to': self.smstunnel_to,
            'message': self.create_text(matches)
        }
        if self.smstunnel_device_id:
            payload['deviceId'] = self.smstunnel_device_id

        try:
            # A redirect would carry the key to another address, so it counts as a failure
            response = requests.post(SMSTUNNEL_URL, json=payload, headers=headers,
                                     timeout=SMSTUNNEL_TIMEOUT, allow_redirects=False)
        except RequestException as e:
            # Only the error's type: its text and context are kept out of the logs
            raise EAException('Error posting SMSTunnel alert: no answer from the API (%s). '
                              'The text may already have been sent.' % type(e).__name__) from None

        try:
            answer = response.json()
        except ValueError:
            answer = None
        answer = answer if isinstance(answer, dict) else {}

        if not 200 <= response.status_code < 300:
            # The API's error code, never its free text
            code = answer.get('code')
            code = ' (%s)' % code if isinstance(code, str) and re.fullmatch(r'[A-Z0-9_]{1,64}', code) else ''
            raise EAException('Error posting SMSTunnel alert: HTTP %s%s' % (response.status_code, code))
        if answer.get('success') is not True:
            raise EAException('Error posting SMSTunnel alert: the API did not confirm the text. '
                              'It may already have been sent.')

        elastalert_logger.info("Alert '%s' sent to SMSTunnel" % self.rule['name'])

    def get_info(self):
        return {'type': 'smstunnel'}
