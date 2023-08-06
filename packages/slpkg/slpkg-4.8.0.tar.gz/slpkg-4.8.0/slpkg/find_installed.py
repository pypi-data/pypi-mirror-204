#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.configs import Configs
from slpkg.utilities import Utilities


class FindInstalled(Configs):
    """ Find installed packages. """

    def __init__(self):
        super(Configs, self).__init__()

        self.color = self.colour()
        self.utils = Utilities()

        self.matching: list = []
        self.yellow: str = self.color['yellow']
        self.cyan: str = self.color['cyan']
        self.green: str = self.color['green']
        self.blue: str = self.color['blue']
        self.endc: str = self.color['endc']
        self.grey: str = self.color['grey']

    def find(self, packages: list) -> None:
        """ Find the packages. """
        print(f'The list below shows the installed packages '
              f'that contains \'{", ".join([p for p in packages])}\' files:\n')

        for pkg in packages:
            for package in self.utils.installed_packages.values():
                if pkg in package or pkg == '*':
                    self.matching.append(package)

        self.matched()

    def matched(self) -> None:
        """ Print the matched packages. """
        if self.matching:
            for package in self.matching:
                print(f'{self.cyan}{package}{self.endc}')
            print(f'\n{self.grey}Total found {len(self.matching)} packages.{self.endc}')
        else:
            print('\nDoes not match any package.\n')
