from flake8_plugin_utils import assert_error, assert_not_error

from flake8_vedro.errors.common import SleepWithConstantArgument
from flake8_vedro.visitors.function_visitor import FunctionVisitor


def test_call_sleep():
    code = """
    sleep(1)
    """
    assert_error(FunctionVisitor, code, SleepWithConstantArgument)


def test_call_sleep_in_func():
    code = """
    def foo(): sleep(1)
    """
    assert_error(FunctionVisitor, code, SleepWithConstantArgument)


def test_call_sleep_in_class():
    code = """
    class Test:
        def foo(): sleep(1)
    """
    assert_error(FunctionVisitor, code, SleepWithConstantArgument)


def test_call_sleep_with_var():
    code = """
    sleep(var)
    """
    assert_not_error(FunctionVisitor, code)
