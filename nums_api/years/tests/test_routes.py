from unittest import TestCase
from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from nums_api.years.models import Year

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.drop_all()
db.create_all()

class YearRouteTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""
        self.client = app.test_client()

        Year.query.delete()

        self.y1 = Year(
            year=1,
            fact_fragment="the year for the first test entry",
            fact_statement="First test for year 1",
            was_submitted=False
        )
        self.y2 = Year(
            year=2,
            fact_fragment="the year for the second test entry",
            fact_statement="2 is the year for this test fact statement.",
            was_submitted=False
        )
        self.y3 = Year(
            year=1,
            fact_fragment="the year for the third test entry",
            fact_statement="Another test for year 1.",
            was_submitted=False
        )

        db.session.add_all([self.y1, self.y2, self.y3])
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

    def test_get_year_fact(self):
        """Tests for getting a single fact by year.
        Get a single fact about the year 1"""
        with self.client as c:

            resp = c.get("/api/years/1")
            print("FACT ", resp.json["fact"])
            self.assertIn("year 1", resp.json["fact"]["fact_statement"])
            self.assertEqual(resp.status_code, 200)

    def test_error_for_year_without_fact(self):
        """Tests for getting an error for a year without a fact.
        """
        with self.client as c:

            resp = c.get("api/years/100000")
            self.assertIn("not found", resp.json["error"]["message"])
            self.assertEqual(resp.status_code, 404)

    def test_get_year_fact_random(self):
        """Test for getting a single fact on a random year."""
        with self.client as c:

            resp = c.get("api/years/random")
            self.assertTrue(resp.json["fact"]["fact_fragment"])
            with self.assertRaises(KeyError):
                resp.json["error"]["message"]
            self.assertEqual(resp.status_code, 200)

    def test_invalid_year_url_input(self):
        """Test for invalid URL input for a year."""
        with self.client as c:

            resp = c.get("api/years/BLAH")
            self.assertFalse(resp.json)
            self.assertEqual(resp.status_code, 404)