import ast
from typing import List

from flake8_plugin_utils import Error

from flake8_vedro.abstract_checkers import StepsChecker
from flake8_vedro.errors import MockHistoryIsNotSaved
from flake8_vedro.visitors.scenario_visitor import Context, ScenarioVisitor


@ScenarioVisitor.register_steps_checker
class MockHistoryChecker(StepsChecker):

    def _check_saving_mock_history(self, body: List[ast.stmt]) -> List[Error]:
        errors = []
        for line in body:
            if isinstance(line, ast.With):
                # with mocked_1, mocked_2:
                for item in line.items:
                    if item.optional_vars is None:
                        if isinstance(item.context_expr, ast.Name):
                            errors.append(MockHistoryIsNotSaved(
                                line.lineno, line.col_offset, mock_name=item.context_expr.id))

                        # with self.mock_1:
                        elif isinstance(item.context_expr, ast.Attribute):
                            errors.append(MockHistoryIsNotSaved(
                                line.lineno, line.col_offset, mock_name=item.context_expr.attr))
                # with mocked_1:
                #   with mocked 2:
                errors.extend(self._check_saving_mock_history(line.body))
        return errors

    def check_steps(self, context: Context) -> List[Error]:
        errors = []
        for step in context.steps:
            errors.extend(self._check_saving_mock_history(step.body))
        return errors
