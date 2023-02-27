import ast
from typing import Union

from flake8_plugin_utils import Visitor

from flake8_vedro.errors.common import (
    ArgAnnotationMissing,
    ReturnAnnotationMissing
)


class AnnotationVisitor(Visitor):

    def check_annotation(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]):
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

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.check_annotation(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.check_annotation(node)
