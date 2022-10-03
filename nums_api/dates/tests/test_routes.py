from unittest import TestCase
from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from nums_api.dates.models import Date

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.drop_all()
db.create_all()


class DateRouteTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""
        self.client = app.test_client()

        self.test1 = Date(
            day_of_year=10,
            year=1900,
            fact_fragment="test1 fragment",
            fact_statement="test1 statement",
            was_submitted=False
        )

        self.test2 = Date(
            day_of_year=50,
            year=1900,
            fact_fragment="test2 fragment",
            fact_statement="test2 statement",
            was_submitted=False
        )

        db.session.add_all([self.test1, self.test2])
        db.session.commit()

        self.test1_id = self.test1.id
        self.test2_id = self.test2.id

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

class DatesRouteTests(DateRouteTestCase):
    def test_date_fact(self):
        """Test GET route for dates/month/day returns correct JSON response"""
        with app.test_client() as c:
            resp = c.get("/api/dates/1/10")

            self.assertEqual(resp.status_code, 200)

            data = resp.json

            self.assertEqual(data, ({"fact":
                                     {
                                         'day_of_year': 10,
                                         'year': 1900,
                                         'fact_fragment': "test1 fragment",
                                         'fact_statement': "test1 statement",
                                         'type': 'date'
                                     }}))

    def test_invalid_day(self):
        """Test GET route for dates/month/day returns 404 if invalid day"""
        with app.test_client() as c:
            resp = c.get("/api/dates/10/32")

            self.assertEqual(resp.status_code, 404)

            data = resp.json

            self.assertEqual(data, {"error": {
                "message": "Invalid value for day",
                "status": 404
            }})

    def test_invalid_month(self):
        """Test GET route for dates/month/day returns 404 if invalid month"""
        with app.test_client() as c:
            resp = c.get("/api/dates/100/30")

            self.assertEqual(resp.status_code, 404)

            data = resp.json

            self.assertEqual(data, {"error": {
                "message": "Invalid value for month",
                "status": 404
            }})

    def test_date_without_fact(self):
        """Test GET route for dates/month/day returns 404 if date does not have fact"""
        with app.test_client() as c:
            resp = c.get("/api/dates/1/30")

            self.assertEqual(resp.status_code, 404)

            data = resp.json

            self.assertEqual(data, {"error": {
                "message": "A date fact for 1/30 not found",
                "status": 404
            }})


class DatesRandomRouteTests(DateRouteTestCase):
    def test_random_date_fact(self):
        """Test GET route for dates/random returns correct JSON response"""
        with app.test_client() as c:

            resp1 = c.get("/api/dates/1/10") # this is test1 input month/day
            resp2 = c.get("/api/dates/2/19") # this is test2 input month/day
            resp_list = [resp1.json, resp2.json]

            resp_random = c.get("/api/dates/random")

            data = resp_random.json

            self.assertEqual(resp_random.status_code, 200)

            self.assertIn(data, resp_list)