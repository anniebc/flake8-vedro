from typing import List

from flake8_plugin_utils import Error

from flake8_vedro.errors.scenario import ScenarioLocationInvalid
from flake8_vedro.visitors.scenario_visitor import (
    Context,
    ScenarioChecker,
    ScenarioVisitor
)

SCENARIOS_FOLDER = 'scenarios/'


@ScenarioVisitor.register_scenario_checker
class LocationChecker(ScenarioChecker):

    def check_scenario(self, context: Context, *args) -> List[Error]:
        if (
                context.filename is not None
                and SCENARIOS_FOLDER not in context.filename
        ):
            return [ScenarioLocationInvalid(context.scenario_node.lineno, context.scenario_node.col_offset)]
        return []
