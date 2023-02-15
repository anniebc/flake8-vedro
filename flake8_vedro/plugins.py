import argparse
import ast
from typing import Callable, List, Optional

from flake8.options.manager import OptionManager
from flake8_plugin_utils import Plugin, Visitor

from flake8_vedro.visitors import (
    CommonVisitor,
    ParametrizationVisitor,
    ScenarioVisitor,
    StepsVisitor
)

from .confiig import Config
from .defaults import Defaults


class CommonStylePlugin(Plugin):
    name = 'flake8_vedro_common_style'
    version = '0.0.1'
    visitors = [
        CommonVisitor,
    ]


class VedroScenarioStylePlugin(Plugin):
    name = 'flake8_vedro'
    version = '0.1.0'
    visitors = [
        ScenarioVisitor,
        StepsVisitor,
        ParametrizationVisitor
    ]

    def __init__(self, tree: ast.AST, filename: str,  *args, **kwargs):
        super(VedroScenarioStylePlugin, self).__init__(tree)
        self.filename = filename

    def run(self):
        for visitor_cls in self.visitors:
            visitor = self._create_visitor(visitor_cls, filename=self.filename)
            visitor.visit(self._tree)
            for error in visitor.errors:
                yield self._error(error)

    @classmethod
    def _create_visitor(cls, visitor_cls: Callable, filename: Optional[str] = None) -> Visitor:
        if cls.config is None:
            return visitor_cls(filename=filename)
        return visitor_cls(config=cls.config, filename=filename)

    @classmethod
    def add_options(cls, option_manager: OptionManager):
        option_manager.add_option(
            '--scenario-params-max-count',
            default=Defaults.MAX_PARAMS_COUNT,
            type=int,
            parse_from_config=True,
            help='Maximum allowed parameters in vedro parametrized scenario. '
                 '(Default: %(default)s)',
        )

    @classmethod
    def parse_options_to_config(
        cls, option_manager: OptionManager, options: argparse.Namespace, args: List[str]
    ) -> Config:
        return Config(
            max_params_count=options.scenario_params_max_count
        )
