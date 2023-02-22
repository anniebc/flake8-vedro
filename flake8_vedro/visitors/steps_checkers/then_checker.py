from typing import List

from flake8_plugin_utils import Error

from flake8_vedro.errors.scenario import StepThenDuplicated, StepThenNotFound
from flake8_vedro.helpers.get_scenario_elements import get_then_steps
from flake8_vedro.visitors.scenario_visitor import (
    Context,
    ScenarioVisitor,
    StepsChecker
)


@ScenarioVisitor.register_steps_checker
class SingleThenChecker(StepsChecker):

    @staticmethod
    def check_steps(context: Context) -> List[Error]:
        then_steps = get_then_steps(context.steps)

        lineno = context.scenario_node.lineno
        col_offset = context.scenario_node.col_offset

        if not then_steps:
            return [StepThenNotFound(lineno, col_offset)]

        if len(then_steps) > 1:
            return [StepThenDuplicated(lineno, col_offset)]
        return []
