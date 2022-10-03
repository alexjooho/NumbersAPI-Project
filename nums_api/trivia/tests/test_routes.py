""" Tests for trivia routes.
    To run tests in venv: python3 -m unittest test_routes.py -v
"""

from unittest import TestCase
from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from nums_api.trivia.models import Trivia

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.drop_all()
db.create_all()


class TriviaRouteTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""
        self.client = app.test_client()
        Trivia.query.delete()

        self.t1 = Trivia(
            number=1,
            fact_fragment="test 1",
            fact_statement="1 is the number for this test fact statement.",
            was_submitted=False
        )

        self.t2 = Trivia(
            number=2,
            fact_fragment="test 2",
            fact_statement="2 is the number for this test fact statement.",
            was_submitted=False
        )

        self.t3 = Trivia(
            number=3,
            fact_fragment="test 3",
            fact_statement="3 is the number for this test fact statement.",
            was_submitted=False
        )

        db.session.add_all([self.t1, self.t2, self.t3])
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

    def test_get_trivia_fact(self):
        """ Tests for getting a fact for number 1 """
        with self.client as c:
            resp = c.get("/api/trivia/1")
            data = resp.json

            self.assertEqual(
                data,
                {"fact": {
                    "number": 1,
                    "fragment": "test 1",
                    "statement": "1 is the number for this test fact statement.",
                    "type": "trivia"
                }
                })
            self.assertEqual(resp.status_code, 200)

    def test_get_trivia_fact_with_notfound_query_floor(self):
        """Test GET route for trivia/number with no trivia fact and
        notfound = 'floor' query parameter, finds the previous existing trivia
        fact and returns correct JSON response """
        with self.client as c:
            resp = c.get("/api/trivia/4?notfound=floor")
            data = resp.json

            self.assertEqual(
                data,
                {"fact": {
                    "number": 3,
                    "fragment": "test 3",
                    "statement": "3 is the number for this test fact statement.",
                    "type": "trivia"
                }
                })
            self.assertEqual(resp.status_code, 200)

    def test_get_trivia_fact_with_notfound_query_ceil(self):
        """Test GET route for trivia/number with no trivia fact and
        notfound = 'ceil' query parameter, finds the next existing trivia fact
        and returns correct JSON response"""
        with self.client as c:
            resp = c.get("/api/trivia/0?notfound=ceil")
            data = resp.json

            self.assertEqual(
                data,
                {"fact": {
                    "number": 1,
                    "fragment": "test 1",
                    "statement": "1 is the number for this test fact statement.",
                    "type": "trivia"
                }
                })
            self.assertEqual(resp.status_code, 200)

    def test_error_for_number_with_no_fact_and_notfound_floor_doesnotexist(self):
        """Test GET route for trivia/number returns 404 if number not found and
        no existing trivia fact for previous number"""
        with self.client as c:
            resp = c.get("/api/trivia/0?notfound=floor")
            data = resp.json

            self.assertEqual(
                data,{
                "error": {
                    "message": "A trivia fact for 0 not found",
                    "status": 404
                }})
            self.assertEqual(resp.status_code, 404)

    def test_error_for_number_with_no_fact_and_notfound_ceil_doesnotexist(self):
        """Test GET route for trivia/number returns 404 if number not found and
        no existing trivia fact for next number"""
        with self.client as c:
            resp = c.get("/api/trivia/5?notfound=ceil")
            data = resp.json

            self.assertEqual(
                data,{
                "error": {
                    "message": "A trivia fact for 5 not found",
                    "status": 404
                }})
            self.assertEqual(resp.status_code, 404)

    def test_error_for_number_with_no_fact_and_no_notfound_query(self):
        """Test GET route for trivia/number returns 404 if number not found and
        no notfound query parameter supplied in request"""
        with self.client as c:
            resp = c.get("/api/trivia/5")
            data = resp.json

            self.assertEqual(data, {
                "error": {
                    "message": "A trivia fact for 5 not found",
                    "status": 404
                }
            })
            self.assertEqual(resp.status_code, 404)

    def test_error_for_number_with_no_fact_and_invalid_notfound_query(self):
        """Test GET route for trivia/number returns 404 if number not found and
        notfound query parameter is invalid (not "ceil" or "floor")"""
        with self.client as c:
            resp = c.get("/api/trivia/5?notfound=true")
            data = resp.json

            self.assertEqual(data, {
                "error": {
                    "message": "A trivia fact for 5 not found",
                    "status": 404
                }
            })
            self.assertEqual(resp.status_code, 404)

    def test_get_trivia_fact_invalid_number(self):
        """ Tests that an error will be thrown if an invalid number is given in URL parameter """
        with self.client as c:
            resp = c.get("/api/trivia/test")

            self.assertEqual(resp.status_code, 404)

    def test_get_random_trivia_fact(self):
        """ Tests getting a random fact """
        with self.client as c:
            resp = c.get("/api/trivia/random")
            data = resp.json

            t1resp = c.get("/api/trivia/1")
            t2resp = c.get("/api/trivia/2")
            t3resp = c.get("/api/trivia/3")

            t1_fact_data = t1resp.json
            t2_fact_data = t2resp.json
            t3_fact_data = t3resp.json

            self.assertIn(data, [t1_fact_data, t2_fact_data, t3_fact_data])
            self.assertEqual(resp.status_code, 200)
