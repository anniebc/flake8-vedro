import ast
from functools import reduce
from typing import List, Optional, Type

from flake8_plugin_utils import Error, Visitor

from flake8_vedro.checker.steps import StepCheckContext, StepChecker
from flake8_vedro.confiig import Config


class StepsVisitor(Visitor):

    def __init__(self, config: Optional[Config] = None, **kwargs) -> None:
        super(StepsVisitor, self).__init__(config=config)
        self.imports_node = []

    def error_from_node(self, error: Type[Error],
                        node: ast.AST,
                        lineno: Optional[int] = None,
                        col_offset: Optional[int] = None,
                        **kwargs) -> None:
        if lineno is None:
            lineno = node.lineno
        if col_offset is None:
            col_offset = node.col_offset
        self.errors.append(error(lineno, col_offset, **kwargs))

    def visit_ImportFrom(self, node: ast.Import):
        """
        Save all imports from scenario (for validation ImportedInterfaceInWrongStep)
        """
        self.imports_node.append(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        if node.name == 'Scenario':

            steps: List[ast.FunctionDef or ast.AsyncFunctionDef] = [
                element for element in node.body if (
                        isinstance(element, ast.FunctionDef) or isinstance(element, ast.AsyncFunctionDef)
                )
            ]

            final_context: StepCheckContext = reduce(
                lambda context, step: StepChecker.check_step(step, context),
                steps,
                StepCheckContext(
                    report_error=self.error_from_node,
                    imports_node=self.imports_node,
                )
            )

            StepChecker.check_context(node, final_context)
