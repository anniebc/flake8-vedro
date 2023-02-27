import ast
from typing import List

from flake8_plugin_utils import Error

from flake8_vedro.errors.scenario import (
    SubjectDuplicated,
    SubjectEmpty,
    SubjectNotFound
)
from flake8_vedro.helpers.get_scenario_elements import (
    get_subject,
    get_subjects
)
from flake8_vedro.visitors.scenario_visitor import (
    Context,
    ScenarioChecker,
    ScenarioVisitor
)


@ScenarioVisitor.register_scenario_checker
class SingleSubjectChecker(ScenarioChecker):

    def check_scenario(self, context: Context, *args) -> List[Error]:
        subjects = get_subjects(context.scenario_node)

        if not subjects:
            return [SubjectNotFound(context.scenario_node.lineno, context.scenario_node.col_offset)]

        errors = []
        if len(subjects) > 1:
            for subject in subjects[1:]:
                errors.append(SubjectDuplicated(subject.lineno, subject.col_offset))

        return errors


@ScenarioVisitor.register_scenario_checker
class SubjectEmptyChecker(ScenarioChecker):

    def check_scenario(self, context: Context, *args) -> List[Error]:
        subject = get_subject(context.scenario_node)
        if isinstance(subject.value, ast.Constant):
            if not subject.value.value:
                return [SubjectEmpty(subject.lineno, subject.col_offset)]
        return []
