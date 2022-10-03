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
            fact_statement="1 is the year for this test fact statement.",
            was_submitted=False
        )
        self.y2 = Year(
            year=2,
            fact_fragment="the year for the second test entry",
            fact_statement="2 is the year for this test fact statement.",
            was_submitted=False
        )
        self.y3 = Year(
            year=3,
            fact_fragment="the year for the third test entry",
            fact_statement="3 is the year for this test fact statement.",
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
            self.assertEqual(
                resp.json,
                {'fact': {
                    'year': 1,
                    'fragment': 'the year for the first test entry',
                    'statement': '1 is the year for this test fact statement.',
                    'type': 'year',
                }})

            self.assertEqual(resp.status_code, 200)

    def test_error_for_year_without_fact(self):
        """Tests for getting an error for a year without a fact.
        """
        with self.client as c:

            resp = c.get("api/years/100000")
            self.assertEqual(
                resp.json,
                {'error': {
                    'status': 404,
                    'message': 'A fact for 100000 not found',
                }})
            
            self.assertEqual(resp.status_code, 404)

    def test_get_year_fact_random(self):
        """Test for getting a single fact on a random year."""
        with self.client as c:
            
            y1_resp = c.get("api/years/1")
            y2_resp = c.get("api/years/2")
            y3_resp = c.get("api/years/3")
            
            resp_list = [y1_resp.json, y2_resp.json, y3_resp.json]

            random_resp = c.get("api/years/random")
            
            self.assertIn(random_resp.json, resp_list)
            self.assertEqual(random_resp.status_code, 200)

    def test_invalid_year_url_input(self):
        """Test for invalid URL input for a year."""
        with self.client as c:

            resp = c.get("api/years/BLAH")
            self.assertFalse(resp.json)
            self.assertEqual(resp.status_code, 404)