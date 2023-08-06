#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.repositories import Repositories
from slpkg.binaries.queries import BinQueries


class SearchPackage(Configs):
    """ Search packages from the repositories. """

    def __init__(self, flags=None):
        __slots__ = 'flags'
        super(Configs, self).__init__()
        self.flags: list = flags

        self.color = self.colour()
        self.utils = Utilities()
        self.repos = Repositories()

        self.yellow: str = self.color['yellow']
        self.cyan: str = self.color['cyan']
        self.green: str = self.color['green']
        self.grey: str = self.color['grey']
        self.endc: str = self.color['endc']

        self.option_for_binaries: bool = self.utils.is_option(
            ['-B', '--bin-repo='], self.flags)

    def package(self, data: dict, packages: list, repo: str) -> None:
        """ Searching and print the matched packages. """
        print(f'The list below shows the repo '
              f'packages that contains \'{", ".join([p for p in packages])}\':\n')

        matching: int = 0

        # Searching for binaries.
        if self.option_for_binaries:

            if repo == '*':
                data: dict = BinQueries('').repositories_data()
                for package in packages:
                    for data_pkg in data.values():

                        if package in data_pkg[0] or package == '*':
                            matching += 1

                            print(f'{data_pkg[12]}: {self.cyan}{data_pkg[0]}{self.endc} '
                                  f'{self.yellow}{data_pkg[1]}{self.endc} {self.green}{data_pkg[10]}{self.endc}')

            else:
                for package in packages:
                    for name, data_pkg in data.items():

                        if package in name or package == '*':
                            matching += 1

                            print(f'{data_pkg[11]}: {self.cyan}{name}{self.endc} {self.yellow}{data_pkg[0]}{self.endc}'
                                  f'{self.green}{data_pkg[9]}{self.endc}')

        else:
            # Searching for slackbuilds.
            names: list = list(data.keys())
            for package in packages:
                for name in names:

                    if package in name or package == '*':
                        matching += 1

                        version: str = data[name][2]
                        desc: str = data[name][8].replace(name, '')

                        print(f'{self.cyan}{name}{self.endc} {self.yellow}{version}{self.endc}'
                              f'{self.green}{desc}{self.endc}')

        if not matching:
            print('\nDoes not match any package.\n')
        else:
            print(f'\n{self.grey}Total found {matching} packages.{self.endc}')
