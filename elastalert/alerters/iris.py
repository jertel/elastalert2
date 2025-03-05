import requests
import uuid

from datetime import datetime
from requests import RequestException

from elastalert.alerts import Alerter
from elastalert.util import EAException, elastalert_logger, lookup_es_key


class IrisAlerter(Alerter):
    required_options = set(['iris_host', 'iris_api_token'])

    def __init__(self, rule):
        super(IrisAlerter, self).__init__(rule)
        self.url = f"https://{self.rule.get('iris_host')}"
        self.api_token = self.rule.get('iris_api_token')
        self.customer_id = self.rule.get('iris_customer_id', 1)
        self.ca_cert = self.rule.get('iris_ca_cert')
        self.ignore_ssl_errors = self.rule.get('iris_ignore_ssl_errors', False)
        self.description = self.rule.get('iris_description', None)
        self.overwrite_timestamp = self.rule.get('iris_overwrite_timestamp', False)
        self.type = self.rule.get('iris_type', 'alert')
        self.case_template_id = self.rule.get('iris_case_template_id', None)
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.rule.get("iris_api_token")}'
        }
        self.alert_note = self.rule.get('iris_alert_note', None)
        self.alert_source = self.rule.get('iris_alert_source', 'ElastAlert2')
        self.alert_tags = self.rule.get('iris_alert_tags', None)
        self.alert_status_id = self.rule.get('iris_alert_status_id', 2)
        self.alert_source_link = self.rule.get('iris_alert_source_link', None)
        self.alert_severity_id = self.rule.get('iris_alert_severity_id', 1)
        self.alert_context = self.rule.get('iris_alert_context', None)
        self.iocs = self.rule.get('iris_iocs', None)

    def lookup_field(self, match: dict, field_name: str, default):
        """Populates a field with values depending on the contents of the Elastalert match
        provided to it.

        Uses a similar algorithm to that implemented to populate the `alert_text_args`.
        First checks any fields found in the match provided, then any fields defined in
        the rule, finally returning the default value provided if no value can be found.
        """
        field_value = lookup_es_key(match, field_name)
        if field_value is None:
            field_value = self.rule.get(field_name, default)

        return field_value

    def make_alert_context_records(self, matches):
        alert_context = {}

        for key, value in self.alert_context.items():
            data = str(self.lookup_field(matches[0], value, ''))
            alert_context.update(
                {
                    key: data
                }
            )

        return alert_context

    def make_iocs_records(self, matches):
        iocs = []
        for record in self.iocs:
            # Duplicating match record data so we can update the ioc_value without overwriting record
            record_data = record.copy()
            record_data['ioc_value'] = lookup_es_key(matches[0], record['ioc_value'])
            if record_data['ioc_value'] is not None:
                iocs.append(record_data)
        return iocs

    def make_alert(self, matches):
        if self.overwrite_timestamp:
            event_timestamp = matches[0].get('@timestamp')
        else:
            event_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        
        alert_data = {
            "alert_title": self.create_title(matches),
            "alert_description": self.description,
            "alert_source": self.alert_source,
            "alert_severity_id": self.alert_severity_id,
            "alert_status_id": self.alert_status_id,
            "alert_source_event_time": event_timestamp,
            "alert_note": self.alert_note,
            "alert_tags": self.alert_tags,
            "alert_customer_id": self.customer_id,
        }

        # If there is an exisiting description, it will populate in alert_data otherwise update the alert_data with the create_alert_body data.
        if not self.description:
            alert_data.update(
                {"alert_description": self.create_alert_body(matches)}
            ) 

        if self.alert_source_link:
            alert_data.update(
                {"alert_source_link": self.alert_source_link}
            )

        if self.iocs:
            iocs = self.make_iocs_records(matches)
            alert_data.update(
                {"alert_iocs": iocs}
            )

        if self.alert_context:
            alert_context = self.make_alert_context_records(matches)
            alert_data.update(
                {"alert_context": alert_context}
            )

        return alert_data

    def make_case(self, matches):
        iocs = []
        case_data = {
            "case_soc_id": f"SOC_{str(uuid.uuid4())[0:6]}",
            "case_customer": self.customer_id,
            "case_name": self.rule.get('name'),
            "case_description": self.description
        }

        if self.iocs:
            iocs = self.make_iocs_records(matches)

        if self.case_template_id:
            case_data.update(
                {"case_template_id": self.case_template_id}
            )

        return case_data, iocs
    
    def alert(self, matches):
        if self.ca_cert:
            verify = self.ca_cert
        else:
            verify = not self.ignore_ssl_errors

        if self.ignore_ssl_errors:
            requests.packages.urllib3.disable_warnings()

        if 'alert' in self.type:
            alert_data = self.make_alert(matches)

            try:
                alert_response = requests.post(
                    url=f'{self.url}/alerts/add',
                    headers=self.headers,
                    json=alert_data,
                    verify=verify,
                )

                if alert_response.status_code != 200:
                    raise EAException(f"Cannot create a new alert: {alert_response.status_code}")

            except RequestException as e:
                raise EAException(f"Error posting alert to Iris: {e}")
            elastalert_logger.info('Alert sent to Iris')

        elif 'case' in self.type:
            case_data, iocs = self.make_case(matches)

            try:
                case_response = requests.post(
                    url=f'{self.url}/manage/cases/add',
                    headers=self.headers,
                    json=case_data,
                    verify=verify,
                )


                if case_response.status_code == 200:
                    case_response_data = case_response.json()
                    case_id = case_response_data.get('data', '').get('case_id')
                    for ioc in iocs:
                        ioc.update(
                            {
                                "cid": case_id
                            }
                        )

                        try:
                            response_ioc = requests.post(
                                url=f'{self.url}/case/ioc/add',
                                headers=self.headers,
                                json=ioc,
                                verify=verify,
                            )

                            if response_ioc.status_code != 200:
                                raise EAException(f"Unable to add a new IOC to the case {case_id}")

                        except RequestException as e:
                            raise EAException(f"Error when adding IOC to the case {case_id}: {e}")
                        elastalert_logger.info('IOCs successfully added to the case')

                else:
                    raise EAException(f'Cannot create a new case: {case_response.status_code}')

            except RequestException as e:
                raise EAException(f"Error posting the case to Iris: {e}")
            elastalert_logger.info('Case successfully created in Iris')

    def get_info(self):
        return {
            'type': 'IrisAlerter',
            'iris_api_endpoint': self.url
        }
