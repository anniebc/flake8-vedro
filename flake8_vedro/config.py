class Config:
    def __init__(self, max_params_count: int, skip_tests_init_annotation: bool):
        self.max_params_count = max_params_count
        self.skip_tests_init_annotation = skip_tests_init_annotation


class DefaultConfig(Config):
    def __init__(self,
                 max_params_count: int = 1,
                 skip_tests_init_annotation: bool = False):
        super().__init__(max_params_count, skip_tests_init_annotation)
