import os
import shutil
import unittest

from database import Database
from processing.fetch10K import Fetch10K
from processing.utils import ProcessingRequest

class ProcessingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.db = Database(dbName='unittest_fsil.db')
        self.fetch10K = Fetch10K("Testing", "test@noreply.com", "unittest-sec-filings")

    def test_apple_05_2024_num(self) -> None:
        self.assertEqual(
            len(self.fetch10K.download("AAPL")),
            28,
        )

    def test_db_cache(self) -> None:
        self.db.cache_filing("AAPL", "GARBAGE_DATA")
        self.assertTrue(self.db.filing_is_cached("AAPL"))

    def tearDown(self) -> None:
        os.remove('unittest_fsil.db')
        # shutil.rmtree('unittest-sec-filings')

        return super().tearDown()
