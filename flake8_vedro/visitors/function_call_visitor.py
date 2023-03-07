import ast
from abc import ABC, abstractmethod
from typing import List, Type

from flake8_vedro.visitors._visitor_with_filename import VisitorWithFilename


class Checker(ABC):
    @abstractmethod
    def check(self, call_node): pass


class FunctionCallVisitor(VisitorWithFilename):
    checkers: List[Checker] = []

    @classmethod
    def register_checker(cls, checker: Type[Checker]):
        cls.checkers.append(checker())
        return checker

    @classmethod
    def deregister_all(cls):
        cls.checkers = []

    def visit_Call(self, node: ast.Call):
        try:
            for checker in self.checkers:
                self.errors.extend(checker.check(node))
        except Exception as e:
            print(f'Linter failed: checking {self.filename} with {checker.__class__}.\n'
                  f'Exception: {e}')
