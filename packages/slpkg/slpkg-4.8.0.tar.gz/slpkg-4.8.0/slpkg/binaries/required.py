#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.repositories import Repositories


class Required:
    """ Creates a list of dependencies with
    the right order to install. """

    def __init__(self, data: dict, name: str):
        __slots__ = 'data', 'name,'
        self.data: dict = data
        self.name: str = name
        self.repos = Repositories()

        self.special_repos: list = [
            self.repos.salixos_repo_name,
            self.repos.salixos_patches_repo_name,
            self.repos.salixos_extra_repo_name,
            self.repos.slackel_repo_name,
            self.repos.slint_repo_name
        ]

        self.repo = self.data[name][11]

    def resolve(self) -> list:
        """ Resolve the dependencies. """
        required: list[str] = list(self.remove_deps(self.data[self.name][6].split()))

        # Resolve dependencies for some special repos.
        if self.repo in self.special_repos:
            for req in required:
                if req not in list(self.data.keys()):
                    required.remove(req)

        else:
            for req in required:
                sub_required: list[str] = list(self.remove_deps(self.data[req][6].split()))
                for sub in sub_required:
                    required.append(sub)

        required.reverse()
        return list(dict.fromkeys(required))

    def remove_deps(self, requires):
        """ Remove requires that not in the repository or blacklisted. """
        for dep in requires:
            if dep in list(self.data.keys()):
                yield dep
