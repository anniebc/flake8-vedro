from typing import List

from flake8_plugin_utils import Error

from flake8_vedro.errors.scenario import StepWhenDuplicated, StepWhenNotFound
from flake8_vedro.helpers.get_scenario_elements import get_when_steps
from flake8_vedro.visitors.scenario_visitor import (
    Context,
    ScenarioVisitor,
    StepsChecker
)


@ScenarioVisitor.register_steps_checker
class SingleWhenChecker(StepsChecker):

    @staticmethod
    def check_steps(context: Context) -> List[Error]:
        when_steps = get_when_steps(context.steps)

        lineno = context.scenario_node.lineno
        col_offset = context.scenario_node.col_offset

        if not when_steps:
            return [StepWhenNotFound(lineno, col_offset)]

        if len(when_steps) > 1:
            return [StepWhenDuplicated(lineno, col_offset)]
        return []
