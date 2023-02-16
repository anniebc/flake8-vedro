import ast
from typing import Callable, List, Optional

from flake8_vedro.errors.scenario import (
    ImportedInterfaceInWrongStep,
    MockHistoryIsNotSaved,
    StepAssertHasComparisonWithoutAssert,
    StepAssertHasUselessAssert,
    StepAssertWithoutAssert,
    StepHasAssert,
    StepInvalidName,
    StepsWrongOrder,
    StepThenDuplicated,
    StepThenNotFound,
    StepWhenDuplicated,
    StepWhenNotFound
)
from flake8_vedro.helpers.scenario.imports import (
    get_imported_from_interfaces_functions
)
from flake8_vedro.helpers.scenario.step_content import get_func_names_in_step


class StepCheckContext:
    def __init__(self, report_error: Callable, imports_node: List[ast.ImportFrom]):
        self.report_error = report_error
        self.imported_from_interface = get_imported_from_interfaces_functions(imports_node)
        self.previous_step_name = None
        self.has_when_step = False
        self.has_then_step = False


class CommonStepChecker:

    @staticmethod
    def check_no_interfaces_call_in_step(step: ast.FunctionDef or ast.AsyncFunctionDef,
                                         context: StepCheckContext) -> None:
        for func, lineno, col_offset in get_func_names_in_step(step):
            for func_name in context.imported_from_interface:
                if func == func_name.name or func == func_name.asname:
                    context.report_error(ImportedInterfaceInWrongStep, step,
                                         lineno=lineno,
                                         col_offset=col_offset,
                                         func_name=func)

    @classmethod
    def check_saving_mock_history(cls, body: List[ast.stmt], context: StepCheckContext):
        for line in body:
            if isinstance(line, ast.With):
                # with mocked_1, mocked_2:
                for item in line.items:
                    if item.optional_vars is None:
                        if isinstance(item.context_expr, ast.Name):
                            context.report_error(MockHistoryIsNotSaved, line,
                                                 mock_name=item.context_expr.id)
                        # with self.mock_1:
                        elif isinstance(item.context_expr, ast.Attribute):
                            context.report_error(MockHistoryIsNotSaved, line,
                                                 mock_name=item.context_expr.attr)
                # with mocked_1:
                #   with mocked 2:
                cls.check_saving_mock_history(line.body, context)

    @staticmethod
    def check_step_order(step: ast.FunctionDef or ast.AsyncFunctionDef,
                         context: StepCheckContext) -> None:

        def get_step_order_by_name(name: str) -> Optional[int]:
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

        previous_order = get_step_order_by_name(context.previous_step_name)
        if previous_order is not None:
            if get_step_order_by_name(step.name) < previous_order:
                context.report_error(StepsWrongOrder,
                                     step,
                                     previous_step=context.previous_step_name,
                                     current_step=step.name)

    @staticmethod
    def check_no_assert_in_step(step: ast.FunctionDef or ast.AsyncFunctionDef,
                                context: StepCheckContext):
        for line in step.body:
            if isinstance(line, ast.Assert):
                context.report_error(StepHasAssert, line, step_name=step.name)


class StepChecker(CommonStepChecker):

    @classmethod
    def _step_given_proceed(cls, step: ast.FunctionDef or ast.AsyncFunctionDef,
                            context: StepCheckContext) -> None:
        cls.check_step_order(step, context)
        cls.check_no_interfaces_call_in_step(step, context)
        cls.check_no_assert_in_step(step, context)

    @classmethod
    def _step_when_proceed(cls, step: ast.FunctionDef or ast.AsyncFunctionDef,
                           context: StepCheckContext) -> StepCheckContext:
        cls.check_step_order(step, context)
        cls.check_no_assert_in_step(step, context)
        if context.has_when_step:
            context.report_error(StepWhenDuplicated, step)
        context.has_when_step = True
        return context

    @classmethod
    def _step_assert_proceed(cls, step: ast.FunctionDef or ast.AsyncFunctionDef,
                             context: StepCheckContext) -> None:
        cls.check_step_order(step, context)
        cls.check_no_interfaces_call_in_step(step, context)

        has_assert = False
        for line in step.body:
            if isinstance(line, ast.Assert):
                has_assert = True

                if isinstance(line.test, ast.Constant) or isinstance(line.test, ast.Name):
                    context.report_error(StepAssertHasUselessAssert, line, step_name=step.name)

            if isinstance(line, ast.Expr):
                if isinstance(line.value, ast.Compare):
                    context.report_error(StepAssertHasComparisonWithoutAssert, line, step_name=step.name)
        if not has_assert:
            context.report_error(StepAssertWithoutAssert, step, step_name=step.name)

    @classmethod
    def _step_then_proceed(cls, step: ast.FunctionDef or ast.AsyncFunctionDef,
                           context: StepCheckContext) -> StepCheckContext:
        if context.has_then_step:
            context.report_error(StepThenDuplicated, step)
        context.has_then_step = True
        cls._step_assert_proceed(step, context)
        return context

    @classmethod
    def _step_init_proceed(cls, step: ast.FunctionDef or ast.AsyncFunctionDef,
                           context: StepCheckContext) -> None:
        cls.check_no_assert_in_step(step, context)

    @staticmethod
    def _step_unknown_proceed(step: ast.FunctionDef or ast.AsyncFunctionDef,
                              context: StepCheckContext) -> None:
        """
        Proceed unknown step, report error.
        """
        context.report_error(StepInvalidName, step, step_name=step.name)

    @classmethod
    def check_step(cls, step: ast.FunctionDef or ast.AsyncFunctionDef,
                   context: StepCheckContext) -> StepCheckContext:
        cls.check_saving_mock_history(step.body, context)

        if step.name.startswith('given'):
            cls._step_given_proceed(step, context)

        elif step.name.startswith('when'):
            context = cls._step_when_proceed(step, context)

        elif step.name.startswith('then'):
            context = cls._step_then_proceed(step, context)

        elif step.name.startswith('and') or step.name.startswith('but'):
            cls._step_assert_proceed(step, context)

        elif step.name == '__init__':
            cls._step_init_proceed(step, context)

        else:
            cls._step_unknown_proceed(step, context)

        context.previous_step_name = step.name
        return context

    @staticmethod
    def check_context(node: ast.ClassDef, context: StepCheckContext):
        if not context.has_when_step:
            context.report_error(StepWhenNotFound, node)
        if not context.has_then_step:
            context.report_error(StepThenNotFound, node)
