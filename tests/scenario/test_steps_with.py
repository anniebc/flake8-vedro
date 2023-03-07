from flake8_plugin_utils import assert_error, assert_not_error

from flake8_vedro.errors.scenario import MockHistoryIsNotSaved
from flake8_vedro.visitors import ScenarioVisitor
from flake8_vedro.visitors.steps_checkers import MockHistoryChecker


def test_scenario_with_no_history():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockHistoryChecker)
    code = """
    class Scenario:
        def when():
            with mocked_1:
                pass
    """
    assert_error(ScenarioVisitor, code, MockHistoryIsNotSaved, mock_name='mocked_1')


def test_scenario_with_history():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockHistoryChecker)
    code = """
    class Scenario:
        def when():
            with mocked_1 as self.history:
                pass
    """
    assert_not_error(ScenarioVisitor, code)


def test_scenario_several_with_history_last():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockHistoryChecker)
    code = """
    class Scenario:
        def when():
            with mocked_1, mocked_2 as self.history:
                pass
    """
    assert_error(ScenarioVisitor, code, MockHistoryIsNotSaved, mock_name='mocked_1')


def test_scenario_several_with_history_first():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockHistoryChecker)
    code = """
    class Scenario:
        def when():
            with mocked_1 as self.history, mocked_2:
                pass

    """
    assert_error(ScenarioVisitor, code, MockHistoryIsNotSaved, mock_name='mocked_2')


def test_scenario_several_with_history_all():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockHistoryChecker)
    code = """
    class Scenario:
        def when():
            with mocked_1 as self.history_1, mocked_2 as self.history_2:
                pass
    """
    assert_not_error(ScenarioVisitor, code)


def test_scenario_with_child():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockHistoryChecker)
    code = """
    class Scenario:
        def when():
            with mocked_1 as self.history:
                with mocked_2:
                    pass
    """
    assert_error(ScenarioVisitor, code, MockHistoryIsNotSaved, mock_name='mocked_2')


def test_scenario_with_self():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_steps_checker(MockHistoryChecker)
    code = """
    class Scenario:
        def when():
            with self.mocked_1:
                pass
    """
    assert_error(ScenarioVisitor, code, MockHistoryIsNotSaved, mock_name='mocked_1')
