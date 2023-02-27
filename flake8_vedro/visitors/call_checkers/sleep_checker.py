import ast
from typing import List

from flake8_plugin_utils import Error

from flake8_vedro.errors import SleepWithConstantArgument
from flake8_vedro.visitors.function_call_visitor import (
    Checker,
    Context,
    FunctionCallVisitor
)


@FunctionCallVisitor.register_checker
class SleepChecker(Checker):

    def check(self, call_node: ast.Call, context: Context) -> List[Error]:
        if (
            context.sleep_function_name
            and isinstance(call_node.func, ast.Name)
            and call_node.func.id == context.sleep_function_name
            and isinstance(call_node.args[0], ast.Constant)
        ):
            return [SleepWithConstantArgument(call_node.lineno, call_node.col_offset)]

        if (
            context.is_imported_module_time
            and isinstance(call_node.func, ast.Attribute)
            and isinstance(call_node.args[0], ast.Constant)
            and call_node.func.attr == 'sleep'
            and call_node.func.value.id == 'time'
        ):
            return [SleepWithConstantArgument(call_node.lineno, call_node.col_offset)]
        return []
