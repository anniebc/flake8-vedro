from flake8_plugin_utils import assert_error, assert_not_error

from flake8_vedro.errors.scenario import (
    StepInvalidName,
    StepThenDuplicated,
    StepThenNotFound,
    StepWhenDuplicated,
    StepWhenNotFound
)
from flake8_vedro.visitors import StepsVisitor


def test_scenario_init_step():
    code = """
    class Scenario(vedro.Scenario):
        def __init__(self): pass
        def when(): pass
        def then(): assert foo == var
    """
    assert_not_error(StepsVisitor, code)


def test_several_given_steps():
    code = """
    class Scenario(vedro.Scenario):
        def given(): pass
        def given_another(self): pass
        def when(): pass
        def then(): assert foo == var
        def and_(self): assert foo == var
    """
    assert_not_error(StepsVisitor, code)


def test_invalid_step_name():
    code = """
    class Scenario(vedro.Scenario):
        def given(): pass
        def when(): pass
        def then(): assert foo == var
        def it_should_be(): pass
    """
    assert_error(StepsVisitor, code, StepInvalidName, step_name="it_should_be")


def test_scenario_without_when():
    code = """
    class Scenario(vedro.Scenario):
        def given(): pass
        def then(): assert foo == var
    """
    assert_error(StepsVisitor, code, StepWhenNotFound)


def test_scenario_with_when():
    code = """
    class Scenario(vedro.Scenario):
        def when(): pass
        def then(): assert foo == var
    """
    assert_not_error(StepsVisitor, code)


def test_scenario_with_when_long_name():
    code = """
    class Scenario(vedro.Scenario):
        def when_user_get(): pass
        def then(): assert foo == var
    """
    assert_not_error(StepsVisitor, code)


def test_scenario_with_duplicated_when():
    code = """
    class Scenario(vedro.Scenario):
        def when(): pass
        def when_another(): pass
        def then(): assert foo == var
    """
    assert_error(StepsVisitor, code, StepWhenDuplicated)


def test_scenario_without_then():
    code = """
    class Scenario(vedro.Scenario):
        def given(): pass
        def when(): pass
    """
    assert_error(StepsVisitor, code, StepThenNotFound)


def test_scenario_with_then_long_name():
    code = """
    class Scenario(vedro.Scenario):
        def when(): pass
        def then_it_should_return(): assert foo == var
    """
    assert_not_error(StepsVisitor, code)


def test_scenario_with_duplicated_then():
    code = """
    class Scenario(vedro.Scenario):
        def when(): pass
        def then(): assert foo == var
        def then_another(): assert foo == var
    """
    assert_error(StepsVisitor, code, StepThenDuplicated)
