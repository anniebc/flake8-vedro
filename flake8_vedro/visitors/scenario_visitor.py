from abc import ABC, abstractmethod
import ast
from typing import List, Optional

from flake8_plugin_utils import Error, Visitor

from flake8_vedro.confiig import Config
from flake8_vedro.helpers.get_scenario_elements import get_all_steps


class Context:
    def __init__(self, steps, scenario_node, import_from_nodes, filename):
        self.steps = steps
        self.scenario_node = scenario_node
        self.import_from_nodes = import_from_nodes
        self.filename = filename


class ScenarioChecker(ABC):

    @abstractmethod
    def check_scenario(self, context, config) -> List[Error]:
        pass


class StepsChecker(ABC):

    @abstractmethod
    def check_steps(self, context) -> List[Error]:
        pass


class ScenarioVisitor(Visitor):
    scenarios_checkers: List[ScenarioChecker] = []
    steps_checkers: List[StepsChecker] = []
    import_from_nodes: List[ast.ImportFrom] = []

    def __init__(self, config: Optional[Config] = None,
                 filename: Optional[str] = None) -> None:
        super(ScenarioVisitor, self).__init__(config=config)
        self.filename = filename
        self.import_from_nodes = []

    @property
    def config(self):
        return self._config

    @classmethod
    def register_steps_checker(cls, checker: StepsChecker):
        cls.steps_checkers.append(checker())
        return checker

    @classmethod
    def register_scenario_checker(cls, checker: ScenarioChecker):
        cls.scenarios_checkers.append(checker())
        return checker

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """
        Save all imports from scenario (for validation ImportedInterfaceInWrongStep)
        """
        self.import_from_nodes.append(node)

    @classmethod
    def deregister_all(cls):
        cls.steps_checkers = []
        cls.scenarios_checkers = []

    def visit_ClassDef(self, node: ast.ClassDef):
        if node.name == 'Scenario':
            context = Context(steps=get_all_steps(node),
                              scenario_node=node,
                              import_from_nodes=self.import_from_nodes,
                              filename=self.filename)

            for checker in self.steps_checkers:
                self.errors.extend(checker.check_steps(context))

            for checker in self.scenarios_checkers:
                self.errors.extend(checker.check_scenario(context, self.config))
