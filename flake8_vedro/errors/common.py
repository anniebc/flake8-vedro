from flake8_plugin_utils import Error

# --- Common errors (in scenarios, helpers etc). Error pattern: S0**


class SleepWithConstantArgument(Error):
    code = 'CS1'
    message = 'using sleep with constant as argument is prohibited. Use sleep(var) instead'


class Print(Error):
    code = 'CS2'
    message = 'try to avoid printing. If it\'s necessary ignore this warning'


# assert var == var
class AssertSameObjectsForEquality(Error):
    code = 'CS3'
    message = 'comparing same objects in assert doesn\'t make any sense'


# assert var == 'string'
# assert var == 2
class AssertWithConstant(Error):
    code = 'CS4'
    message = 'assert variable with constants is not allowed, move constant to libs'


class ArgAnnotationMissing(Error):
    code = 'CS5'
    message = 'missing annotation for argument "{arg_name}" for function "{func_name}"'


class ReturnAnnotationMissing(Error):
    code = 'CS6'
    message = 'missing return annotation for function "{func_name}"'
