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
            html = resp.get_data(as_text=True)

            self.assertIn('Numbers API V2 Documentation', html)
            self.assertEqual(200, resp.status_code)