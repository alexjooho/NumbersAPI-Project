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
        Trivia.query.delete()

        t1 = Trivia(
            number=1,
            fact_fragment='cool number',
            fact_statement='1 is the first number after 0.',
            was_submitted=True
        )

        t2 = Trivia(
            number=2,
            fact_fragment='not a cool number',
            fact_statement='2 is the most lame number.',
            was_submitted=True
        )

        t3 = Trivia(
            number=3,
            fact_fragment='meh number',
            fact_statement='3 is honestly a meh number.',
            was_submitted=True
        )

        db.session.add_all([t1, t2, t3])
        db.session.commit()

        self.t1_id = t1.id
        self.t2_id = t2.id
        self.t3_id = t3.id

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

    def test_specific_number(self):
        """ Tests for getting a fact about a specific number """
        with self.client as c:
            resp = c.get("/api/trivia/1")
            data = resp.json

            self.assertEqual(data, {
                "number": 1, "fragment": 'cool number',
                "statement": '1 is the first number after 0.', "type": "trivia"
            })
            self.assertEqual(resp.status_code, 200)

    def test_specific_number_invalid(self):
        """ Tests for an invalid number """
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

    def test_get_random_trivia(self):
        """ Tests getting a random fact """
        with self.client as c:
            resp = c.get("/api/trivia/random")
            data = resp.json
            resp1 = c.get("/api/trivia/1")
            data1= resp1.json
            resp2 = c.get("/api/trivia/2")
            data2= resp2.json
            resp3 = c.get("/api/trivia/3")
            data3= resp3.json

            possible_results = [
                {"random": data1["fragment"]},
                {"random": data2["fragment"]},
                {"random": data3["fragment"]}
            ]

            self.assertIn(data, possible_results)
            self.assertEqual(resp.status_code, 200)
