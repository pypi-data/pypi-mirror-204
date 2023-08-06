import unittest

from pathlib import Path
from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.sbos.queries import SBoQueries


class TestUtilities(unittest.TestCase):

    def setUp(self):
        self.utils = Utilities()
        self.sbo_queries = SBoQueries()
        self.data: dict = self.sbo_queries.repository_data()
        self.build_path = Configs.build_path
        self.package = 'aaa_base-15.0-x86_64-4_slack15.0'

    def test_ins_installed(self):
        self.assertEqual(self.package, self.utils.is_package_installed('aaa_base'))

    def test_split_name(self):
        self.assertEqual('aaa_base', self.utils.split_binary_pkg(self.package)[0])

    def test_split_version(self):
        self.assertEqual('15.0', self.utils.split_binary_pkg(self.package)[1])

    def test_split_arch(self):
        self.assertEqual('x86_64', self.utils.split_binary_pkg(self.package)[2])

    def test_split_build(self):
        self.assertEqual('4', self.utils.split_binary_pkg(self.package)[3])

    def test_is_installed(self):
        self.assertEqual(self.package, self.utils.is_package_installed('aaa_base'))

    def test_all_installed(self):
        self.assertIn(self.package, self.utils.installed_packages.values())

    def test_read_build_tag(self):
        self.assertEqual('1', self.utils.read_sbo_build_tag('slpkg', 'system'))

    def test_is_option(self):
        self.assertTrue(True, self.utils.is_option(['-P', '--parallel'],
                                                   ['-k', '-p', '-P', '--parallel', '--bin-repo']))

    def test_get_file_size(self):
        self.assertEqual('2 MB', self.utils.get_file_size(Path('/var/log/packages/', self.package)))

    def test_apply_package_pattern(self):
        self.assertGreater(len(self.utils.apply_package_pattern(self.data, ['*'])), 1)


if __name__ == '__main__':
    unittest.main()
