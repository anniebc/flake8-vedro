import ast
from typing import List, Optional


def get_init_step(node: ast.ClassDef) -> Optional[ast.FunctionDef or ast.AsyncFunctionDef]:
    for element in node.body:
        if (isinstance(element, ast.FunctionDef) or isinstance(element, ast.AsyncFunctionDef)) \
                and element.name == '__init__':
            return element


def get_subject(node: ast.ClassDef) -> Optional[ast.Assign]:
    for element in node.body:
        if isinstance(element, ast.Assign) and element.targets[0].id == 'subject':
            return element


def get_params_decorators(init_node: ast.FunctionDef or ast.AsyncFunctionDef) -> List[ast.Call]:
    params_decorator = []
    for decorator in init_node.decorator_list:
        if isinstance(decorator, ast.Call):

            # @vedro.params
            if (
                    isinstance(decorator.func, ast.Attribute)
                    and decorator.func.value.id == 'vedro'
                    and decorator.func.attr == 'params'
            ):
                params_decorator.append(decorator)

            # @params
            elif isinstance(decorator.func, ast.Name) and decorator.func.id == 'params':
                params_decorator.append(decorator)
    return params_decorator


def get_imported_from_interfaces_functions(imports_node: List[ast.ImportFrom]) -> List[ast.alias]:
    """
    Return list of function names which was imported from interfaces
    """
    function_names: List[ast.alias] = []
    for import_node in imports_node:
        import_node: ast.ImportFrom
        if import_node.module == 'interfaces' or 'interfaces.' in import_node.module:
            for name in import_node.names:
                function_names.append(name)
    return function_names
