from flake8_plugin_utils import assert_error, assert_not_error

from flake8_vedro.errors.scenario import (
    DecoratorVedroOnly,
    ScenarioNotInherited
)
from flake8_vedro.visitors.scenario.scenario_visitor import ScenarioVisitor


def test_vedro_decorator_only():
    code = """
    @vedro.only
    class Scenario(vedro.Scenario):
        subject = 'any subject'
        def when(): pass
        def then(): assert True
    """
    assert_error(ScenarioVisitor, code, DecoratorVedroOnly)


def test_vedro_decorator_skip():
    code = """
    @vedro.skip
    class Scenario(vedro.Scenario):
        subject = 'any subject'
        def when(): pass
        def then(): assert True
    """
    assert_not_error(ScenarioVisitor, code)


def test_vedro_scenario_not_wrong_herietence():
    code = """
    class Scenario():
        subject = 'any subject'
        def when(): pass
        def then(): assert True
    """
    assert_error(ScenarioVisitor, code, ScenarioNotInherited)


def test_vedro_scenario_not_wrong_inherietence():
    code = """
    class Scenario(vedro.S):
        subject = 'any subject'
        def when(): pass
        def then(): assert True
    """
    assert_error(ScenarioVisitor, code, ScenarioNotInherited)


def test_vedro_scenario_right_inherietence():
    code = """
    class Scenario(vedro.Scenario):
        subject = 'any subject'
        def when(): pass
        def then(): assert True
    """
    assert_not_error(ScenarioVisitor, code)
