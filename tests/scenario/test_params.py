from flake8_plugin_utils import assert_error, assert_not_error

from flake8_vedro.confiig import Config
from flake8_vedro.errors.scenario import (
    ExceedMaxParamsCount,
    SubjectIsNotParametrized
)
from flake8_vedro.visitors import ParametrizationVisitor


def test_params_without_subject_substitution():
    code = """
    class Scenario(vedro.Scenario):
        subject = 'any subject'
        @params(1)
        @params(2)
        def __init__(foo): pass
    """
    assert_error(ParametrizationVisitor, code, SubjectIsNotParametrized,
                 config=Config(max_params_count=3))


def test_vedro_params_without_subject_substitution():
    code = """
    class Scenario(vedro.Scenario):
        subject = 'any subject'
        @vedro.params(1)
        @vedro.params(2)
        def __init__(foo): pass
    """
    assert_error(ParametrizationVisitor, code, SubjectIsNotParametrized,
                 config=Config(max_params_count=3))


def test_param_without_subject_substitution():
    code = """
    class Scenario(vedro.Scenario):
        subject = 'any subject'
        @params(1)
        def __init__(foo): pass
    """
    assert_not_error(ParametrizationVisitor, code, Config(max_params_count=3))


def test_params_with_subject_substitution():
    code = """
    class Scenario(vedro.Scenario):
        subject = 'any subject {any}'
        @params(1)
        @params(2)
        def __init__(foo): pass
    """
    assert_not_error(ParametrizationVisitor, code, Config(max_params_count=3))


def test_no_params_no_substitution():
    code = """
    class Scenario(vedro.Scenario):
        subject = 'any subject'
        def __init__(): pass
    """
    assert_not_error(ParametrizationVisitor, code, Config(max_params_count=1))


def test_exceeded_parameters_count():
    code = """
    class Scenario(vedro.Scenario):
        subject = 'any subject'
        @params(1, 2)
        def __init__(foo, bar): pass
    """
    assert_error(ParametrizationVisitor, code, ExceedMaxParamsCount,
                 config=Config(max_params_count=1),
                 max=1,
                 current=2)
