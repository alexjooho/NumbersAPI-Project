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
            was_submitted=True
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

    def test_date_fact(self):
        """Test to retrieve random fact by specific month/day"""
        with self.client as c:
            resp = c.get("/api/dates/1/10")

            self.assertEqual(resp.status_code, 200)

            data = resp.json

            self.assertEqual(data, ({
                'month': 1,
                'day': 10,
                'year': 1900,
                'fact_fragment': "test1 fragment",
                'fact_statement': "test1 statement",
                'type': 'date'
            }))
