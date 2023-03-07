import ast
from typing import List, Tuple

from flake8_plugin_utils import Error

from flake8_vedro.abstract_checkers import StepsChecker
from flake8_vedro.errors.scenario import ImportedInterfaceInWrongStep
from flake8_vedro.visitors.scenario_visitor import Context, ScenarioVisitor


@ScenarioVisitor.register_steps_checker
class InterfacesUsageChecker(StepsChecker):

    @staticmethod
    def _get_name_ast_name(element: ast.Name) -> str:
        return element.id

    def _unwrap_attribute(self, element: ast.Attribute or ast.Call or ast.Name) -> ast.Name:
        if isinstance(element, ast.Attribute):
            return self._unwrap_attribute(element.value)

        elif isinstance(element, ast.Call):
            return self._unwrap_attribute(element.func)

        elif isinstance(element, ast.Name):
            return element

        elif isinstance(element, ast.Subscript):
            return self._unwrap_attribute(element.value)

    def _get_callable_object_name(self, ast_call: ast.Call):
        func = ast_call.func
        if isinstance(func, ast.Name):  # типа foo = func()
            return self._get_name_ast_name(func)

        if isinstance(func, ast.Attribute) or isinstance(func, ast.Call):
            ast_name = self._unwrap_attribute(func)
            name = self._get_name_ast_name(ast_name)
            if name != 'self':  # foo = self.do()
                return name

    def _get_func_names_in_step(self, step: ast.FunctionDef or ast.AsyncFunctionDef) -> List[Tuple[str, int, int]]:
        """
        Return list of names and their positions (line and column offset) in file for functions,
        which are called in step from argument
        """
        functions_in_step: List[Tuple[str, int, int]] = []
        body = step.body
        for line in body:
            ast_call = None
            if isinstance(line, ast.Assign):  # foo = ...
                if isinstance(line.value, ast.Subscript):  # ... = func()[0]
                    if isinstance(line.value.value, ast.Call):
                        ast_call = line.value.value
                elif isinstance(line.value, ast.Call):  # ... = func()
                    ast_call = line.value

            elif isinstance(line, ast.Expr):
                if isinstance(line.value, ast.Call):  # func()
                    ast_call = line.value

                elif isinstance(line.value, ast.Await) and \
                        isinstance(line.value.value, ast.Call):
                    ast_call = line.value.value

            if ast_call:
                name = self._get_callable_object_name(ast_call)
                if name:
                    functions_in_step.append((
                        name,
                        line.lineno,
                        line.col_offset  # TODO fix
                    ))
        return functions_in_step

    def _get_imported_from_interfaces_functions(self, import_from_nodes: List[ast.ImportFrom]) -> List[ast.alias]:
        """
        Return list of function names which was imported from interfaces
        """
        function_names: List[ast.alias] = []
        for import_node in import_from_nodes:
            import_node: ast.ImportFrom
            if import_node.module == 'interfaces' or 'interfaces.' in import_node.module:
                for name in import_node.names:
                    function_names.append(name)
        return function_names

    def check_steps(self, context: Context) -> List[Error]:
        errors = []
        imported = self._get_imported_from_interfaces_functions(context.import_from_nodes)
        if not imported:
            return errors

        for step in context.steps:
            if (
                step.name.startswith('given')
                or step.name.startswith('then')
                or step.name.startswith('and')
                or step.name.startswith('but')
            ):
                for func, lineno, col_offset in self._get_func_names_in_step(step):
                    for func_name in imported:
                        if func == func_name.name or func == func_name.asname:
                            errors.append(ImportedInterfaceInWrongStep(
                                lineno=lineno, col_offset=col_offset, func_name=func))
        return errors
