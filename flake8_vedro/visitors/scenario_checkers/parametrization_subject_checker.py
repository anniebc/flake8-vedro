import re
from typing import List

from flake8_plugin_utils import Error

from flake8_vedro.errors.scenario import SubjectIsNotParametrized
from flake8_vedro.helpers.get_scenario_elements import (
    get_init_step,
    get_params_decorators,
    get_subject
)
from flake8_vedro.visitors.scenario_visitor import (
    Context,
    ScenarioChecker,
    ScenarioVisitor
)


@ScenarioVisitor.register_scenario_checker
class ParametrizationSubjectChecker(ScenarioChecker):

    @staticmethod
    def check_scenario(context: Context, *args) -> List[Error]:
        init_node = get_init_step(context.scenario_node)

        if init_node and init_node.decorator_list:
            params_decorator = get_params_decorators(init_node)

            if len(params_decorator) > 1:
                subject_node = get_subject(context.scenario_node)
                pattern = re.compile('^.*\{.+\}.*$')  # noqa: W605
                if not pattern.match(subject_node.value.value):
                    return [SubjectIsNotParametrized(subject_node.lineno, subject_node.col_offset)]
        return []