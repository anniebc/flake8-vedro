import ast

from flake8_plugin_utils import Visitor

from flake8_vedro.errors.common import (
    ArgAnnotationMissing,
    AssertSameObjectsForEquality,
    AssertWithConstant,
    Print,
    ReturnAnnotationMissing,
    SleepWithConstantArgument
)


class CommonVisitor(Visitor):
    """
    Check common code style helpers:
    - no print
    - no sleep(<any constant>)
    - no comparing same objects (like assert 1 = 1)
    - etc
    """

    def check_annotation(self, node: ast.FunctionDef or ast.AsyncFunctionDef):
        for arg in node.args.args:
            if arg.annotation is None and arg.arg != 'self' and arg.arg != 'cls':
                self.error_from_node(ArgAnnotationMissing, node,
                                     arg_name=arg.arg,
                                     func_name=node.name)
        for line in node.body:
            if isinstance(line, ast.Return):
                if node.returns is None:
                    self.error_from_node(ReturnAnnotationMissing, node,
                                         func_name=node.name)

    def check_sleep(self, node: ast.FunctionDef or ast.AsyncFunctionDef):
        for line in node.body:
            if isinstance(line, ast.Expr) and isinstance(line.value, ast.Call):
                self.visit_Call(line.value)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.check_annotation(node)
        self.check_sleep(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.check_annotation(node)
        self.check_sleep(node)

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            if node.func.id == 'sleep':
                if isinstance(node.args[0], ast.Constant):
                    self.error_from_node(SleepWithConstantArgument, node)

            if node.func.id == 'print' or node.func.id == 'pp':
                self.error_from_node(Print, node)

    def visit_Assert(self, node: ast.Assert):
        if isinstance(node.test, ast.Compare):

            # assert 1 == 2
            if isinstance(node.test.left, ast.Constant) and \
                    isinstance(node.test.comparators[0], ast.Constant):

                if node.test.left.value == node.test.comparators[0].value:
                    self.error_from_node(AssertSameObjectsForEquality, node)

            # assert var == var
            elif isinstance(node.test.left, ast.Name) and \
                    isinstance(node.test.comparators[0], ast.Name):
                if node.test.left.id == node.test.comparators[0].id:
                    self.error_from_node(AssertSameObjectsForEquality, node)

            # assert var == 'string' or assert var == 1
            elif isinstance(node.test.comparators[0], ast.Constant):
                self.error_from_node(AssertWithConstant, node)
