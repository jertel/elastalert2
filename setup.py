# -*- coding: utf-8 -*-
import os

from setuptools import find_packages
from setuptools import setup


base_dir = os.path.dirname(__file__)
setup(
    name='elastalert2',
    version='2.27.0',
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
        'apscheduler>=3.11.0,<4.0',
        'aws-requests-auth>=0.4.3',
        'boto3>=1.40.59',
        'cffi>=2.0.0',
        'croniter>=6.0.0',
        'elasticsearch==7.10.1',
        'envparse>=0.2.0',
        'exotel==0.1.5',
        'Jinja2>=3.1.6',
        'jira>=3.10.5',
        'jsonpointer>=3.0.0',
        'jsonschema>=4.25.1',
        'prettytable>=3.16.0',
        'prison>=0.2.1',
        'prometheus_client>=0.23.1',
        'python-dateutil>=2.9.0.post0',
        'PyYAML>=6.0.3',
        'py-zabbix>=1.1.7',
        'requests>=2.31.0',
        'sortedcontainers>=2.4.0',
        'statsd-tags==3.2.1.post1',
        'stomp.py>=8.2.0',
        'tencentcloud-sdk-python>=3.0.1479',
        'texttable>=1.7.0',
        'twilio>=9.8.4',
    ]
)
