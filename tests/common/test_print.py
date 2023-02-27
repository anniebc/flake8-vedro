from flake8_plugin_utils import assert_error

from flake8_vedro.errors.common import Print
from flake8_vedro.visitors.function_visitor import FunctionVisitor


def test_call_print():
    code = """
    print('asdasd')
    """
    assert_error(FunctionVisitor, code, Print)


def test_call_pp():
    code = """
    pp('asdasd')
    """
    assert_error(FunctionVisitor, code, Print)
