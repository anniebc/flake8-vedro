import ast
from typing import List

from flake8_plugin_utils import Error

from flake8_vedro.errors.scenario import StepAssertWithoutAssert
from flake8_vedro.visitors.scenario_visitor import (
    Context,
    ScenarioVisitor,
    StepsChecker
)


@ScenarioVisitor.register_steps_checker
class AssertChecker(StepsChecker):

    @staticmethod
    def check_steps(context: Context) -> List[Error]:
        errors = []
        for step in context.steps:
            if (
                step.name.startswith('then')
                or step.name.startswith('and')
                or step.name.startswith('but')
            ):
                has_assert = False
                for line in step.body:
                    if isinstance(line, ast.Assert):
                        has_assert = True
                if not has_assert:
                    errors.append(StepAssertWithoutAssert(step.lineno, step.col_offset, step_name=step.name))
        return errors
