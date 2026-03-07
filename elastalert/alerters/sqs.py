import boto3
import json
from urllib.parse import urlparse

from elastalert.alerts import Alerter
from elastalert.util import elastalert_logger, EAException


def _get_region_from_sqs_url(queue_url, default_region="us-east-1"):
    """Infer the AWS region from an SQS queue URL like
    https://sqs.us-east-1.amazonaws.com/123456789012/my-queue.
    Falls back to default_region if it cannot be determined.
    """
    host = urlparse(queue_url).hostname or ""
    parts = host.split(".")
    if len(parts) >= 3 and parts[0] == "sqs":
        return parts[1]
    return default_region


class SqsAlerter(Alerter):
    """Send alert using AWS SQS service"""

    required_options = frozenset(["sqs_queue_url"])

    def __init__(self, *args):
        super(SqsAlerter, self).__init__(*args)
        self.sqs_queue_url = self.rule.get("sqs_queue_url", None)
        self.sqs_aws_access_key_id = self.rule.get("sqs_aws_access_key_id")
        self.sqs_aws_secret_access_key = self.rule.get("sqs_aws_secret_access_key")
        explicit_region = self.rule.get("sqs_aws_region")
        if explicit_region:
            self.sqs_aws_region = explicit_region
        else:
            # If no region is configured explicitly, derive it from the queue URL.
            self.sqs_aws_region = _get_region_from_sqs_url(self.sqs_queue_url or "")
        self.profile = self.rule.get("sqs_aws_profile", None)

    def alert(self, matches):
        # Create the alert as a JSON object
        alert_data = {
            "rule_name": self.rule["name"],
            "matches": matches,
        }
        alert_text = self.create_alert_body(matches)
        # SQS message body limit is 1 MB; crop text at ~800KB to be safe
        if len(alert_text) > 800000:
            alert_text = alert_text[:800000]
            alert_text += "\n*message was cropped according to SQS limits!*"
        alert_data["text"] = alert_text
        body = json.dumps(alert_data, default=str)

        # If the body is still too long, remove the text field
        if len(body) > 1048576:
            alert_data["text"] = "Text message omitted due to SQS size limit."
            body = json.dumps(alert_data, default=str)
        try:
            # Always create the session in the configured region. SQS does not
            # infer the region from the queue URL; the client region must match.
            if self.profile is None:
                session = boto3.Session(
                    aws_access_key_id=self.sqs_aws_access_key_id,
                    aws_secret_access_key=self.sqs_aws_secret_access_key,
                    region_name=self.sqs_aws_region,
                )
            else:
                session = boto3.Session(
                    profile_name=self.profile,
                    region_name=self.sqs_aws_region,
                )

            sqs_client = session.client("sqs")

            response = sqs_client.send_message(
                QueueUrl=self.sqs_queue_url,
                MessageBody=body,
            )
        except Exception as e:
            raise EAException("Error sending Amazon SQS: %s" % e)
        elastalert_logger.info("Sent Amazon SQS message to %s, MessageId: %s" % (self.sqs_queue_url, response.get("MessageId")))

    def get_info(self):
        return {"type": "sqs"}
