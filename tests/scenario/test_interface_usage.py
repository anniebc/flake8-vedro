from flake8_plugin_utils import assert_error, assert_not_error

from flake8_vedro.errors.scenario import ImportedInterfaceInWrongStep
from flake8_vedro.visitors import StepsVisitor


def test_interface_imported_from_submodule():
    code = """
    from interfaces.api import API
    class Scenario(vedro.Scenario):
        subject = 'string'
        def given(): API().get()
        def when(): pass
        def then(): assert foo == var
    """
    assert_error(StepsVisitor, code, ImportedInterfaceInWrongStep, func_name='API')


def test_interface_imported_from_module():
    code = """
    from interfaces import API

    class Scenario(vedro.Scenario):
        subject = 'string'
        def given(): API().get()
        def when(): pass
        def then(): assert foo == var
    """
    assert_error(StepsVisitor, code, ImportedInterfaceInWrongStep, func_name='API')


def test_interface_imported_from_module_no_init():
    code = """
    from interfaces import API

    class Scenario(vedro.Scenario):
        subject = 'string'
        def given(): API.get()
        def when(): pass
        def then(): assert foo == var
    """
    assert_error(StepsVisitor, code, ImportedInterfaceInWrongStep, func_name='API')


def test_interface_called_as_assign():
    code = """
    from interfaces import API

    class Scenario(vedro.Scenario):
        subject = 'string'
        def given(): response = API()
        def when(): pass
        def then(): assert foo == var
    """
    assert_error(StepsVisitor, code, ImportedInterfaceInWrongStep, func_name='API')


def test_interface_as_function():
    code = """
    from interfaces import get

    class Scenario(vedro.Scenario):
        subject = 'string'
        def given(): get()
        def when(): pass
        def then(): assert foo == var
    """
    assert_error(StepsVisitor, code, ImportedInterfaceInWrongStep, func_name='get')


def test_interface_method_in_when():
    code = """
    from interfaces.api import API
    from contexts import added

    class Scenario(vedro.Scenario):
        subject = 'string'
        def given(): added()
        def when(): API().get()
        def then(): assert foo == var
    """
    assert_not_error(StepsVisitor, code)


def test_interface_method_in_then():
    code = """
    from interfaces.api import API
    from contexts import added

    class Scenario(vedro.Scenario):
        subject = 'string'
        def given(): added()
        def when(): pass
        def then():
            assert foo == var
            API()
    """
    assert_error(StepsVisitor, code, ImportedInterfaceInWrongStep, func_name='API')


def test_interface_method_in_and():
    code = """
    from interfaces.api import API
    from contexts import added

    class Scenario(vedro.Scenario):
        subject = 'string'
        def given(): added()
        def when(): pass
        def then(): assert foo == var
        def and_():
            assert foo == var
            API()
    """
    assert_error(StepsVisitor, code, ImportedInterfaceInWrongStep, func_name='API')


def test_interface_method_in_but():
    code = """
    from interfaces.api import API
    from contexts import added

    class Scenario(vedro.Scenario):
        subject = 'string'
        def given(): added()
        def when(): pass
        def then(): assert foo == var
        def and_(): assert foo == var
        def but():
            assert foo == var
            API()
    """
    assert_error(StepsVisitor, code, ImportedInterfaceInWrongStep, func_name='API')


def test_call_self_method():
    code = """
    from interfaces.api import API
    from contexts import added

    class Scenario(vedro.Scenario):
        subject = 'string'
        def given(): self.photo = self.photo_method()
        def when(): pass
        def then(): assert foo == var
    """
    assert_not_error(StepsVisitor, code)
