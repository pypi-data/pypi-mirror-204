import unittest
from slpkg.checks import Check
from slpkg.binaries.queries import BinQueries


class TestPkgInstalled(unittest.TestCase):

    def setUp(self):
        self.bin_queries = BinQueries('alien')
        self.data = self.bin_queries.repository_data()
        self.check = Check(['-B', '--bin-repo='], self.data)
        self.packages = ['audacity', 'vlc', 'dnspython']

    def test_check_exists(self):
        self.assertIsNone(self.check.exists_in_the_database(self.packages))

    def test_check_unsupported(self):
        self.assertIsNone(self.check.is_package_unsupported(self.packages))

    def test_check_is_installed(self):
        self.assertIsNone(self.check.is_package_unsupported(self.packages))


if __name__ == "__main__":
    unittest.main()
