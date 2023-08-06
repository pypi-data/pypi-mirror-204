#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.configs import Configs
from slpkg.views.ascii import Ascii
from slpkg.utilities import Utilities


class Tracking(Configs):
    """ Tracking of the package dependencies. """

    def __init__(self, flags: list):
        __slots__ = 'flags'
        super(Configs, self).__init__()
        self.flags: list = flags

        self.ascii = Ascii()
        self.color = self.colour()
        self.utils = Utilities()

        self.llc: str = self.ascii.lower_left_corner
        self.hl: str = self.ascii.horizontal_line
        self.vl: str = self.ascii.vertical_line
        self.cyan: str = self.color['cyan']
        self.grey: str = self.color['grey']
        self.yellow: str = self.color['yellow']
        self.endc: str = self.color['endc']

        self.option_for_pkg_version: bool = self.utils.is_option(
            ['-p', '--pkg-version'], self.flags)

        self.option_for_binaries: bool = self.utils.is_option(
            ['-B', '--bin-repo='], self.flags)

    def packages(self, data: dict, packages: list) -> None:
        """ Prints the packages dependencies. """
        print(f"The list below shows the packages '{', '.join([p for p in packages])}' with dependencies:\n")

        packages: list = self.utils.apply_package_pattern(data, packages)

        char: str = f' {self.llc}{self.hl}'
        sp: str = ' ' * 4

        for package in packages:
            how_many: int = 0
            pkg = f'{self.yellow}{package}{self.endc}'

            if self.option_for_pkg_version:

                if self.option_for_binaries:
                    version: str = data[package][0]
                else:
                    version: str = data[package][2]

                pkg = f'{self.yellow}{package} {version}{self.endc}'

            if self.option_for_binaries:
                requires: list = data[package][6].split()
            else:
                requires: list = data[package][7].split()

            print(pkg)
            print(char, end='')

            if not requires:
                print(f' {self.cyan}No dependencies{self.endc}')
            else:
                for i, req in enumerate(requires, start=1):

                    how_many += 1

                    require: str = f'{self.cyan}{req}{self.endc}'

                    if self.option_for_pkg_version:

                        if self.option_for_binaries:
                            version: str = ' (not included)'
                            if data.get(req):
                                version: str = f' {self.yellow}{data[req][0]}{self.endc}'
                        else:
                            version: str = f' {self.yellow}{data[req][2]}{self.endc}'

                        require: str = f'{self.cyan}{req}{self.endc}{version}'

                    if i == 1:
                        print(f' {require}')
                    else:
                        print(f'{sp}{require}')

            print(f'\n{self.grey}{how_many} dependencies for {package}{self.endc}\n')
