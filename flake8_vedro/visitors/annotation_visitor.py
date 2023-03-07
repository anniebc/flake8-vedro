import ast
from typing import Union

from flake8_vedro.abstract_checkers import ScenarioHelper
from flake8_vedro.errors import ArgAnnotationMissing, ReturnAnnotationMissing
from flake8_vedro.visitors._visitor_with_filename import VisitorWithFilename


class AnnotationVisitor(VisitorWithFilename):

    def check_annotation(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]):

        # exclude annotation check for __init__ in scenarios

        if self.config.skip_tests_init_annotation:
            if node.name == '__init__':
                if ScenarioHelper().is_scenario_in_correct_location(self.filename):
                    return

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
