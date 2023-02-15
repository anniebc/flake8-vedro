from flake8_plugin_utils import assert_error, assert_not_error

from flake8_vedro.errors.common import SleepWithConstantArgument
from flake8_vedro.visitors.common_visitor import CommonVisitor


def test_call_sleep():
    code = """
    sleep(1)
    """
    assert_error(CommonVisitor, code, SleepWithConstantArgument)


def test_call_sleep_in_func():
    code = """
    def foo(): sleep(1)
    """
    assert_error(CommonVisitor, code, SleepWithConstantArgument)


def test_call_sleep_in_class():
    code = """
    class Test:
        def foo(): sleep(1)
    """
    assert_error(CommonVisitor, code, SleepWithConstantArgument)


def test_call_sleep_with_var():
    code = """
    sleep(var)
    """
    assert_not_error(CommonVisitor, code)
