# -*- coding: utf-8 -*-
import os

from setuptools import find_packages
from setuptools import setup


base_dir = os.path.dirname(__file__)
setup(
    name='elastalert2',
    version='2.31.0',
    description='Automated rule-based alerting for Elasticsearch',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jertel/elastalert2",
    setup_requires='setuptools',
    license='Apache 2.0',
    project_urls={
        "Documentation": "https://elastalert2.readthedocs.io",
        "Source Code": "https://github.com/jertel/elastalert2",
        "Discussion Forum": "https://github.com/jertel/elastalert2/discussions",
    },
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': ['elastalert-create-index=elastalert.create_index:main',
                            'elastalert-test-rule=elastalert.test_rule:main',
                            'elastalert=elastalert.elastalert:main']},
    packages=find_packages(exclude=["tests"]),
    package_data={'elastalert': ['schema.yaml', 'es_mappings/**/*.json']},
    python_requires='>=3.12',
    install_requires=[
        'apscheduler>=3.11.3,<4.0',
        'aws-requests-auth>=0.4.3',
        'boto3>=1.43.115',
        'cffi>=2.1.1',
        'croniter>=6.2.4',
        'elasticsearch==7.10.1',
        'envparse>=0.2.0',
        'exotel==0.1.5',
        'Jinja2>=3.1.6',
        'jira>=3.10.5',
        'jsonpointer>=3.4',
        'jsonschema>=4.26.0',
        'prettytable>=3.18.0',
        'prison>=0.2.1',
        'prometheus-client>=0.26.0',
        'python-dateutil>=2.9.0',
        'pytz>=2026.2',
        'pycryptodomex>=3.24.1',
        'PyYAML>=6.0.3',
        'certifi>=2026.10.19',
        'zabbix-utils>=2.0.4',
        'requests>=2.34.2',
        'requests-ntlm2>=6.6.0',
        'sortedcontainers>=2.4.0',
        'statsd-tags==3.2.1.post1',
        'stomp.py>=9.0.0',
        'tencentcloud-sdk-python>=3.1.190',
        'texttable>=1.7.2',
        'twilio>=9.12.0',
    ]
)
