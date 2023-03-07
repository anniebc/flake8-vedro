from flake8_plugin_utils import Error

# common errors

class SleepWithConstantArgument(Error):
    code = 'VDR001'
    message = 'using sleep with constant as argument is prohibited. Use sleep(var) instead'


class Print(Error):
    code = 'VDR002'
    message = 'try to avoid printing. If it\'s necessary ignore this warning'


# assert var == var
class AssertSameObjectsForEquality(Error):
    code = 'VDR003'
    message = 'comparing same objects in assert doesn\'t make any sense'


# assert var == 'string'
# assert var == 2
class AssertWithConstant(Error):
    code = 'VDR004'
    message = 'assert variable with constants is not allowed, move constant to libs'


class ArgAnnotationMissing(Error):
    code = 'VDR005'
    message = 'missing annotation for argument "{arg_name}" for function "{func_name}"'


class ReturnAnnotationMissing(Error):
    code = 'VDR006'
    message = 'missing return annotation for function "{func_name}"'


# scenario errors


class DecoratorVedroOnly(Error):
    code = 'VDR101'
    message = 'decorator @vedro.only should not be presented'


class ScenarioNotInherited(Error):
    code = 'VDR102'
    message = 'class Scenario should be inherited from class vedro.Scenario'


class ScenarioLocationInvalid(Error):
    code = 'VDR103'
    message = 'scenario should be located in folder "scenarios/"'


# Subject errors

class SubjectNotFound(Error):
    code = 'VDR104'
    message = 'class Scenario should have a subject'


class SubjectEmpty(Error):
    code = 'VDR105'
    message = 'subject in class Scenario should not be empty'


class SubjectDuplicated(Error):
    code = 'VDR106'
    message = 'class Scenario should have only one subject'


# Parametrization errors

class SubjectIsNotParametrized(Error):
    code = 'VDR107'
    message = 'subject in parametrised scenario is not parametrised'


class FunctionCallInParams(Error):
    code = 'VDR108'
    message = 'function call in parametrization, use lambda instead'


class ExceedMaxParamsCount(Error):
    code = 'VDR109'
    message = 'exceeded max parameters in vedro.params: {current} > {max}'


# Step errors

class StepInvalidName(Error):
    code = 'VDR300'
    message = 'step name should starts with "given_", "when_", "then_", "and_", "but_". ' \
              '"{step_name}" is given.'


class StepsWrongOrder(Error):
    code = 'VDR301'
    message = 'steps order is wrong: step "{previous_step}" should not be before "{current_step}"'


class ImportedInterfaceInWrongStep(Error):
    code = 'VDR302'
    message = 'interface should not be used in contexts (given) or asserts (then, and, but) steps - ' \
              '"{func_name}" is used.'


class StepWhenNotFound(Error):
    code = 'VDR303'
    message = 'scenario should have "when" step'


class StepWhenDuplicated(Error):
    code = 'VDR304'
    message = 'scenario should have only one "when" step'


# class StepWhenWithCondition(Error):
#     code = 'VDR108'
#     message = 'step when "{step_name}" should have no conditions.'
#

class StepThenNotFound(Error):
    code = 'VDR305'
    message = 'scenario should have "then" step'


class StepThenDuplicated(Error):
    code = 'VDR306'
    message = 'scenario should have only one "then" step'


class StepAssertWithoutAssert(Error):
    code = 'VDR307'
    message = 'step "{step_name}" does not have an assert'


# assert foo, assert True
class StepAssertHasUselessAssert(Error):
    code = 'VDR308'
    message = 'step "{step_name}" has useless assert'


# foo == var
class StepAssertHasComparisonWithoutAssert(Error):
    code = 'VDR309'
    message = 'step "{step_name}" has comparison without assert'


class StepHasAssert(Error):
    code = 'VDR310'
    message = 'step "{step_name}" should not have assertion'


class MockHistoryIsNotSaved(Error):
    code = 'VDR311'
    message = 'history of mock "{mock_name}" is not saved'
