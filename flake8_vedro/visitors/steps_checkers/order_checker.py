from typing import List, Optional

from flake8_plugin_utils import Error

from flake8_vedro.abstract_checkers import StepsChecker
from flake8_vedro.errors.scenario import StepsWrongOrder
from flake8_vedro.visitors.scenario_visitor import Context, ScenarioVisitor


@ScenarioVisitor.register_steps_checker
class OrderChecker(StepsChecker):

    @staticmethod
    def _get_step_order_by_name(name: str) -> Optional[int]:
        if name == '__init__' or name is None:
            return 0
        elif name.startswith('given'):
            return 1
        elif name.startswith('when'):
            return 2
        elif name.startswith('then'):
            return 3
        elif name.startswith('and') or name.startswith('but'):
            return 4

    def check_steps(self, context: Context) -> List[Error]:
        errors = []
        previous_name = None
        for step in context.steps:
            previous_order = self._get_step_order_by_name(previous_name)
            if previous_order is not None:
                if self._get_step_order_by_name(step.name) < previous_order:
                    errors.append(StepsWrongOrder(step.lineno, step.col_offset,
                                                  previous_step=previous_name,
                                                  current_step=step.name))
            previous_name = step.name
        return errors
