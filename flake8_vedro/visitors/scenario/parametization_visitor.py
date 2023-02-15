import ast

from flake8_plugin_utils import Visitor

from flake8_vedro.checker.parametrizarion import (
    ParametrizationChecker,
    ParametrizationContext
)
from flake8_vedro.confiig import Config


class ParametrizationVisitor(Visitor):
    def __init__(self, config: Config, **kwargs) -> None:
        super(ParametrizationVisitor, self).__init__(config=config)

    def visit_ClassDef(self, node: ast.ClassDef):
        if node.name == 'Scenario':

            context = ParametrizationContext(report_error=self.error_from_node,
                                             max_params_count=self.config.max_params_count)
            ParametrizationChecker.check(node, context)
