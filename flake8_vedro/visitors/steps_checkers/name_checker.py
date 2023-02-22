from typing import List

from flake8_plugin_utils import Error

from flake8_vedro.errors.scenario import StepInvalidName
from flake8_vedro.visitors.scenario_visitor import (
    Context,
    ScenarioVisitor,
    StepsChecker
)


@ScenarioVisitor.register_steps_checker
class NameChecker(StepsChecker):

    @staticmethod
    def check_steps(context: Context) -> List[Error]:
        errors = []
        for step in context.steps:
            if not (
                    step.name.startswith('given')
                    or step.name.startswith('when')
                    or step.name.startswith('then')
                    or step.name.startswith('and')
                    or step.name.startswith('but')
                    or step.name == '__init__'
            ):
                errors.append(StepInvalidName(step.lineno, step.col_offset, step_name=step.name))
        return errors
