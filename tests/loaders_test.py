# -*- coding: utf-8 -*-
from base64 import b64encode
import copy
import datetime
import os

from unittest import mock
import pytest

import elastalert.alerts
import elastalert.ruletypes
from elastalert.alerters.email import EmailAlerter
from elastalert.config import load_conf
from elastalert.loaders import (
    FileRulesLoader,
    RulesLoader,
    load_rule_schema,
)

from elastalert.util import EAException


loaders_test_cases_path = os.path.join(os.path.dirname(__file__), 'loaders_test_cases')
empty_folder_test_path = os.path.join(loaders_test_cases_path, 'empty')

test_config = {'rules_folder': empty_folder_test_path,
               'run_every': {'minutes': 10},
               'buffer_time': {'minutes': 10},
               'es_host': 'elasticsearch.test',
               'es_port': 12345,
               'writeback_index': 'test_index'}

test_rule = {'es_host': 'test_host',
             'es_port': 12345,
             'name': 'testrule',
             'type': 'spike',
             'spike_height': 2,
             'spike_type': 'up',
             'timeframe': {'minutes': 10},
             'index': 'test_index',
             'query_key': 'testkey',
             'compare_key': 'comparekey',
             'filter': [{'term': {'key': 'value'}}],
             'alert': 'email',
             'use_count_query': True,
             'email': 'test@test.test',
             'aggregation': {'hours': 2},
             'include': ['comparekey', '@timestamp']}

test_args = mock.Mock()
test_args.config = 'test_config'
test_args.rule = None
test_args.debug = False
test_args.es_debug_trace = None


def test_import_rules():
    rules_loader = FileRulesLoader(test_config)
    test_rule_copy = copy.deepcopy(test_rule)
    test_rule_copy['type'] = 'testing.test.RuleType'
    with mock.patch.object(rules_loader, 'load_yaml') as mock_open:
        mock_open.return_value = test_rule_copy

        # Test that type is imported
        with mock.patch('builtins.__import__') as mock_import:
            mock_import.return_value = elastalert.ruletypes
            rules_loader.load_configuration('test_config', test_config)
        assert mock_import.call_args_list[0][0][0] == 'testing.test'
        assert mock_import.call_args_list[0][0][3] == ['RuleType']

        # Test that alerts are imported
        test_rule_copy = copy.deepcopy(test_rule)
        mock_open.return_value = test_rule_copy
        test_rule_copy['alert'] = 'testing2.test2.Alerter'
        with mock.patch('builtins.__import__') as mock_import:
            mock_import.return_value = elastalert.alerts
            rules_loader.load_configuration('test_config', test_config)
        assert mock_import.call_args_list[0][0][0] == 'testing2.test2'
        assert mock_import.call_args_list[0][0][3] == ['Alerter']


def test_import_import():
    rules_loader = FileRulesLoader(test_config)
    import_rule = copy.deepcopy(test_rule)
    del(import_rule['es_host'])
    del(import_rule['es_port'])
    import_rule['import'] = 'importme.ymlt'
    import_me = {
        'es_host': 'imported_host',
        'es_port': 12349,
        'email': 'ignored@email',  # overwritten by the email in import_rule
    }

    with mock.patch.object(rules_loader, 'get_yaml') as mock_open:
        mock_open.side_effect = [import_rule, import_me]
        rules = rules_loader.load_configuration('blah.yaml', test_config)
        assert mock_open.call_args_list[0][0] == ('blah.yaml',)
        assert mock_open.call_args_list[1][0] == ('importme.ymlt',)
        assert len(mock_open.call_args_list) == 2
        assert rules['es_port'] == 12349
        assert rules['es_host'] == 'imported_host'
        assert rules['email'] == ['test@test.test']
        assert rules['filter'] == import_rule['filter']

        # check global import_rule dependency
        assert rules_loader.import_rules == {'blah.yaml': ['importme.ymlt']}


