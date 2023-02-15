import ast
from typing import List


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
