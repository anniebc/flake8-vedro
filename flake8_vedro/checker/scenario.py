import ast
from typing import Callable

from flake8_vedro.errors.scenario import (
    DecoratorVedroOnly,
    ScenarioLocationInvalid,
    ScenarioNotInherited,
    SubjectDuplicated,
    SubjectEmpty,
    SubjectNotFound
)


class ScenarioCheckContext:
    def __init__(self, report_error: Callable,
                 filename: str,
                 scenarios_folder: str,
                 has_subject: bool = False):
        self.report_error = report_error
        self.filename = filename
        self.scenarios_folder = scenarios_folder
        self.has_subject = has_subject


class ScenarioChecker:

    @staticmethod
    def check_scenario_in_folder(node: ast.ClassDef, context: ScenarioCheckContext):
        if (
                context.filename is not None
                and context.scenarios_folder not in context.filename
        ):
            context.report_error(ScenarioLocationInvalid, node)

    @staticmethod
    def check_vedro_only_decorator(node: ast.ClassDef, context: ScenarioCheckContext):
        for decorator in node.decorator_list:
            if (
                    isinstance(decorator, ast.Attribute)
                    and decorator.value.id == 'vedro'
                    and decorator.attr == 'only'
            ):
                context.report_error(DecoratorVedroOnly, decorator)

    @staticmethod
    def check_correct_parent(node: ast.ClassDef, context: ScenarioCheckContext) -> bool:
        has_parent = False
        for base in node.bases:
            if isinstance(base, ast.Attribute):
                base: ast.Attribute
                if base.attr == 'Scenario' and base.value.id == 'vedro':
                    has_parent = True
        if not has_parent:
            context.report_error(ScenarioNotInherited, node)

    @staticmethod
    def check_subject(node: ast.ClassDef, context: ScenarioCheckContext) -> ScenarioCheckContext:
        for element in node.body:
            if (
                    isinstance(element, ast.Assign)
                    and element.targets[0].id == 'subject'
            ):
                if context.has_subject:
                    context.report_error(SubjectDuplicated, node)
                else:
                    context.has_subject = True
                    if isinstance(element.value, ast.Constant):
                        # проверяем subject на пустоту
                        if not element.value.value:
                            context.report_error(SubjectEmpty, element)
        return context

    @classmethod
    def check_scenario(cls, node: ast.ClassDef, context: ScenarioCheckContext) -> ScenarioCheckContext:
        cls.check_scenario_in_folder(node, context)
        cls.check_vedro_only_decorator(node, context)
        cls.check_correct_parent(node, context)
        context = cls.check_subject(node, context)
        return context

    @staticmethod
    def check_context(node: ast.ClassDef, context: ScenarioCheckContext):
        if not context.has_subject:
            context.report_error(SubjectNotFound, node)