def test_import_absolute_import():
    rules_loader = FileRulesLoader(test_config)
    import_rule = copy.deepcopy(test_rule)
    del(import_rule['es_host'])
    del(import_rule['es_port'])
    import_rule['import'] = '/importme.ymlt'
    import_me = {
        'es_host': 'imported_host',
        'es_port': 12349,
        'email': 'ignored@email',  # overwritten by the email in import_rule
    }

    with mock.patch.object(rules_loader, 'get_yaml') as mock_open:
        mock_open.side_effect = [import_rule, import_me]
        rules = rules_loader.load_configuration('blah.yaml', test_config)
        assert mock_open.call_args_list[0][0] == ('blah.yaml',)
        assert mock_open.call_args_list[1][0] == ('/importme.ymlt',)
        assert len(mock_open.call_args_list) == 2
        assert rules['es_port'] == 12349
        assert rules['es_host'] == 'imported_host'
        assert rules['email'] == ['test@test.test']
        assert rules['filter'] == import_rule['filter']


def test_import_filter():
    # Check that if a filter is specified the rules are merged:

    rules_loader = FileRulesLoader(test_config)
    import_rule = copy.deepcopy(test_rule)
    del(import_rule['es_host'])
    del(import_rule['es_port'])
    import_rule['import'] = 'importme.ymlt'
    import_me = {
        'es_host': 'imported_host',
        'es_port': 12349,
        'filter': [{'term': {'ratchet': 'clank'}}],
    }

    with mock.patch.object(rules_loader, 'get_yaml') as mock_open:
        mock_open.side_effect = [import_rule, import_me]
        rules = rules_loader.load_configuration('blah.yaml', test_config)
        assert rules['filter'] == [{'term': {'ratchet': 'clank'}}, {'term': {'key': 'value'}}]


def test_load_inline_alert_rule():
    rules_loader = FileRulesLoader(test_config)
    test_rule_copy = copy.deepcopy(test_rule)
    test_rule_copy['alert'] = [
        {
            'email': {
                'email': 'foo@bar.baz'
            }
        },
        {
            'email': {
                'email': 'baz@foo.bar'
            }
        }
    ]
    test_config_copy = copy.deepcopy(test_config)
    with mock.patch.object(rules_loader, 'get_yaml') as mock_open:
        mock_open.side_effect = [test_config_copy, test_rule_copy]
        rules_loader.load_modules(test_rule_copy)
        assert isinstance(test_rule_copy['alert'][0], EmailAlerter)
        assert isinstance(test_rule_copy['alert'][1], EmailAlerter)
        assert 'foo@bar.baz' in test_rule_copy['alert'][0].rule['email']
        assert 'baz@foo.bar' in test_rule_copy['alert'][1].rule['email']


def test_load_inline_alert_rule_with_jinja():
    rules_loader = FileRulesLoader(test_config)
    test_rule_copy = copy.deepcopy(test_rule)
    test_rule_copy['alert'] = [
        {
            'email': {
                'alert_text_type': 'alert_text_jinja',
                'alert_text': '{{ myjinjavar }}'
            }
        },
        {
            'email': {
                'alert_text': 'hello'
            }
        }
    ]
    test_config_copy = copy.deepcopy(test_config)
    with mock.patch.object(rules_loader, 'get_yaml') as mock_open:
        mock_open.side_effect = [test_config_copy, test_rule_copy]
        rules_loader.load_modules(test_rule_copy)
        assert isinstance(test_rule_copy['alert'][0], EmailAlerter)
        assert isinstance(test_rule_copy['alert'][1], EmailAlerter)
        assert 'jinja_template' in test_rule_copy['alert'][0].rule
        assert 'jinja_template' not in test_rule_copy['alert'][1].rule


def test_file_rules_loader_get_names_recursive():
    conf = {'scan_subdirectories': True, 'rules_folder': empty_folder_test_path}
    rules_loader = FileRulesLoader(conf)
    walk_paths = (('root', ['folder_a', 'folder_b'], ('rule.yaml',)),
                  ('root/folder_a', [], ('a.yaml', 'ab.yaml')),
                  ('root/folder_b', [], ('b.yaml',)))
    with mock.patch('os.walk') as mock_walk:
        mock_walk.return_value = walk_paths
        paths = rules_loader.get_names(conf)

    paths = [p.replace(os.path.sep, '/') for p in paths]

    assert 'root/rule.yaml' in paths
    assert 'root/folder_a/a.yaml' in paths
    assert 'root/folder_a/ab.yaml' in paths
    assert 'root/folder_b/b.yaml' in paths
    assert len(paths) == 4


