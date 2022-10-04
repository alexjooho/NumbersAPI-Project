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


class DateRouteBaseTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""
        self.client = app.test_client()

        Date.query.delete()

        self.d1 = Date(
            day_of_year=10,
            year=1900,
            fact_fragment='test1 fragment',
            fact_statement='test1 statement',
            was_submitted=False
        )

        self.d2 = Date(
            day_of_year=50,
            year=1900,
            fact_fragment='test2 fragment',
            fact_statement='test2 statement',
            was_submitted=False
        )

        db.session.add_all([self.d1, self.d2])
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)


class DateRouteSpecificDateTestCase(DateRouteBaseTestCase):
    def test_get_date_fact(self):
        """Test GET route for dates/month/day returns correct JSON response"""
        with app.test_client() as c:
            resp = c.get('/api/dates/1/10')

            data = resp.json

            self.assertEqual(
                data,
                {'fact': {
                    'number': 10,
                    'year': 1900,
                    'fragment': 'test1 fragment',
                    'statement': 'test1 statement',
                    'type': 'date'
                }})

            self.assertEqual(resp.status_code, 200)

    def test_error_invalid_day(self):
        """Test GET route for dates/month/day returns 400 if invalid day"""
        with app.test_client() as c:
            resp = c.get('/api/dates/10/32')

            data = resp.json

            self.assertEqual(
                data,
                {'error': {
                    'message': 'Invalid value for day',
                    'status': 400
                }})

            self.assertEqual(resp.status_code, 400)

    def test_error_invalid_month(self):
        """Test GET route for dates/month/day returns 400 if invalid month"""
        with app.test_client() as c:
            resp = c.get('/api/dates/100/30')

            data = resp.json

            self.assertEqual(
                data,
                {'error': {
                    'message': 'Invalid value for month',
                    'status': 400
                }})

            self.assertEqual(resp.status_code, 400)

    def test_error_date_without_fact(self):
        """Test GET route for dates/month/day returns 404 if date does not have fact"""
        with app.test_client() as c:
            resp = c.get('/api/dates/1/30')

            data = resp.json

            self.assertEqual(
                data,
                {'error': {
                    'message': 'A date fact for 1/30 not found',
                    'status': 404
                }})

            self.assertEqual(resp.status_code, 404)


class DateRouteRandomDateTestCase(DateRouteBaseTestCase):
    def test_get_random_date_fact(self):
        """Test GET route for dates/random returns correct JSON response"""
        with app.test_client() as c:

            resp1 = c.get('/api/dates/1/10')  # this is test1 input month/day
            resp2 = c.get('/api/dates/2/19')  # this is test2 input month/day
            resp_list = [resp1.json, resp2.json]

            resp_random = c.get('/api/dates/random')

            data = resp_random.json

            self.assertIn(data, resp_list)

            self.assertEqual(resp_random.status_code, 200)
