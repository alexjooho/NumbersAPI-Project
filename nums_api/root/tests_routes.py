"""Homepage View tests."""

from unittest import TestCase
from nums_api import app




class HomepageView(TestCase):
    def setUp(self):
        """Set up test data here"""
        self.client = app.test_client()

    def test_homepage(self):
        """Testing homepage loads correctly"""
        with self.client as c:

            resp = c.get("/")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<body>", str(resp.data))