def test_file_rules_loader_get_names_invalid_path():
    conf = {'scan_subdirectories': True, 'rules_folder': './folder_missing#XYZ'}
    try:
        # folder missing so FileRulesLoader must throws an error
        if FileRulesLoader(conf).get_names(conf):
            assert False
    except EAException:
        pass


def test_file_rules_loader_get_names():

    class MockDirEntry:
        # os.DirEntry of os.scandir
        def __init__(self, name):
            self.name = name

    # Check for no subdirectory
    conf = {'scan_subdirectories': False, 'rules_folder': 'root'}
    rules_loader = FileRulesLoader(conf)
    files = [MockDirEntry(name='badfile'), MockDirEntry('a.yaml'), MockDirEntry('b.yaml')]

    with mock.patch('os.path.isdir') as mock_dir:
        with mock.patch('os.scandir') as mock_list:
            with mock.patch('os.path.isfile') as mock_path:
                mock_dir.return_value = conf['rules_folder']
                mock_path.return_value = True
                mock_list.return_value = files
                paths = rules_loader.get_names(conf)

    paths = [p.replace(os.path.sep, '/') for p in paths]
    assert 'root/a.yaml' in paths
    assert 'root/b.yaml' in paths
    assert len(paths) == 2


def test_load_rules():
    test_rule_copy = copy.deepcopy(test_rule)
    test_config_copy = copy.deepcopy(test_config)
    with mock.patch('elastalert.config.read_yaml') as mock_conf_open:
        mock_conf_open.return_value = test_config_copy
        with mock.patch('elastalert.loaders.read_yaml') as mock_rule_open:
            mock_rule_open.return_value = test_rule_copy

            with mock.patch('os.walk') as mock_ls:
                mock_ls.return_value = [('', [], ['testrule.yaml'])]
                rules = load_conf(test_args)
                rules['rules'] = rules['rules_loader'].load(rules)
                assert isinstance(rules['rules'][0]['type'], elastalert.ruletypes.RuleType)
                assert isinstance(rules['rules'][0]['alert'][0], elastalert.alerts.Alerter)
                assert isinstance(rules['rules'][0]['timeframe'], datetime.timedelta)
                assert isinstance(rules['run_every'], datetime.timedelta)
                for included_key in ['comparekey', 'testkey', '@timestamp']:
                    assert included_key in rules['rules'][0]['include']

                # Assert include doesn't contain duplicates
                assert rules['rules'][0]['include'].count('@timestamp') == 1
                assert rules['rules'][0]['include'].count('comparekey') == 1


def test_load_default_host_port():
    test_rule_copy = copy.deepcopy(test_rule)
    test_rule_copy.pop('es_host')
    test_rule_copy.pop('es_port')
    test_config_copy = copy.deepcopy(test_config)
    with mock.patch('elastalert.config.read_yaml') as mock_conf_open:
        mock_conf_open.return_value = test_config_copy
        with mock.patch('elastalert.loaders.read_yaml') as mock_rule_open:
            mock_rule_open.return_value = test_rule_copy

            with mock.patch('os.walk') as mock_ls:
                mock_ls.return_value = [('', [], ['testrule.yaml'])]
                rules = load_conf(test_args)
                rules['rules'] = rules['rules_loader'].load(rules)

                # Assert include doesn't contain duplicates
                assert rules['es_port'] == 12345
                assert rules['es_host'] == 'elasticsearch.test'


