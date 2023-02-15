from flake8_plugin_utils import assert_error, assert_not_error

from flake8_vedro.errors.scenario import (
    StepAssertHasComparisonWithoutAssert,
    StepAssertHasUselessAssert,
    StepAssertWithoutAssert,
    StepHasAssert
)
from flake8_vedro.visitors import StepsVisitor


def test_scenario_then_without_assert():
    code = """
     class Scenario(vedro.Scenario):
        def when(): pass
        def then(): pass
    """
    assert_error(StepsVisitor, code, StepAssertWithoutAssert, step_name='then')


def test_scenario_and_without_assert():
    code = """
     class Scenario(vedro.Scenario):
        def when(): pass
        def then(): assert foo == var
        def and_(): pass
    """
    assert_error(StepsVisitor, code, StepAssertWithoutAssert, step_name='and_')


def test_scenario_but_without_assert():
    code = """
     class Scenario(vedro.Scenario):
        def when(): pass
        def then(): assert foo == var
        def but(): pass
    """
    assert_error(StepsVisitor, code, StepAssertWithoutAssert, step_name='but')


def test_comprasion_without_assert():
    code = """
     class Scenario(vedro.Scenario):
        def when(): pass
        def then():
            assert foo == far
            foo == var
    """
    assert_error(StepsVisitor, code, StepAssertHasComparisonWithoutAssert, step_name='then')


def test_comprasion_with_assert():
    code = """
     class Scenario(vedro.Scenario):
        def when(): pass
        def then():
            assert foo == var
    """
    assert_not_error(StepsVisitor, code)


def test_useless_assert_constant():
    code = """
    class Scenario(vedro.Scenario):
        def when(): pass
        def then():
            assert True
    """
    assert_error(StepsVisitor, code, StepAssertHasUselessAssert, step_name='then')


def test_useless_assert_var():
    code = """
    class Scenario(vedro.Scenario):
        def when(): pass
        def then():
            assert foo
    """
    assert_error(StepsVisitor, code, StepAssertHasUselessAssert, step_name='then')


def test_assert_constant_not_in_scenario():
    code = """
    def any_helper(): assert True
    """
    assert_not_error(StepsVisitor, code)


def test_scenario_with_init_with_assert():
    code = """
    class Scenario(vedro.Scenario):
        def __init__(): assert user
        def when(): pass
        def then(): assert foo == var
    """
    assert_error(StepsVisitor, code, StepHasAssert, step_name="__init__")


def test_scenario_with_given_with_assert():
    code = """
    class Scenario(vedro.Scenario):
        def given():
            user = user()
            assert user
        def when(): pass
        def then(): assert foo == var
    """
    assert_error(StepsVisitor, code, StepHasAssert, step_name="given")


def test_scenario_with_when_with_assert():
    code = """
    class Scenario(vedro.Scenario):
        def when(): assert user
        def then(): assert foo == var
    """
    assert_error(StepsVisitor, code, StepHasAssert, step_name="when")
