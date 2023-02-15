from flake8_plugin_utils import assert_error, assert_not_error

from flake8_vedro.errors.common import (
    ArgAnnotationMissing,
    ReturnAnnotationMissing
)
from flake8_vedro.visitors.common_visitor import CommonVisitor


def test_func_no_annotation():
    code = """
    def f(var): pass
    """
    assert_error(CommonVisitor, code, ArgAnnotationMissing, arg_name='var', func_name='f')


def test_func_with_annotation():
    code = """
    def f(var: int): pass
    """
    assert_not_error(CommonVisitor, code)


def test_func_with_partial_annotation():
    code = """
    def f(var_1: int, var_2): pass
    """
    assert_error(CommonVisitor, code, ArgAnnotationMissing, arg_name='var_2', func_name='f')


def test_func_with_annotation_and_defaults():
    code = """
    def f(var_1: int, var_2: bool = True): pass
    """
    assert_not_error(CommonVisitor, code)


def test_func_without_annotation_and_defaults():
    code = """
    def f(var_1: int, var_2 = True): pass
    """
    assert_error(CommonVisitor, code, ArgAnnotationMissing, func_name='f', arg_name='var_2')


def test_func_self_arg():
    code = """
    def f(self): pass
    """
    assert_not_error(CommonVisitor, code)


def test_func_cls_arg():
    code = """
    def f(cls): pass
    """
    assert_not_error(CommonVisitor, code)


def test_func_no_return_annotation():
    code = """
    def f(): return True
    """
    assert_error(CommonVisitor, code, ReturnAnnotationMissing, func_name='f')


def test_func_return_annotation():
    code = """
    def f() -> bool: return True
    """
    assert_not_error(CommonVisitor, code)