def test_load_ssl_env_false():
    test_rule_copy = copy.deepcopy(test_rule)
    test_rule_copy.pop('es_host')
    test_rule_copy.pop('es_port')
    test_config_copy = copy.deepcopy(test_config)
    with mock.patch('elastalert.config.read_yaml') as mock_conf_open:
        mock_conf_open.return_value = test_config_copy
        with mock.patch('elastalert.loaders.read_yaml') as mock_rule_open:
            mock_rule_open.return_value = test_rule_copy

            with mock.patch('os.listdir') as mock_ls:
                with mock.patch.dict(os.environ, {'ES_USE_SSL': 'false'}):
                    mock_ls.return_value = ['testrule.yaml']
                    rules = load_conf(test_args)
                    rules['rules'] = rules['rules_loader'].load(rules)

                    assert rules['use_ssl'] is False


def test_load_ssl_env_true():
    test_rule_copy = copy.deepcopy(test_rule)
    test_rule_copy.pop('es_host')
    test_rule_copy.pop('es_port')
    test_config_copy = copy.deepcopy(test_config)
    with mock.patch('elastalert.config.read_yaml') as mock_conf_open:
        mock_conf_open.return_value = test_config_copy
        with mock.patch('elastalert.loaders.read_yaml') as mock_rule_open:
            mock_rule_open.return_value = test_rule_copy

            with mock.patch('os.listdir') as mock_ls:
                with mock.patch.dict(os.environ, {'ES_USE_SSL': 'true'}):
                    mock_ls.return_value = ['testrule.yaml']
                    rules = load_conf(test_args)
                    rules['rules'] = rules['rules_loader'].load(rules)

                    assert rules['use_ssl'] is True


def test_load_url_prefix_env():
    test_rule_copy = copy.deepcopy(test_rule)
    test_rule_copy.pop('es_host')
    test_rule_copy.pop('es_port')
    test_config_copy = copy.deepcopy(test_config)
    with mock.patch('elastalert.config.read_yaml') as mock_conf_open:
        mock_conf_open.return_value = test_config_copy
        with mock.patch('elastalert.loaders.read_yaml') as mock_rule_open:
            mock_rule_open.return_value = test_rule_copy

            with mock.patch('os.listdir') as mock_ls:
                with mock.patch.dict(os.environ, {'ES_URL_PREFIX': 'es/'}):
                    mock_ls.return_value = ['testrule.yaml']
                    rules = load_conf(test_args)
                    rules['rules'] = rules['rules_loader'].load(rules)

                    assert rules['es_url_prefix'] == 'es/'


def test_load_disabled_rules():
    test_rule_copy = copy.deepcopy(test_rule)
    test_rule_copy['is_enabled'] = False
    test_config_copy = copy.deepcopy(test_config)
    with mock.patch('elastalert.config.read_yaml') as mock_conf_open:
        mock_conf_open.return_value = test_config_copy
        with mock.patch('elastalert.loaders.read_yaml') as mock_rule_open:
            mock_rule_open.return_value = test_rule_copy

            with mock.patch('os.listdir') as mock_ls:
                mock_ls.return_value = ['testrule.yaml']
                rules = load_conf(test_args)
                rules['rules'] = rules['rules_loader'].load(rules)
                # The rule is not loaded for it has "is_enabled=False"
                assert len(rules['rules']) == 0


def test_raises_on_missing_config():
    optional_keys = ('aggregation', 'use_count_query', 'query_key', 'compare_key', 'filter', 'include', 'es_host', 'es_port', 'name')
    test_rule_copy = copy.deepcopy(test_rule)
    for key in list(test_rule_copy.keys()):
        test_rule_copy = copy.deepcopy(test_rule)
        test_config_copy = copy.deepcopy(test_config)
        test_rule_copy.pop(key)

        # Non required keys
        if key in optional_keys:
            continue

        with mock.patch('elastalert.config.read_yaml') as mock_conf_open:
            mock_conf_open.return_value = test_config_copy
            with mock.patch('elastalert.loaders.read_yaml') as mock_rule_open:
                mock_rule_open.return_value = test_rule_copy
                with mock.patch('os.walk') as mock_walk:
                    mock_walk.return_value = [('', [], ['testrule.yaml'])]
                    with pytest.raises(EAException):
                        rules = load_conf(test_args)
                        rules['rules'] = rules['rules_loader'].load(rules)


