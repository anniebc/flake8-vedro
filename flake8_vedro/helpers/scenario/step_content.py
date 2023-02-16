import ast
from typing import List, Tuple


def get_name_ast_name(element: ast.Name):
    return element.id


def unwrap_attribute(element: ast.Attribute or ast.Call or ast.Name) -> ast.Name:
    if isinstance(element, ast.Attribute):
        return unwrap_attribute(element.value)

    elif isinstance(element, ast.Call):
        return unwrap_attribute(element.func)

    elif isinstance(element, ast.Name):
        return element

    elif isinstance(element, ast.Subscript):
        return unwrap_attribute(element.value)
    print('None')


def get_callable_object_name(ast_call: ast.Call):
    func = ast_call.func
    if isinstance(func, ast.Name):  # типа foo = func()
        return get_name_ast_name(func)

    if isinstance(func, ast.Attribute) or isinstance(func, ast.Call):
        ast_name = unwrap_attribute(func)
        name = get_name_ast_name(ast_name)
        if name != 'self':  # foo = self.do()
            return name


def get_func_names_in_step(step: ast.FunctionDef or ast.AsyncFunctionDef) -> List[Tuple[str, int, int]]:
    """
    Return list of names and their positions (line and column offset) in file for functions,
    which are called in step from argument
    """
    functions_in_step: List[Tuple[str, int, int]] = []
    body = step.body
    for line in body:
        try:
            ast_call = None
            if isinstance(line, ast.Assign):  # foo = ...
                if isinstance(line.value, ast.Subscript):  # ... = func()[0]
                    if isinstance(line.value.value, ast.Call):
                        ast_call = line.value.value
                elif isinstance(line.value, ast.Call):    # ... = func()
                    ast_call = line.value

            elif isinstance(line, ast.Expr):
                if isinstance(line.value, ast.Call):    # func()
                    ast_call = line.value

                elif isinstance(line.value, ast.Await) and \
                        isinstance(line.value.value, ast.Call):
                    ast_call = line.value.value

            if ast_call:
                name = get_callable_object_name(ast_call)
                if name:
                    functions_in_step.append((
                        name,
                        line.lineno,
                        line.col_offset  # TODO fix
                    ))
        except:
            print(f'Exception during validation {step.name} on line {line.lineno}')
    return functions_in_step
