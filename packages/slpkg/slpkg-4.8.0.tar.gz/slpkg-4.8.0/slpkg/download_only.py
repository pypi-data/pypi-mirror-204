#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import shutil
from pathlib import Path

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.downloader import Downloader
from slpkg.views.views import ViewMessage
from slpkg.repositories import Repositories
from slpkg.models.models import session as Session


class Download(Configs):
    """ Download the slackbuilds with the sources only. """

    def __init__(self, directory: Path, flags: list):
        __slots__ = 'directory', 'flags'
        super(Configs, self).__init__()
        self.flags: list = flags
        self.directory: Path = directory

        self.repos = Repositories()
        self.utils = Utilities()
        self.session = Session

        self.option_for_directory: bool = self.utils.is_option(
            ['-z', '--directory='], self.flags)

        self.option_for_binaries: bool = self.utils.is_option(
            ['-B', '--bin-repo='], self.flags)

    def packages(self, data: dict, packages: list) -> None:
        """ Download the package only. """
        packages: list = self.utils.apply_package_pattern(data, packages)

        view = ViewMessage(self.flags, data)
        view.download_packages(packages, self.directory)
        view.question()

        download_path: Path = self.download_only_path
        if self.option_for_directory:
            download_path: Path = self.directory

        start: float = time.time()
        urls: list = []
        for pkg in packages:

            if self.option_for_binaries:
                package: str = data[pkg][1]
                mirror: str = data[pkg][2]
                location: str = data[pkg][3]
                urls.append(f'{mirror}{location}/{package}')
            else:
                location: str = data[pkg][0]
                if self.os_arch == 'x86_64' and data[pkg][4]:
                    sources = data[pkg][4].split()
                else:
                    sources = data[pkg][3].split()

                urls += sources

                if self.repos.ponce_repo:
                    ponce_repo_path_package = Path(self.repos.ponce_repo_path, location, pkg)
                    shutil.copytree(ponce_repo_path_package, Path(download_path, pkg))
                else:
                    file: str = f'{pkg}{self.repos.sbo_repo_tar_suffix}'
                    urls += [f'{self.repos.sbo_repo_mirror[0]}{location}/{file}']

        down = Downloader(download_path, urls, self.flags)
        down.download()

        elapsed_time: float = time.time() - start
        self.utils.finished_time(elapsed_time)
