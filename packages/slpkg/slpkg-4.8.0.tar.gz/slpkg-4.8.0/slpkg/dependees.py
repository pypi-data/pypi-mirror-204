#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import Generator
from slpkg.configs import Configs
from slpkg.views.ascii import Ascii
from slpkg.utilities import Utilities
from slpkg.repositories import Repositories


class Dependees(Configs):
    """ Show which packages depend. """

    def __init__(self, data: dict, packages: list, flags: list):
        __slots__ = 'data', 'packages', 'flags'
        super(Configs, self).__init__()
        self.data: dict = data
        self.packages: list = packages
        self.flags: list = flags

        self.ascii = Ascii()
        self.repos = Repositories()
        self.color = self.colour()
        self.utils = Utilities()

        self.llc: str = self.ascii.lower_left_corner
        self.hl: str = self.ascii.horizontal_line
        self.var: str = self.ascii.vertical_and_right
        self.bold: str = self.color['bold']
        self.violet: str = self.color['violet']
        self.cyan: str = self.color['cyan']
        self.grey: str = self.color['grey']
        self.yellow: str = self.color['yellow']
        self.byellow: str = f'{self.bold}{self.yellow}'
        self.endc: str = self.color['endc']

        self.option_for_full_reverse: bool = self.utils.is_option(
            ['-E', '--full-reverse'], self.flags)

        self.option_for_pkg_version: bool = self.utils.is_option(
            ['-p', '--pkg-version'], self.flags)

        self.option_for_binaries: bool = self.utils.is_option(
            ['-B', '--bin-repo='], self.flags)

    def find(self) -> None:
        """ Collecting the dependees. """
        print(f"The list below shows the "
              f"packages that dependees on '{', '.join([p for p in self.packages])}':\n")

        self.packages: list = self.utils.apply_package_pattern(self.data, self.packages)

        for pkg in self.packages:
            dependees: dict = dict(self.find_requires(pkg))

            package: str = f'{self.byellow}{pkg}{self.endc}'

            if self.option_for_pkg_version:
                if self.option_for_binaries:
                    version: str = self.data[pkg][0]
                else:
                    version: str = self.data[pkg][2]

                package: str = f'{self.byellow}{pkg} {version}{self.endc}'

            print(package)

            print(f' {self.llc}{self.hl}', end='')

            if not dependees:
                print(f'{self.cyan} No dependees{self.endc}')

            sp: str = ' ' * 4
            for i, (name, requires) in enumerate(dependees.items(), start=1):
                dependency: str = f'{self.cyan}{name}{self.endc}'

                if self.option_for_pkg_version:

                    if self.option_for_binaries:
                        version: str = self.data[name][0]
                    else:
                        version: str = self.data[name][2]

                    dependency: str = (f'{self.cyan}{name}{self.endc} {self.yellow}'
                                       f'{version}{self.endc}')

                if i == 1:
                    print(f' {dependency}')
                else:
                    print(f'{sp}{dependency}')

                if self.option_for_full_reverse:
                    if i == len(dependees):
                        print(' ' * 4 + f' {self.llc}{self.hl} {self.violet}{requires}{self.endc}')
                    else:
                        print(' ' * 4 + f' {self.var}{self.hl} {self.violet}{requires}{self.endc}')

            print(f'\n{self.grey}{len(dependees)} dependees for {pkg}{self.endc}\n')

    def find_requires(self, pkg: str) -> Generator:
        """ Find requires that package dependees. """
        if self.option_for_binaries:

            for name, data in self.data.items():
                if pkg in data[6].split():
                    yield name, data[6]

        else:
            for name, data in self.data.items():
                if pkg in data[7].split():
                    yield name, data[7]
