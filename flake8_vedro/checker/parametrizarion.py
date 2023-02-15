import ast
import re
from typing import Callable

from flake8_vedro.errors.scenario import (
    ExceedMaxParamsCount,
    FunctionCallInParams,
    SubjectIsNotParametrized
)
from flake8_vedro.helpers.scenario.get_elements import (
    get_init_step,
    get_params_decorators,
    get_subject
)


class ParametrizationContext:
    def __init__(self, report_error: Callable, max_params_count: int):
        self.report_error = report_error
        self.max_params_count = max_params_count


class ParametrizationChecker:

    @staticmethod
    def _check_subject_parametrization(node: ast.ClassDef, context: ParametrizationContext):
        subject_node = get_subject(node)
        pattern = re.compile('^.*\{.+\}.*$')  # noqa: W605
        if not pattern.match(subject_node.value.value):
            context.report_error(SubjectIsNotParametrized, subject_node)

    @staticmethod
    def _check_params_limit(decorator: ast.Call, context: ParametrizationContext):
        if len(decorator.args) > context.max_params_count:
            context.report_error(ExceedMaxParamsCount, decorator,
                                 current=len(decorator.args),
                                 max=context.max_params_count)

    @staticmethod
    def _check_func_call_in_params(decorator: ast.Call, context: ParametrizationContext):
        for arg in decorator.args:
            if isinstance(arg, ast.Call):
                context.report_error(FunctionCallInParams, decorator)

    @classmethod
    def check(cls, node: ast.ClassDef, context: ParametrizationContext):
        init_node = get_init_step(node)
        if init_node and init_node.decorator_list:
            params_decorator = get_params_decorators(init_node)

            if len(params_decorator) > 1:
                cls._check_subject_parametrization(node, context)

            for decorator in init_node.decorator_list:
                cls._check_func_call_in_params(decorator, context)
                cls._check_params_limit(decorator, context)
