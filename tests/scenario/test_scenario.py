from flake8_plugin_utils import assert_error, assert_not_error

from flake8_vedro.errors.scenario import (
    DecoratorVedroOnly,
    ScenarioNotInherited
)
from flake8_vedro.visitors import ScenarioVisitor
from flake8_vedro.visitors.scenario_checkers import (
    ParentChecker,
    VedroOnlyChecker
)


def test_vedro_decorator_only():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(VedroOnlyChecker)
    code = """
    @vedro.only
    class Scenario: pass
    """
    assert_error(ScenarioVisitor, code, DecoratorVedroOnly)


def test_vedro_decorator_skip():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(VedroOnlyChecker)
    code = """
    @vedro.skip
    class Scenario: pass
    """
    assert_not_error(ScenarioVisitor, code)


def test_vedro_scenario_not_wrong_herietence():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(ParentChecker)
    code = """
    class Scenario():
        subject = 'any subject'
        def when(): pass
        def then(): assert True
    """
    assert_error(ScenarioVisitor, code, ScenarioNotInherited)


def test_vedro_scenario_not_wrong_inherietence():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(ParentChecker)
    code = """
    class Scenario(vedro.S):
        subject = 'any subject'
        def when(): pass
        def then(): assert True
    """
    assert_error(ScenarioVisitor, code, ScenarioNotInherited)


def test_vedro_scenario_right_inherietence():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(ParentChecker)
    code = """
    class Scenario(vedro.Scenario):
        subject = 'any subject'
        def when(): pass
        def then(): assert True
    """
    assert_not_error(ScenarioVisitor, code)
