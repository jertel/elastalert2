import boto3
import json

from elastalert.alerts import Alerter
from elastalert.util import elastalert_logger, EAException


class SqsAlerter(Alerter):
    """Send alert using AWS SQS service"""

    required_options = frozenset(["sqs_queue_url"])

    def __init__(self, *args):
        super(SqsAlerter, self).__init__(*args)
        self.sqs_queue_url = self.rule.get("sqs_queue_url", None)
        self.sqs_aws_access_key_id = self.rule.get("sqs_aws_access_key_id")
        self.sqs_aws_secret_access_key = self.rule.get("sqs_aws_secret_access_key")
        self.sqs_aws_region = self.rule.get("sqs_aws_region", "us-east-1")
        self.profile = self.rule.get("sqs_aws_profile", None)

    def alert(self, matches):
        # Create the alert as a JSON object
        alert_data = {
            "rule_name": self.rule["name"],
            "matches": matches,
        }
        alert_text = self.create_alert_body(matches)
        # SQS message body limit is 256 KB; crop text at 128 KB to be safe
        if len(alert_text) > 128000:
            alert_text = alert_text[:128000]
            alert_text += "\n*message was cropped according to SQS limits!*"
        alert_data["text"] = alert_text
        body = json.dumps(alert_data, default=str)

        # If the body is still too long, remove the text field
        if len(body) > 256000:
            alert_data["text"] = "Text message omitted due to SQS size limit."
            body = json.dumps(alert_data, default=str)
        try:
            if self.profile is None:
                session = boto3.Session(
                    aws_access_key_id=self.sqs_aws_access_key_id,
                    aws_secret_access_key=self.sqs_aws_secret_access_key,
                    region_name=self.sqs_aws_region,
                )
            else:
                session = boto3.Session(profile_name=self.profile)

            sqs_client = session.client("sqs")

            sqs_client.send_message(
                QueueUrl=self.sqs_queue_url,
                MessageBody=body,  # Send the JSON body directly
            )
        except Exception as e:
            raise EAException("Error sending Amazon SQS: %s" % e)
        elastalert_logger.info("Sent Amazon SQS message to %s" % (self.sqs_queue_url))

    def get_info(self):
        return {"type": "sqs"}
