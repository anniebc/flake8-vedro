import ast
from typing import Optional

from flake8_plugin_utils import Visitor

from flake8_vedro.checker.scenario import ScenarioCheckContext, ScenarioChecker
from flake8_vedro.confiig import Config

SCENARIOS_FOLDER = 'scenarios/'


class ScenarioVisitor(Visitor):
    def __init__(self, config: Optional[Config] = None, filename: Optional[str] = None) -> None:
        super(ScenarioVisitor, self).__init__(config=config)
        self.filename = filename

    def visit_ClassDef(self, node: ast.ClassDef):
        if node.name == 'Scenario':

            scenario_context = ScenarioChecker.check_scenario(
                node,
                context=ScenarioCheckContext(
                    report_error=self.error_from_node,
                    filename=self.filename,
                    scenarios_folder=SCENARIOS_FOLDER)
            )
            ScenarioChecker.check_context(node, scenario_context)
