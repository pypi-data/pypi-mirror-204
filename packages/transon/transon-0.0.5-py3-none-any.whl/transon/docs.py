import os.path
from collections import defaultdict
import inspect

import unittest
from functools import lru_cache

import transon
from transon.tests.base import TableDataBaseCase
from transon.transformers import Transformer


@lru_cache(maxsize=None)
def get_test_cases():
    project_root = os.path.dirname(os.path.dirname(transon.__file__))
    unittest.defaultTestLoader.discover(project_root)
    return list(TableDataBaseCase.iterate_valid_cases())


@lru_cache(maxsize=None)
def get_test_cases_by_tag(tag: str):
    return [
        case
        for case in get_test_cases()
        if tag in case.tags
    ]


@lru_cache(maxsize=None)
def get_test_case_by_name(name: str):
    for case in get_test_cases():
        if case.__name__ == name:
            return case


def get_rules_docs(cls=Transformer):
    return [
        {
            'name': rule.__rule_name__,
            'doc': inspect.getdoc(rule),
        }
        for rule in cls.get_rules()
    ]


def get_rule_parameter_docs(rule_name, cls=Transformer):
    rule = cls.get_rule(rule_name)
    return [
        {
            'name': param_name,
            'doc': inspect.cleandoc(param_docs),
        }
        for param_name, param_docs in rule.__rule_params__.items()
    ]


def get_test_cases_for_rule(rule_name):
    return [
        {
            'name': case.__name__,
            'doc': inspect.getdoc(case),
            'template': case.template,
            'data': case.data,
            'result': case.result,
        }
        for case in get_test_cases_by_tag(rule_name)
    ]


def get_test_cases_for_rule_param(rule_name, param_name):
    tag = f'{rule_name}:{param_name}'
    return [
        {
            'name': case.__name__,
            'doc': inspect.getdoc(case),
            'template': case.template,
            'data': case.data,
            'result': case.result,
        }
        for case in get_test_cases_by_tag(tag)
    ]


def get_all_docs(cls=Transformer):
    return {
        'doc': inspect.getdoc(cls),
        'rules': [
            {
                'rule': rule_doc,
                'examples': [
                    case
                    for case in get_test_cases_for_rule(rule_doc['name'])
                ],
                'params': [
                    {
                        'param': param,
                        'examples': [
                            case
                            for case in get_test_cases_for_rule_param(rule_doc['name'], param['name'])
                        ]
                    }
                    for param in get_rule_parameter_docs(rule_doc['name'], cls)
                ]
            }
            for rule_doc in get_rules_docs(cls)
        ]
    }


if __name__ == '__main__':  # pragma: no cover
    import json
    print(json.dumps(get_all_docs(), indent=4))
