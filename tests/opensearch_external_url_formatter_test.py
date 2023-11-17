from typing import Any
import os
import pytest

import requests
from requests.auth import AuthBase, HTTPBasicAuth

from elastalert.opensearch_external_url_formatter import AbsoluteOpensearchExternalUrlFormatter
from elastalert.opensearch_external_url_formatter import OpensearchExternalUrlFormatter
from elastalert.opensearch_external_url_formatter import create_opensearch_external_url_formatter

from elastalert.auth import RefeshableAWSRequestsAuth
from elastalert.util import EAException

from unittest import mock


class AbsoluteFormatTestCase:
    def __init__(
         self,
         base_url: str,
         relative_url: str,
         expected_url: str,
    ) -> None:
        self.base_url = base_url
        self.relative_url = relative_url
        self.expected_url = expected_url


@pytest.mark.parametrize("test_case", [
    # Relative to OpenSearch Dashboards
    AbsoluteFormatTestCase(
        base_url='http://opensearch.test.org/_dashboards/',
        relative_url='app/dev_tools#/console',
        expected_url='http://opensearch.test.org/_dashboards/app/dev_tools#/console'
    ),
])


def test_absolute_opensearch_external_url_formatter(
    test_case: AbsoluteFormatTestCase
):
    formatter = AbsoluteOpensearchExternalUrlFormatter(
        base_url=test_case.base_url
    )
    actualUrl = formatter.format(test_case.relative_url)
    print(actualUrl)
    assert actualUrl == test_case.expected_url
