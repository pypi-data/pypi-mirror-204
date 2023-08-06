#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.repositories import Repositories
from slpkg.models.models import session as Session
from slpkg.models.models import SBoTable, PonceTable


class SBoQueries(Configs):
    """ Queries class for the sbo repository. """

    def __init__(self):
        super(Configs, self).__init__()
        self.session = Session

        self.repos = Repositories()
        self.utils = Utilities()

        # Switch between sbo and ponce repository.
        self.sbo_table = SBoTable
        if self.repos.ponce_repo:
            self.sbo_table = PonceTable

    def repository_data(self) -> dict:
        """ Returns a dictionary with the repository data. """
        repository_data: tuple = self.session.query(self.sbo_table).all()

        repos_dict: dict = {
            data.name: (data.location,
                        data.files,
                        data.version,
                        data.download,
                        data.download64,
                        data.md5sum,
                        data.md5sum64,
                        data.requires,
                        data.short_description)
            for data in repository_data
            if not self.utils.blacklist_pattern(data.name)
        }

        return repos_dict
