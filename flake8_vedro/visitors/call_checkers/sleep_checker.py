import ast
from typing import List

from flake8_plugin_utils import Error

from flake8_vedro.errors.common import SleepWithConstantArgument
from flake8_vedro.visitors.function_call_visitor import (
    Checker,
    FunctionCallVisitor
)


@FunctionCallVisitor.register_checker
class SleepChecker(Checker):

    def check(self, call_node: ast.Call) -> List[Error]:
        if isinstance(call_node.func, ast.Name):
            if call_node.func.id == 'sleep':
                if isinstance(call_node.args[0], ast.Constant):
                    return [SleepWithConstantArgument(call_node.lineno, call_node.col_offset)]
        return []
