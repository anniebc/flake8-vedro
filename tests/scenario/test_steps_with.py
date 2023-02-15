from flake8_plugin_utils import assert_error, assert_not_error

from flake8_vedro.errors.scenario import MockHistoryIsNotSaved
from flake8_vedro.visitors import StepsVisitor


def test_scenario_with_no_history():
    code = """
    class Scenario(vedro.Scenario):
        def when():
            with mocked_1:
                pass
        def then(): assert foo == var
    """
    assert_error(StepsVisitor, code, MockHistoryIsNotSaved, mock_name='mocked_1')


def test_scenario_with_history():
    code = """
    class Scenario(vedro.Scenario):
        def when():
            with mocked_1 as self.history:
                pass
        def then(): assert foo == var
    """
    assert_not_error(StepsVisitor, code)


def test_scenario_several_with_history_last():
    code = """
    class Scenario(vedro.Scenario):
        def when():
            with mocked_1, mocked_2 as self.history:
                pass
        def then(): assert foo == var
    """
    assert_error(StepsVisitor, code, MockHistoryIsNotSaved, mock_name='mocked_1')


def test_scenario_several_with_history_first():
    code = """
    class Scenario(vedro.Scenario):
        def when():
            with mocked_1 as self.history, mocked_2:
                pass
        def then(): assert foo == var
    """
    assert_error(StepsVisitor, code, MockHistoryIsNotSaved, mock_name='mocked_2')


def test_scenario_several_with_history_all():
    code = """
    class Scenario(vedro.Scenario):
        def when():
            with mocked_1 as self.history_1, mocked_2 as self.history_2:
                pass
        def then(): assert foo == var
    """
    assert_not_error(StepsVisitor, code)


def test_scenario_with_child():
    code = """
    class Scenario(vedro.Scenario):
        def when():
            with mocked_1 as self.history:
                with mocked_2:
                    pass
        def then(): assert foo == var
    """
    assert_error(StepsVisitor, code, MockHistoryIsNotSaved, mock_name='mocked_2')
