import sqlite3
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from setup_db import create_db

class RetailSQLTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp.name) / 'test.db'
        create_db(self.db_path)
        self.conn = sqlite3.connect(self.db_path)

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def query(self, filename):
        sql = (ROOT / 'sql' / filename).read_text(encoding='utf-8')
        return self.conn.execute(sql).fetchall()

    def test_monthly_revenue(self):
        rows = self.query('01_monthly_revenue.sql')
        self.assertEqual(sum(row[1] for row in rows), 72500)
        self.assertEqual(sum(row[2] for row in rows), 3)

    def test_top_product(self):
        self.assertEqual(self.query('03_top_products.sql')[0], ('Laptop', 1, 50000))

    def test_lifetime_value_includes_zero_spend_customer(self):
        rows = self.query('05_customer_ltv.sql')
        self.assertEqual(len(rows), 4)
        self.assertIn(('Morgan Patel', 0, 0), rows)

    def test_country_rank_is_separate(self):
        rows = self.query('04_country_rank.sql')
        canada = [r for r in rows if r[0] == 'Canada']
        usa = [r for r in rows if r[0] == 'USA']
        self.assertEqual(canada[0][3], 1)
        self.assertEqual(usa[0][3], 1)

if __name__ == '__main__':
    unittest.main()
