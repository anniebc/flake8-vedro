from flake8_plugin_utils import assert_error, assert_not_error

from flake8_vedro.errors.scenario import (
    SubjectDuplicated,
    SubjectEmpty,
    SubjectNotFound
)
from flake8_vedro.visitors.scenario.scenario_visitor import ScenarioVisitor


def test_vedro_scenario_correct_subject():
    code = """
    class Scenario(vedro.Scenario):
        subject = 'any string'
        def when(): pass
        def then(): assert True
    """
    assert_not_error(ScenarioVisitor, code)


def test_vedro_scenario_empty_subject():
    code = """
    class Scenario(vedro.Scenario):
        subject = ''
        def when(): pass
        def then(): assert True
    """
    assert_error(ScenarioVisitor, code, SubjectEmpty)


def test_vedro_scenario_no_subject():
    code = """
        class Scenario(vedro.Scenario):
            def when(): pass
            def then(): assert True
    """
    assert_error(ScenarioVisitor, code, SubjectNotFound)


def test_vedro_scenario_subject_duplicate():
    code = """
    class Scenario(vedro.Scenario):
        subject = 'string'
        subject = 'another string'
        def when(): pass
        def then(): assert True
    """
    assert_error(ScenarioVisitor, code, SubjectDuplicated)
