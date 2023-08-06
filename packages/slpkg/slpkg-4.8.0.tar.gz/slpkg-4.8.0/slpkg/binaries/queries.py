#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.utilities import Utilities
from slpkg.models.models import BinariesTable
from slpkg.models.models import session as Session


class BinQueries:
    """ Queries class for the binary repositories. """

    def __init__(self, repo: str):
        __slots__ = 'repo'
        self.repo: str = repo
        self.session = Session

        self.utils = Utilities()

    def repository_data(self) -> dict:
        """ Returns a dictionary with the repository data. """
        repository_data: tuple = self.session.query(
            BinariesTable).where(
            BinariesTable.repo == self.repo).all()

        repos_dict: dict = {
            data.name: (data.version,
                        data.package,
                        data.mirror,
                        data.location,
                        data.size_comp,
                        data.size_uncomp,
                        data.required,
                        data.conflicts,
                        data.suggests,
                        data.description,
                        data.checksum,
                        data.repo)
            for data in repository_data
            if not self.utils.blacklist_pattern(data.name)
        }

        return repos_dict

    def repositories_data(self) -> dict:
        """ Returns a dictionary with repositories data. """
        repositories_data: tuple = self.session.query(BinariesTable).all()

        repos_dict: dict = {
            data.id: (data.name,
                      data.version,
                      data.package,
                      data.mirror,
                      data.location,
                      data.size_comp,
                      data.size_uncomp,
                      data.required,
                      data.conflicts,
                      data.suggests,
                      data.description,
                      data.checksum,
                      data.repo)
            for data in repositories_data
            if not self.utils.blacklist_pattern(data.name)
        }

        return repos_dict
