from interfaces import API


class Scenario(vedro.Scenario):
    subject = 'string'

    def given(self):
        API.get()
        expected_provider_blocks = schema.array.contains_all([
            StatisticProviderWithAlbumsSchema,
            StatisticProviderWithAlbumsSchema
        ]).length(2)
        API().get()
        await API.get()

    def when(self): pass
    def then(self): assert foo == var
