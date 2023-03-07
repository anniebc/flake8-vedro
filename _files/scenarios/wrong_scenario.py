from time import sleep

from interfaces import API


@vedro.only
class Scenario(vedro.Scenario):
    subject = 'string'

    def given(self):
        API.get()
        sleep(1)
        pp('asdsd')
        API().get()
        assert True


    def when(self): pass
    def then(self): assert foo == var
