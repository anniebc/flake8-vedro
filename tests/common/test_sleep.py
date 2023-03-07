from flake8_plugin_utils import assert_error, assert_not_error

from flake8_vedro.errors import SleepWithConstantArgument
from flake8_vedro.visitors.call_checkers import SleepChecker
from flake8_vedro.visitors.function_call_visitor import FunctionCallVisitor


def test_call_sleep():
    FunctionCallVisitor.deregister_all()
    FunctionCallVisitor.register_checker(SleepChecker)
    code = """
    sleep(1)
    """
    assert_error(FunctionCallVisitor, code, SleepWithConstantArgument)


def test_call_sleep_in_func():
    FunctionCallVisitor.deregister_all()
    FunctionCallVisitor.register_checker(SleepChecker)
    code = """
    def foo(): sleep(1)
    """
    assert_error(FunctionCallVisitor, code, SleepWithConstantArgument)


def test_call_sleep_in_class():
    FunctionCallVisitor.deregister_all()
    FunctionCallVisitor.register_checker(SleepChecker)
    code = """
    class Test:
        def foo(): sleep(1)
    """
    assert_error(FunctionCallVisitor, code, SleepWithConstantArgument)


def test_call_sleep_with_var():
    FunctionCallVisitor.deregister_all()
    FunctionCallVisitor.register_checker(SleepChecker)
    code = """
    sleep(var)
    """
    assert_not_error(FunctionCallVisitor, code)
