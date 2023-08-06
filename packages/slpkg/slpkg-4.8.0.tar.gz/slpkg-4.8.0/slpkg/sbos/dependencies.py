#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Requires:
    """ Creates a list of dependencies with
    the right order to install. """

    def __init__(self, data: dict, name: str):
        __slots__ = 'data', 'name'
        self.data: dict = data
        self.name: str = name

    def resolve(self) -> list:
        """ Resolve the dependencies. """
        requires: list[str] = list(self.remove_deps(self.data[self.name][7].split()))

        for req in requires:
            sub_requires: list[str] = list(self.remove_deps(self.data[req][7].split()))
            for sub in sub_requires:
                requires.append(sub)

        requires.reverse()

        return list(dict.fromkeys(requires))

    def remove_deps(self, requires):
        """ Remove requires that not in the repository or blacklisted. """
        for dep in requires:
            if dep in list(self.data.keys()):
                yield dep
