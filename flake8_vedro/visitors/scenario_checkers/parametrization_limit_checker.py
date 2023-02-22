import re
from typing import List

from flake8_plugin_utils import Error

from flake8_vedro.errors.scenario import ExceedMaxParamsCount
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
class ParametrizationLimitChecker(ScenarioChecker):

    @staticmethod
    def check_scenario(context: Context, config) -> List[Error]:
        errors = []

        init_node = get_init_step(context.scenario_node)

        if init_node and init_node.decorator_list:
            for decorator in get_params_decorators(init_node):
                if len(decorator.args) > config.max_params_count:
                    errors.append(ExceedMaxParamsCount(decorator.lineno, decorator.col_offset,
                                                       current=len(decorator.args),
                                                       max=config.max_params_count))

        return errors
