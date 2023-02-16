import ast
from typing import List, Tuple


def get_func_names_in_step(step: ast.FunctionDef or ast.AsyncFunctionDef) -> List[Tuple[str, int, int]]:
    """
    Return list of names and their positions (line and column offset) in file for functions,
    which are called in step from argument
    """
    functions_in_step: List[Tuple[str, int, int]] = []
    body = step.body
    for line in body:
        if isinstance(line, ast.Assign) and isinstance(line.value, ast.Call):
            if isinstance(line.value.func, ast.Name):   # типа foo = func()
                functions_in_step.append((line.value.func.id, line.lineno, line.value.col_offset))
            if (
                    isinstance(line.value.func, ast.Attribute)
                    and line.value.func.value.id == 'self'
            ):  # типа foo = self.func()
                pass

        elif isinstance(line, ast.Expr) and isinstance(line.value, ast.Call):
            func = line.value.func

            if isinstance(func, ast.Name):
                functions_in_step.append((func.id, line.lineno, func.col_offset))  # типа func()

            elif isinstance(func, ast.Attribute):

                if isinstance(func.value, ast.Call):  # типа Foo().func()
                    if isinstance(func.value.func, ast.Name):
                        functions_in_step.append((func.value.func.id, line.lineno, func.value.col_offset))

                elif isinstance(func.value, ast.Name):  # типа Foo.func()
                    functions_in_step.append((func.value.id, line.lineno, func.value.col_offset))
    return functions_in_step
