import ast

from flake8_plugin_utils import Visitor

from flake8_vedro.errors.common import Print, SleepWithConstantArgument


class FunctionVisitor(Visitor):

    def check_sleep(self, node: ast.FunctionDef or ast.AsyncFunctionDef):
        for line in node.body:
            if isinstance(line, ast.Expr) and isinstance(line.value, ast.Call):
                self.visit_Call(line.value)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.check_sleep(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.check_sleep(node)

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            if node.func.id == 'sleep':
                if isinstance(node.args[0], ast.Constant):
                    self.error_from_node(SleepWithConstantArgument, node)

            if node.func.id == 'print' or node.func.id == 'pp':
                self.error_from_node(Print, node)