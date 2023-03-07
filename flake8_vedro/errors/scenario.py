from flake8_plugin_utils import Error


class DecoratorVedroOnly(Error):
    code = 'VS1'
    message = 'decorator @vedro.only should not be presented'


class ScenarioNotInherited(Error):
    code = 'VS2'
    message = 'class Scenario should be inherited from class vedro.Scenario'


class ScenarioLocationInvalid(Error):
    code = 'VS3'
    message = 'scenario should be located in folder "scenarios/"'


# Subject errors

class SubjectNotFound(Error):
    code = 'VS4'
    message = 'class Scenario should have a subject'


class SubjectEmpty(Error):
    code = 'VS5'
    message = 'subject in class Scenario should not be empty'


class SubjectDuplicated(Error):
    code = 'VS6'
    message = 'class Scenario should have only one subject'


# Parametrization errors

class SubjectIsNotParametrized(Error):
    code = 'VS7'
    message = 'subject in parametrised scenario is not parametrised'


class FunctionCallInParams(Error):
    code = 'VS8'
    message = 'function call in parametrization, use lambda instead'


class ExceedMaxParamsCount(Error):
    code = 'VS9'
    message = 'exceeded max parameters in vedro.params: {current} > {max}'


# Step errors

class StepInvalidName(Error):
    code = 'VS300'
    message = 'step name should starts with "given_", "when_", "then_", "and_", "but_". ' \
              '"{step_name}" is given.'


class StepsWrongOrder(Error):
    code = 'VS301'
    message = 'steps order is wrong: step "{previous_step}" should not be before "{current_step}"'


class ImportedInterfaceInWrongStep(Error):
    code = 'VS302'
    message = 'interface should not be used in contexts (given) or asserts (then, and, but) steps - ' \
              '"{func_name}" is used.'


class StepWhenNotFound(Error):
    code = 'VS303'
    message = 'scenario should have "when" step'


class StepWhenDuplicated(Error):
    code = 'VS304'
    message = 'scenario should have only one "when" step'


# class StepWhenWithCondition(Error):
#     code = 'VS108'
#     message = 'step when "{step_name}" should have no conditions.'
#

class StepThenNotFound(Error):
    code = 'VS305'
    message = 'scenario should have "then" step'


class StepThenDuplicated(Error):
    code = 'VS306'
    message = 'scenario should have only one "then" step'


class StepAssertWithoutAssert(Error):
    code = 'VS307'
    message = 'step "{step_name}" does not have an assert'


# assert foo, assert True
class StepAssertHasUselessAssert(Error):
    code = 'VS308'
    message = 'step "{step_name}" has useless assert'


# foo == var
class StepAssertHasComparisonWithoutAssert(Error):
    code = 'VS309'
    message = 'step "{step_name}" has comparison without assert'


class StepHasAssert(Error):
    code = 'VS310'
    message = 'step "{step_name}" should not have assertion'


class MockHistoryIsNotSaved(Error):
    code = 'VS311'
    message = 'history of mock "{mock_name}" is not saved'
