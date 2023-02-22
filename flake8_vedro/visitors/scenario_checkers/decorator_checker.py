import ast
from typing import List

from flake8_plugin_utils import Error

from flake8_vedro.errors.scenario import DecoratorVedroOnly
from flake8_vedro.visitors.scenario_visitor import (
    Context,
    ScenarioChecker,
    ScenarioVisitor
)


@ScenarioVisitor.register_scenario_checker
class VedroOnlyChecker(ScenarioChecker):

    @staticmethod
    def check_scenario(context: Context, *args) -> List[Error]:
        for decorator in context.scenario_node.decorator_list:
            if (
                    isinstance(decorator, ast.Attribute)
                    and decorator.value.id == 'vedro'
                    and decorator.attr == 'only'
            ):
                return [DecoratorVedroOnly(decorator.lineno, decorator.col_offset)]
        return []
