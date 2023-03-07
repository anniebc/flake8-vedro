import ast
from abc import ABC, abstractmethod
from typing import List, Type

from flake8_plugin_utils import Visitor


class Checker(ABC):
    @abstractmethod
    def check(self, call_node): pass


class FunctionCallVisitor(Visitor):
    checkers: List[Checker] = []

    @classmethod
    def register_checker(cls, checker: Type[Checker]):
        cls.checkers.append(checker())
        return checker

    @classmethod
    def deregister_all(cls):
        cls.checkers = []

    def visit_Call(self, node: ast.Call):
        for checker in self.checkers:
            self.errors.extend(checker.check(node))
