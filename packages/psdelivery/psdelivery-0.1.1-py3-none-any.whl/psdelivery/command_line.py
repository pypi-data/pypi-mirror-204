import collections
from typing import Dict, Callable
import json
import argparse
from argparse import RawTextHelpFormatter

from psdelivery import __version__
from psdelivery.controller import PsDelivery


class CommandLineAction:
    @staticmethod
    def show_version():
        print(__version__)

    @staticmethod
    def get_problem_list(topic: str, single_page: int | None, output: str):
        data: str | None = None

        if single_page is not None:
            data = json.dumps(
                PsDelivery(topic).get_list_by_single_page(
                    single_page, True),
                ensure_ascii=False,
                sort_keys=True,
                indent=4)

        if data is not None:
            with open(output, 'wt') as f:
                f.write(data)


class CommandLineUtility:
    root_parser: argparse.ArgumentParser
    child_parsers: Dict[str, argparse.ArgumentParser]
    actions: Dict[str, Callable]

    def _init_command_action(self):
        self.actions = {
            'version': CommandLineAction.show_version,
            'getlist': CommandLineAction.get_problem_list,
        }

    @staticmethod
    def _init_root_parser():
        parser = argparse.ArgumentParser(
            prog='psdelivery',
            formatter_class=RawTextHelpFormatter,
            description='PsDelivery is crawler for problem-solving website\n' +
                        'You can collect list or information of algorithm problem by using this')

        parser.add_argument(
            'args', choices=['version', 'getlist'],
            help='version: You can see version of this software\n' + \
                'getlist: You can get list of problems')
        
        return parser

    @staticmethod
    def _init_version_parser():
        parser = argparse.ArgumentParser(prog='psdelivery version')
        return parser
    
    @staticmethod
    def _init_getlist_parser():
        parser = argparse.ArgumentParser(prog='psdelivery getlist')
        parser.add_argument(
            '-t', '--topic', type=str,
            required=True)
        parser.add_argument(
            '-sp', '--single-page', type=int,
            required=False,
            default=1)
        parser.add_argument(
            '-o', '--output', type=str,
            required=True)
        return parser

    def __init__(self):
        self.child_parsers = collections.defaultdict(argparse.ArgumentParser)
        self.root_parser = self._init_root_parser()
        self.child_parsers['getlist'] = self._init_getlist_parser()
        self.child_parsers['version'] = self._init_version_parser()
        self._init_command_action()

    def _parse_root(self):
        root_args, child_args = self.root_parser.parse_known_args()
        root_arg, child_args = root_args.args, list(child_args)
        return root_arg, self.child_parsers[root_arg], child_args

    def run(self):
        root_arg, child_parser, child_args = self._parse_root()
        kwargs = child_parser.parse_args(child_args).__dict__
        self.actions[root_arg](**kwargs)
