from unittest import TestCase
from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from nums_api.maths.models import Math

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.drop_all()
db.create_all()

class MathRouteBaseTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""
        self.client = app.test_client()

        Math.query.delete()

        self.m1 = Math(
            number=5,
            fact_fragment="the number for this m1 test fact fragment",
            fact_statement="5 is the number for m1 this test fact statement.",
            was_submitted=False
        )

        db.session.add(self.m1)
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

class MathRouteNumberTestCase(MathRouteBaseTestCase):
    def test_get_number(self):
        """Test GET route for math/number returns correct JSON response"""
        with app.test_client() as client:
            url = f"/api/math/{self.m1.number}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "number": "5",
                "fact_fragment":"the number for this m1 test fact fragment",
                "fact_statement":"5 is the number for m1 this test fact statement.",
                "type": "math"
            })

    def test_get_number_404_number_not_found(self):
        """Test GET route for math/number returns 404 if number not found"""
        with app.test_client() as client:
            url = f"/api/math/0"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 404)
            data = resp.json
            self.assertEqual(data, {'error': {
                    'message': "A math fact for 0 not found",
                    'status': 404 } })

    def test_get_number_404_not_a_valid_number(self):
        """Test GET route for math/number returns 404 if number not valid"""
        with app.test_client() as client:
            url = f"/api/math/minaj"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 404)

class MathRouteRandomTestCase(MathRouteBaseTestCase):
    def test_get_number(self):
        """Test GET route for math/random returns correct JSON response"""
        with app.test_client() as client:
            url = f"/api/math/random"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "number": "5",
                "fact_fragment":"the number for this m1 test fact fragment",
                "fact_statement":"5 is the number for m1 this test fact statement.",
                "type": "math"
            })