import unittest
from slpkg.sbos.queries import SBoQueries


class TestSBoQueries(unittest.TestCase):

    def setUp(self):
        self.sbo_queries = SBoQueries()
        self.data: dict = self.sbo_queries.repository_data()
        self.name: str = 'slpkg'

    def test_slackbuild(self):
        self.assertTrue(True, self.data[self.name])

    def test_location(self):
        self.assertEqual('system', self.data[self.name][0])

    def test_sources_x86(self):
        self.assertEqual(['https://gitlab.com/dslackw/slpkg/-/archive'
                         '/4.7.8/slpkg-4.7.8.tar.gz'], self.data[self.name][3].split())

    def test_sources_x86_64(self):
        self.assertEqual([], self.data[self.name][4].split())

    def test_requires(self):
        self.assertEqual(['SQLAlchemy', 'python3-pythondialog', 'python3-progress'], self.data[self.name][7].split())

    def test_version(self):
        self.assertEqual('4.7.8', self.data[self.name][2])

    def test_checksum_x86(self):
        self.assertListEqual(['d0ba1c826dc691ceec1ad12603e51330'], self.data[self.name][5].split())

    def test_checksum_x86_64(self):
        self.assertListEqual([], self.data[self.name][6].split())

    def test_files(self):
        self.assertEqual(5, len(self.data[self.name][1].split()))

    def test_description(self):
        self.assertEqual('slpkg (Slackware Packaging Tool)', self.data[self.name][8])


if __name__ == '__main__':
    unittest.main()