def test_compound_query_key():
    test_config_copy = copy.deepcopy(test_config)
    rules_loader = FileRulesLoader(test_config_copy)
    test_rule_copy = copy.deepcopy(test_rule)
    test_rule_copy.pop('use_count_query')
    test_rule_copy['query_key'] = ['field1', 'field2']
    rules_loader.load_options(test_rule_copy, test_config, 'filename.yaml')
    assert 'field1' in test_rule_copy['include']
    assert 'field2' in test_rule_copy['include']
    assert test_rule_copy['query_key'] == 'field1,field2'
    assert test_rule_copy['compound_query_key'] == ['field1', 'field2']


def test_query_key_with_single_value():
    test_config_copy = copy.deepcopy(test_config)
    rules_loader = FileRulesLoader(test_config_copy)
    test_rule_copy = copy.deepcopy(test_rule)
    test_rule_copy.pop('use_count_query')
    test_rule_copy['query_key'] = ['field1']
    rules_loader.load_options(test_rule_copy, test_config, 'filename.yaml')
    assert 'field1' in test_rule_copy['include']
    assert test_rule_copy['query_key'] == 'field1'
    assert 'compound_query_key' not in test_rule_copy


def test_query_key_with_no_values():
    test_config_copy = copy.deepcopy(test_config)
    rules_loader = FileRulesLoader(test_config_copy)
    test_rule_copy = copy.deepcopy(test_rule)
    test_rule_copy.pop('use_count_query')
    test_rule_copy['query_key'] = []
    rules_loader.load_options(test_rule_copy, test_config, 'filename.yaml')
    assert 'query_key' not in test_rule_copy
    assert 'compound_query_key' not in test_rule_copy


def test_name_inference():
    test_config_copy = copy.deepcopy(test_config)
    rules_loader = FileRulesLoader(test_config_copy)
    test_rule_copy = copy.deepcopy(test_rule)
    test_rule_copy.pop('name')
    rules_loader.load_options(test_rule_copy, test_config, 'msmerc woz ere.yaml')
    assert test_rule_copy['name'] == 'msmerc woz ere'


def test_kibana_discover_from_timedelta():
    test_config_copy = copy.deepcopy(test_config)
    rules_loader = FileRulesLoader(test_config_copy)
    test_rule_copy = copy.deepcopy(test_rule)
    test_rule_copy['kibana_discover_from_timedelta'] = {'minutes': 2}
    rules_loader.load_options(test_rule_copy, test_config, 'filename.yaml')
    assert isinstance(test_rule_copy['kibana_discover_from_timedelta'], datetime.timedelta)
    assert test_rule_copy['kibana_discover_from_timedelta'] == datetime.timedelta(minutes=2)


def test_kibana_discover_to_timedelta():
    test_config_copy = copy.deepcopy(test_config)
    rules_loader = FileRulesLoader(test_config_copy)
    test_rule_copy = copy.deepcopy(test_rule)
    test_rule_copy['kibana_discover_to_timedelta'] = {'minutes': 2}
    rules_loader.load_options(test_rule_copy, test_config, 'filename.yaml')
    assert isinstance(test_rule_copy['kibana_discover_to_timedelta'], datetime.timedelta)
    assert test_rule_copy['kibana_discover_to_timedelta'] == datetime.timedelta(minutes=2)


def test_rulesloader_get_names():
    try:
        RulesLoader.get_names('', '')
        assert False
    except NotImplementedError:
        assert True


def test_rulesloader_get_hashes():
    try:
        RulesLoader.get_hashes('', '')
        assert False
    except NotImplementedError:
        assert True


def test_rulesloader_get_yaml():
    try:
        RulesLoader.get_yaml('', '')
        assert False
    except NotImplementedError:
        assert True


def test_get_import_rule():
    rule = {
        'import': 'a'
    }
    result = RulesLoader.get_import_rule('', rule)
    assert 'a' == result


def test_get_rule_file_hash_when_file_not_found():
    test_config_copy = copy.deepcopy(test_config)
    rules_loader = FileRulesLoader(test_config_copy)
    hash = rules_loader.get_rule_file_hash('empty_folder_test/file_not_found.yml')
    assert isinstance(hash, bytes)
    b64Hash = b64encode(hash).decode('ascii')
    assert 'zR1Ml8y8S8Z/I5j7b48OH+DJqUw=' == b64Hash


