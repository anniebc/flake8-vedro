from flake8_plugin_utils import assert_error

from flake8_vedro.errors import Print
from flake8_vedro.visitors.call_checkers import PrintChecker
from flake8_vedro.visitors.function_call_visitor import FunctionCallVisitor


def test_call_print():
    FunctionCallVisitor.deregister_all()
    FunctionCallVisitor.register_checker(PrintChecker)
    code = """
    print('asdasd')
    """
    assert_error(FunctionCallVisitor, code, Print)


def test_call_pp():
    FunctionCallVisitor.deregister_all()
    FunctionCallVisitor.register_checker(PrintChecker)
    code = """
    pp('asdasd')
    """
    assert_error(FunctionCallVisitor, code, Print)
