from flake8_plugin_utils import assert_error, assert_not_error

from flake8_vedro.config import DefaultConfig
from flake8_vedro.errors import (
    ExceedMaxParamsCount,
    FunctionCallInParams,
    SubjectIsNotParametrized
)
from flake8_vedro.visitors import ScenarioVisitor
from flake8_vedro.visitors.scenario_checkers import (
    ParametrizationCallChecker,
    ParametrizationLimitChecker,
    ParametrizationSubjectChecker
)


def test_params_without_subject_substitution():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(ParametrizationSubjectChecker)
    code = """
    class Scenario:
        subject = 'any subject'
        @params(1)
        @params(2)
        def __init__(foo): pass
    """
    assert_error(ScenarioVisitor, code, SubjectIsNotParametrized,
                 config=DefaultConfig(max_params_count=3))


def test_vedro_params_without_subject_substitution():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(ParametrizationSubjectChecker)
    code = """
    class Scenario:
        subject = 'any subject'
        @vedro.params(1)
        @vedro.params(2)
        def __init__(foo): pass
    """
    assert_error(ScenarioVisitor, code, SubjectIsNotParametrized,
                 config=DefaultConfig(max_params_count=3))


def test_param_without_subject_substitution():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(ParametrizationSubjectChecker)
    code = """
    class Scenario:
        subject = 'any subject'
        @params(1)
        def __init__(foo): pass
    """
    assert_not_error(ScenarioVisitor, code, DefaultConfig(max_params_count=3))


def test_params_with_subject_substitution():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(ParametrizationSubjectChecker)
    code = """
    class Scenario:
        subject = 'any subject {any}'
        @params(1)
        @params(2)
        def __init__(foo): pass
    """
    assert_not_error(ScenarioVisitor, code, DefaultConfig(max_params_count=3))


def test_no_params_no_substitution():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(ParametrizationSubjectChecker)
    code = """
    class Scenario:
        subject = 'any subject'
        def __init__(): pass
    """
    assert_not_error(ScenarioVisitor, code)


def test_exceeded_parameters_count():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(ParametrizationLimitChecker)
    code = """
    class Scenario:
        subject = 'any subject'
        @params(1, 2)
        def __init__(foo, bar): pass
    """
    assert_error(ScenarioVisitor, code, ExceedMaxParamsCount,
                 config=DefaultConfig(max_params_count=1),
                 max=1,
                 current=2)


def test_not_exceeded_parameters_count():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(ParametrizationLimitChecker)
    code = """
    class Scenario:
        subject = 'any subject'
        @params(1)
        def __init__(foo): pass
    """
    assert_not_error(ScenarioVisitor, code, DefaultConfig(max_params_count=1))


def test_call_func_in_params():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(ParametrizationCallChecker)
    code = """
    class Scenario:
        subject = 'any subject'
        @params(foo())
        def __init__(foo): pass
    """
    assert_error(ScenarioVisitor, code, FunctionCallInParams)


def test_call_lambda_in_params():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(ParametrizationCallChecker)
    code = """
    class Scenario:
        subject = 'any subject'
        @params(lambda: foo)
        def __init__(foo): pass
    """
    assert_not_error(ScenarioVisitor, code)


def test_constant_in_params():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(ParametrizationCallChecker)
    code = """
    class Scenario:
        subject = 'any subject'
        @params(1)
        def __init__(foo): pass
    """
    assert_not_error(ScenarioVisitor, code)
