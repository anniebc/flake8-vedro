import ast
from typing import List

from flake8_plugin_utils import Error

from flake8_vedro.errors.scenario import FunctionCallInParams
from flake8_vedro.helpers.get_scenario_elements import (
    get_init_step,
    get_params_decorators
)
from flake8_vedro.visitors.scenario_visitor import (
    Context,
    ScenarioChecker,
    ScenarioVisitor
)


@ScenarioVisitor.register_scenario_checker
class ParametrizationCallChecker(ScenarioChecker):

    def check_scenario(self, context: Context, config) -> List[Error]:
        errors = []

        init_node = get_init_step(context.scenario_node)

        if init_node is None or not init_node.decorator_list:
            return errors

        for decorator in get_params_decorators(init_node):
            for arg in decorator.args:
                if isinstance(arg, ast.Call):
                    errors.append(FunctionCallInParams(decorator.lineno, decorator.col_offset))
        return errors
