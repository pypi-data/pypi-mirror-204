#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import time
import shutil
import logging
import fnmatch
import subprocess
from pathlib import Path
from typing import Generator, Union

from slpkg.configs import Configs
from slpkg.blacklist import Blacklist
from slpkg.repositories import Repositories
from slpkg.logging_config import LoggingConfig


class Utilities:

    def __init__(self):
        self.configs = Configs
        self.colors = self.configs.colour
        self.color = self.colors()
        self.black = Blacklist()
        self.repos = Repositories()

        self.bold: str = self.color['bold']
        self.yellow: str = self.color['yellow']
        self.cyan: str = self.color['cyan']
        self.red: str = self.color['red']
        self.endc: str = self.color['endc']
        self.bred: str = f'{self.bold}{self.red}'

        self.installed_packages: dict = dict(self.all_installed())

        logging.basicConfig(filename=LoggingConfig.log_file,
                            filemode='w',
                            encoding='utf-8',
                            level=logging.INFO)

    def is_package_installed(self, name: str) -> str:
        """ Returns the installed package binary. """
        try:
            return self.installed_packages[name]
        except KeyError:
            return ''

    def all_installed(self) -> dict:
        """ Return all installed packages from /val/log/packages folder. """
        var_log_packages: Path = Path(self.configs.log_packages)

        try:
            for file in var_log_packages.glob(self.configs.file_pattern):
                name = self.split_binary_pkg(file.name)[0]

                if not name.startswith('.') and not self.blacklist_pattern(name):
                    yield name, file.name

        except ValueError as err:
            logger = logging.getLogger(__name__)
            logger.info('%s: %s: %s', self.__class__.__name__,
                        Utilities.all_installed.__name__,
                        err)

    @staticmethod
    def remove_file_if_exists(path: Path, file: str) -> None:
        """ Clean the old files. """
        archive = Path(path, file)
        if archive.is_file():
            archive.unlink()

    @staticmethod
    def remove_folder_if_exists(folder: Path) -> None:
        """ Clean the old folders. """
        if folder.exists():
            shutil.rmtree(folder)

    @staticmethod
    def create_folder(path: Path, folder: str) -> None:
        """ Creates folder. """
        directory = Path(path, folder)
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def split_binary_pkg(package: str) -> list:
        """ Split the package by the name, version, arch, build and tag. """
        name: str = '-'.join(package.split('-')[:-3])
        version: str = ''.join(package[len(name):].split('-')[:-2])
        arch: str = ''.join(package[len(name + version) + 2:].split('-')[:-1])
        build_tag: str = package.split('-')[-1]
        build: str = ''.join(re.findall(r'\d+', build_tag[:2]))

        return [name, version, arch, build]

    def finished_time(self, elapsed_time: float) -> None:
        """ Printing the elapsed time. """
        print(f'\n{self.yellow}Finished Successfully:{self.endc}',
              time.strftime(f'[{self.cyan}%H:%M:%S{self.endc}]',
                            time.gmtime(elapsed_time)))

    def read_sbo_build_tag(self, sbo: str, location: str) -> str:
        """ Returns build tag from .SlackBuild file. """
        build: str = ''

        sbo_script = Path(self.repos.sbo_repo_path, location, sbo, f'{sbo}.SlackBuild')

        if sbo_script.is_file():
            with open(sbo_script, 'r', encoding='utf-8') as f:
                lines = f.readlines()

                for line in lines:
                    if line.startswith('BUILD=$'):
                        build = ''.join(re.findall(r'\d+', line))

        return build

    @staticmethod
    def is_option(flag: list, flags: list) -> bool:
        """ Checking for flags. """
        for f in flag:
            if f in flags:
                return True
        return False

    def read_packages_from_file(self, file: Path) -> Generator:
        """ Reads packages from file and split these to list. """
        try:

            with open(file, 'r', encoding='utf-8') as pkgs:
                packages: list = pkgs.read().splitlines()

            for package in packages:
                if package and not package.startswith('#'):
                    if '#' in package:
                        package = package.split('#')[0].strip()

                    yield package

        except FileNotFoundError:
            self.raise_error_message(f"No such file or directory: '{file}'")

    @staticmethod
    def read_file(file: Union[str, Path]) -> list:
        """ Reads the text file. """
        with open(file, 'r', encoding='utf-8', errors='replace') as f:
            return f.readlines()

    @staticmethod
    def process(command: str, stderr=None, stdout=None) -> None:
        """ Handle the processes. """
        try:
            output = subprocess.call(command, shell=True, stderr=stderr, stdout=stdout)
        except (KeyboardInterrupt, subprocess.CalledProcessError) as err:
            raise SystemExit(err)

        if output != 0:
            raise SystemExit(output)

    def raise_error_message(self, message: str) -> None:
        """ A general method to raise an error message and exit. """
        raise SystemExit(f"\n{self.configs.prog_name}: {self.bred}Error{self.endc}: {message}.\n")

    def get_file_size(self, file: Path) -> str:
        """ Get the local file size and converted to units. """
        size = Path(file).stat().st_size
        return self.convert_file_sizes(size)

    @staticmethod
    def convert_file_sizes(size: int) -> str:
        """ Convert file sizes. """
        units: list = ['KB', 'MB', 'GB']

        for unit in units:
            if size < 1000:
                return f'{size:.0f} {unit}'
            size /= 1000

    @staticmethod
    def apply_package_pattern(data: dict, packages: list) -> list:
        """ Apply the pattern. """
        for pkg in packages:

            if pkg == '*':
                packages.remove(pkg)
                packages += list(data.keys())

        return packages

    def blacklist_pattern(self, name):
        """ This module provides support for Unix shell-style wildcards. """
        if [black for black in self.black.packages() if fnmatch.fnmatch(name, black)]:
            return True

    def repository_name(self, data):
        """ Get the binary repository name from the repository data. """
        try:
            # Binary repository name
            repo: list = list(data.values())[0][11]
        except (IndexError, AttributeError):
            # Slackbuilds repository name 'sbo | ponce'
            repo: str = self.repos.sbo_enabled_repo_name

        return repo
