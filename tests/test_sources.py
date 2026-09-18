import unittest
from job_sources.companies import JOB_SOURCES
from job_sources.fetcher import FETCHERS

class TestSources(unittest.TestCase):
    def test_sources_have_valid_provider(self):
        self.assertGreaterEqual(len(JOB_SOURCES), 40)
        for source in JOB_SOURCES:
            self.assertIn(source["provider"], FETCHERS)
            self.assertTrue(source["company"])
            self.assertTrue(source["slug"])

if __name__ == "__main__":
    unittest.main()
