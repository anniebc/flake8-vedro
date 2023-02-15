from flake8_plugin_utils import assert_error, assert_not_error

from flake8_vedro.errors.scenario import StepsWrongOrder
from flake8_vedro.visitors import StepsVisitor


def test_scenario_no_given():
    code = """
    class Scenario(vedro.Scenario):
        def when(): pass
        def then(): assert foo == var
    """
    assert_not_error(StepsVisitor, code)


def test_scenario_no_given_with_init():
    code = """
    class Scenario(vedro.Scenario):
        def __init__(self): pass
        def when(): pass
        def then(): assert foo == var
    """
    assert_not_error(StepsVisitor, code)


def test_scenario_no_init():
    code = """
    class Scenario(vedro.Scenario):
        def given(): pass
        def when(): pass
        def then(): assert foo == var
    """
    assert_not_error(StepsVisitor, code)


def test_scenario_several_given():
    code = """
    class Scenario(vedro.Scenario):
        def given(): pass
        def given_another(): pass
        def when(): pass
        def then(): assert foo == var
    """
    assert_not_error(StepsVisitor, code)


def test_scenario_then_before_when():
    code = """
    class Scenario(vedro.Scenario):
        def then(): assert foo == var
        def when(): pass
    """
    assert_error(StepsVisitor, code, StepsWrongOrder,
                 previous_step='then', current_step='when')


def test_scenario_given_after_when():
    code = """
    class Scenario(vedro.Scenario):
        def when(): pass
        def given(): pass
        def then(): assert foo == var
    """
    assert_error(StepsVisitor, code, StepsWrongOrder,
                 previous_step='when', current_step='given')


def test_scenario_and_before_then():
    code = """
    class Scenario(vedro.Scenario):
        def when(): pass
        def and_(): assert foo == var
        def then(): assert foo == var
    """
    assert_error(StepsVisitor, code, StepsWrongOrder,
                 previous_step='and_', current_step='then')


def test_scenario_several_and():
    code = """
    class Scenario(vedro.Scenario):
        def when(): pass
        def then_(): assert foo == var
        def and_(): assert foo == var
        def and_another(): assert foo == var
    """
    assert_not_error(StepsVisitor, code)


def test_scenario_but_after_and():
    code = """
    class Scenario(vedro.Scenario):
        def when(): pass
        def then_(): assert foo == var
        def and_(): assert foo == var
        def but(): assert foo == var
    """
    assert_not_error(StepsVisitor, code)


def test_scenario_but_before_and():
    code = """
    class Scenario(vedro.Scenario):
        def when(): pass
        def then_(): assert foo == var
        def and_(): assert foo == var
        def but(): assert foo == var
    """
    assert_not_error(StepsVisitor, code)
