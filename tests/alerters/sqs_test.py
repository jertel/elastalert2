import pytest

from elastalert.alerters.sqs import SqsAlerter
from elastalert.loaders import FileRulesLoader
from elastalert.util import EAException


def test_sqs_getinfo():
    rule = {
        "name": "Test Rule",
        "type": "any",
        "sqs_queue_url": "https://sqs.us-east-1.amazonaws.com/123456789012/my-queue",
        "sqs_aws_access_key_id": "access key id",
        "sqs_aws_secret_access_key": "secret access key",
        "alert": [],
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SqsAlerter(rule)

    expected_data = {"type": "sqs"}
    actual_data = alert.get_info()
    assert expected_data == actual_data


@pytest.mark.parametrize(
    "sqs_queue_url, expected_data",
    [
        ("", "Missing required option(s): sqs_queue_url"),
        ("https://sqs.us-east-1.amazonaws.com/123456789012/my-queue", {"type": "sqs"}),
    ],
)
def test_sqs_required_error(sqs_queue_url, expected_data):
    try:
        rule = {"name": "Test Rule", "type": "any", "alert": []}

        if sqs_queue_url:
            rule["sqs_queue_url"] = sqs_queue_url

        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = SqsAlerter(rule)

        actual_data = alert.get_info()
        assert expected_data == actual_data
    except Exception as ea:
        assert expected_data in str(ea)


def test_sqs_ea_exception():
    with pytest.raises(EAException) as ea:
        rule = {
            "name": "Test Rule",
            "type": "any",
            "sqs_queue_url": "https://sqs.us-east-1.amazonaws.com/123456789012/my-queue",
            "sqs_aws_access_key_id": "access key id",
            "sqs_aws_secret_access_key": "secret access key",
            "alert": [],
        }
        match = {
            "@timestamp": "2021-01-10T00:00:00",
            "sender_ip": "1.1.1.1",
            "hostname": "aProbe",
        }
        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = SqsAlerter(rule)
        alert.alert([match])

    assert "Error sending Amazon SQS: " in str(ea)


def test_sqs_message_size_limit():
    rule = {
        "name": "Test Rule",
        "type": "any",
        "sqs_queue_url": "https://sqs.us-east-1.amazonaws.com/123456789012/my-queue",
        "sqs_aws_access_key_id": "access key id",
        "sqs_aws_secret_access_key": "secret access key",
        "alert": [],
    }

    # Create a large match object to test message size limiting
    match = {
        "@timestamp": "2021-01-10T00:00:00",
        "sender_ip": "1.1.1.1",
        "hostname": "aProbe",
        "large_field": "x" * 200000,  # Create a field larger than the 128KB limit
    }

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SqsAlerter(rule)

    # Mock the create_alert_body method to return a large string
    original_method = alert.create_alert_body
    alert.create_alert_body = lambda matches: "x" * 150000

    # Mock boto3 session and SQS client to avoid actual AWS calls
    class MockSQSClient:
        def send_message(self, QueueUrl, MessageBody):
            # Verify message body contains truncation message
            assert len(MessageBody) <= 256000
            assert (
                "message was cropped according to SQS limits" in MessageBody
                or "Text message omitted due to SQS size limit" in MessageBody
            )
            return {}

    class MockSession:
        def __init__(
            self,
            aws_access_key_id=None,
            aws_secret_access_key=None,
            region_name=None,
            profile_name=None,
            **kwargs
        ):
            pass

        def client(self, service_name):
            return MockSQSClient()

    import boto3

    original_session = boto3.Session
    boto3.Session = MockSession

    try:
        # This should not raise an exception
        alert.alert([match])
    finally:
        # Restore original methods
        alert.create_alert_body = original_method
        boto3.Session = original_session


def test_sqs_aws_profile():
    rule = {
        "name": "Test Rule",
        "type": "any",
        "sqs_queue_url": "https://sqs.us-east-1.amazonaws.com/123456789012/my-queue",
        "sqs_aws_profile": "test-profile",
        "alert": [],
    }

    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SqsAlerter(rule)

    # Mock boto3 session to verify profile is used
    session_args = {}

    class MockSession:
        def __init__(self, **kwargs):
            nonlocal session_args
            session_args = kwargs

        def client(self, service_name):
            class MockClient:
                def send_message(self, QueueUrl, MessageBody):
                    return {}

            return MockClient()

    import boto3

    original_session = boto3.Session
    boto3.Session = MockSession

    try:
        match = {"@timestamp": "2021-01-10T00:00:00"}
        alert.alert([match])
        assert "profile_name" in session_args
        assert session_args["profile_name"] == "test-profile"
    finally:
        boto3.Session = original_session