def test_load_yaml_recursive_import():
    config = {}
    rules_loader = FileRulesLoader(config)

    trunk_path = os.path.join(loaders_test_cases_path, 'recursive_import/trunk.yaml')
    branch_path = os.path.join(loaders_test_cases_path, 'recursive_import/branch.yaml')
    leaf_path = os.path.join(loaders_test_cases_path, 'recursive_import/leaf.yaml')

    # re-load the rule a couple times to ensure import_rules cache is updated correctly
    for i in range(3):

        leaf_yaml = rules_loader.load_yaml(leaf_path)
        assert leaf_yaml == {
            'name': 'leaf',
            'rule_file': leaf_path,
            'diameter': '5cm',
        }
        assert sorted(rules_loader.import_rules.keys()) == [
            branch_path,
            leaf_path,
        ]
        assert rules_loader.import_rules[branch_path] == [
            trunk_path,
        ]
        assert rules_loader.import_rules[leaf_path] == [
            branch_path,
        ]


def test_load_yaml_multiple_imports():
    config = {}
    rules_loader = FileRulesLoader(config)

    hydrogen_path = os.path.join(loaders_test_cases_path, 'multiple_imports/hydrogen.yaml')
    oxygen_path = os.path.join(loaders_test_cases_path, 'multiple_imports/oxygen.yaml')
    water_path = os.path.join(loaders_test_cases_path, 'multiple_imports/water.yaml')

    # re-load the rule a couple times to ensure import_rules cache is updated correctly
    for i in range(3):

        water_yaml = rules_loader.load_yaml(water_path)
        assert water_yaml == {
            'name': 'water',
            'rule_file': water_path,
            'symbol': 'O',
        }
        assert sorted(rules_loader.import_rules.keys()) == [
            water_path,
        ]
        assert rules_loader.import_rules[water_path] == [
            hydrogen_path,
            oxygen_path,
        ]


def test_load_yaml_imports_modified():
    config = {}
    rules_loader = FileRulesLoader(config)

    rule_path = os.path.join(empty_folder_test_path, 'rule.yaml')
    first_import_path = os.path.join(empty_folder_test_path, 'first.yaml')
    second_import_path = os.path.join(empty_folder_test_path, 'second.yaml')

    with mock.patch.object(rules_loader, 'get_yaml') as get_yaml:
        get_yaml.side_effect = [
            {
                'name': 'rule',
                'import': first_import_path,
            },
            {
                'imported': 'first',
            }
        ]
        rule_yaml = rules_loader.load_yaml(rule_path)
        assert rule_yaml == {
            'name': 'rule',
            'rule_file': rule_path,
            'imported': 'first',
        }
        assert sorted(rules_loader.import_rules.keys()) == [
            rule_path,
        ]
        assert rules_loader.import_rules[rule_path] == [
            first_import_path
        ]

    # simulate the import changing
    with mock.patch.object(rules_loader, 'get_yaml') as get_yaml:
        get_yaml.side_effect = [
            {
                'name': 'rule',
                'import': second_import_path,
            },
            {
                'imported': 'second',
            }
        ]
        rule_yaml = rules_loader.load_yaml(rule_path)
        assert rule_yaml == {
            'name': 'rule',
            'rule_file': rule_path,
            'imported': 'second',
        }
        assert sorted(rules_loader.import_rules.keys()) == [
            rule_path,
        ]
        assert rules_loader.import_rules[rule_path] == [
            second_import_path
        ]

    # simulate the import being removed
    with mock.patch.object(rules_loader, 'get_yaml') as get_yaml:
        get_yaml.side_effect = [
            {
                'name': 'rule',
            },
        ]
        rule_yaml = rules_loader.load_yaml(rule_path)
        assert rule_yaml == {
            'name': 'rule',
            'rule_file': rule_path,
        }
        assert len(rules_loader.import_rules) == 0


def test_load_rule_schema():
    validator = load_rule_schema()
    validator.check_schema(validator.schema)
