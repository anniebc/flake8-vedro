import ast

from flake8_plugin_utils import Visitor

from flake8_vedro.errors.common import (
    AssertSameObjectsForEquality,
    AssertWithConstant
)


class AssertVisitor(Visitor):

    def visit_Assert(self, node: ast.Assert):
        if isinstance(node.test, ast.Compare):

            left = node.test.left
            right = node.test.comparators[0]

            # assert 1 == 2
            if isinstance(left, ast.Constant) and isinstance(right, ast.Constant):

                if left.value == right.value:
                    self.error_from_node(AssertSameObjectsForEquality, node)

            # assert var == var
            elif isinstance(left, ast.Name) and isinstance(right, ast.Name):
                if left.id == right.id:
                    self.error_from_node(AssertSameObjectsForEquality, node)

            # assert var == 'string' or assert var == 1
            elif isinstance(right, ast.Constant):
                self.error_from_node(AssertWithConstant, node)
