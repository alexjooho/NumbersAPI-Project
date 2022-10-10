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


class SingleTriviaRouteTestCase(TriviaRouteTestCase):
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

    def test_error_for_number_with_no_fact(self):
        """ Tests that a number with no fact will return an error """
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

    def test_get_trivia_fact_invalid_number(self):
        """ Tests that an error will be thrown if an invalid number is given in URL parameter """
        with self.client as c:
            resp = c.get("/api/trivia/test")

            self.assertEqual(resp.status_code, 400)


class TriviaBatchRouteTestCase(TriviaRouteTestCase):
    def test_get_batch_Trivia_fact(self):
        """Test GET route for batch trivia facts with ".." returns correct JSON response"""
        with self.client as client:
            self.maxDiff = None
            resp = client.get("/api/trivia/1..3")

            self.assertEqual(resp.json,
                             {
                                 "facts":
                                 [
                                     {
                                         "number": "1",
                                         "fragment": "test 1",
                                         "statement": "1 is the number for this test fact statement.",
                                         "type": "trivia"
                                     },
                                     {
                                         "number": "2",
                                         "fragment": "test 2",
                                         "statement": "2 is the number for this test fact statement.",
                                         "type": "trivia"
                                     },
                                     {
                                         "number": "3",
                                         "fragment": "test 3",
                                         "statement": "3 is the number for this test fact statement.",
                                         "type": "trivia"
                                     }
                                 ]
                             })

            self.assertEqual(resp.status_code, 200)

    def test_get_batch_trivia_separated_by_commas(self):
        """Tests for getting trivia facts for multiple numbers seperated
        by comma works.
        """
        with self.client as c:
            resp = c.get("/api/trivia/1,2")

            self.assertEqual(resp.json,
                             {
                                 "facts":
                                 [
                                     {
                                         "number": "1",
                                         "fragment": "test 1",
                                         "statement": "1 is the number for this test fact statement.",
                                         "type": "trivia"
                                     },
                                     {
                                         "number": "2",
                                         "fragment": "test 2",
                                         "statement": "2 is the number for this test fact statement.",
                                         "type": "trivia"
                                     },
                                 ]
                             })

            self.assertEqual(resp.status_code, 200)

    def test_multiple_numbers_with_all_syntax_combo(self):
        """Tests for getting a facts for multiple numbers seperated by comma or by '..'
        """
        with self.client as c:

            resp = c.get("api/trivia/1..2,3")

            self.assertEqual(resp.json, {
                "facts":
                [
                    {
                        "number": "1",
                        "fragment": "test 1",
                        "statement": "1 is the number for this test fact statement.",
                        "type": "trivia"
                    },
                    {
                        "number": "2",
                        "fragment": "test 2",
                        "statement": "2 is the number for this test fact statement.",
                        "type": "trivia"
                    },
                    {
                        "number": "3",
                        "fragment": "test 3",
                        "statement": "3 is the number for this test fact statement.",
                        "type": "trivia"
                    }
                ]
            })
            self.assertEqual(resp.status_code, 200)

    def test_get_batch_trivia_fact_error(self):
        """Test error handling for batch trivia facts"""

        with self.client as c:
            resp = c.get("/api/trivia/TEST..TEST")

            self.assertEqual(resp.status_code, 400)
            self.assertEqual(resp.json, {
                "error": {
                    "message": "Invalid URL",
                    "status": 400}
            })

    def test_batch_trivia_with_no_facts(self):
        """Tests for getting multiple trivia facts separated by comma where
        there are no facts available.
        """
        with self.client as c:

            resp = c.get("api/trivia/5,6..10")

            self.assertEqual(resp.json, {"error": {
                "status": 404,
                "message": "No facts for 5,6..10 were found",
            }})

            self.assertEqual(resp.status_code, 404)

    def test_invalid_number_url_input(self):
        """Test for invalid URL input for a number."""
        with self.client as c:

            resp = c.get("api/trivia/TEST")
            self.assertEqual(
                resp.json,
                {"error": {
                    "status": 400,
                    "message": "Invalid URL",
                }})

            self.assertEqual(resp.status_code, 400)


class TriviaRandomRouteTestCase(TriviaRouteTestCase):
    def test_get_random_trivia_fact(self):
        """Test for getting a single fact on a random number (default, no count
        param)."""
        with self.client as c:

            t1resp = c.get("/api/trivia/1")
            t2resp = c.get("/api/trivia/2")
            t3resp = c.get("/api/trivia/3")

            t1_fact_data = t1resp.json
            t2_fact_data = t2resp.json
            t3_fact_data = t3resp.json

            resp = c.get("/api/trivia/random")
            data = resp.json

            self.assertIn(data, [t1_fact_data, t2_fact_data, t3_fact_data])
            self.assertEqual(resp.status_code, 200)

    def test_get_random_trivia_fact_with_count(self):
        """Test for getting a count number of random trivia facts if count param
        is specified."""
        with app.test_client() as client:

            resp1 = client.get("/api/trivia/1")
            resp2 = client.get("/api/trivia/2")
            resp3 = client.get("/api/trivia/3")

            resp_list = [resp1.json["fact"],
                         resp2.json["fact"], resp3.json["fact"]]

            resp_random = client.get("/api/trivia/random?count=2")

            data = resp_random.json

            self.assertIn(data[0], resp_list)
            self.assertIn(data[1], resp_list)
            self.assertIs(len(data), 2)

            self.assertEqual(resp_random.status_code, 200)

    # test_get_trivia_fact_random_count_exceeds_max(self) does not work
    # without mocked MAX_BATCH variable

    # def test_get_trivia_fact_random_count_exceeds_max(self):
    #     """Test for getting a count number that exceeds total number of random
    #     number facts."""
    #     with self.client as c:

    #         y1_resp = c.get("api/trivia/1")
    #         y2_resp = c.get("api/trivia/2")
    #         y3_resp = c.get("api/trivia/3")

    #         resp_list = [
    #             y1_resp.json["fact"],
    #             y2_resp.json["fact"],
    #             y3_resp.json["fact"]
    #         ]

    #         random_resp = c.get("api/trivia/random?count=100")
    #         resp = random_resp.json

    #         self.assertIn(resp[0], resp_list)
    #         self.assertIn(resp[1], resp_list)
    #         self.assertIn(resp[2], resp_list)
    #         with self.assertRaises(IndexError) as exc:
    #             resp[3]
    #             self.assertEqual(str(exc.exception), "list index out of range")
    #         self.assertEqual(random_resp.status_code, 200)

    def test_error_get_trivia_fact_random_count_is_negative(self):
        """Test error if count param is negative for random trivia facts."""
        with self.client as c:

            resp = c.get("api/trivia/random?count=-100")
            self.assertEqual(
                resp.json,
                {"error": {
                    "status": 400,
                    "message": "-100 is an invalid count number",
                }})

            self.assertEqual(resp.status_code, 400)

    def test_error_get_trivia_fact_random_count_is_not_an_integer(self):
        """Test error if count param is not an integer for random trivia facts."""
        with self.client as c:

            resp = c.get("api/trivia/random?count=TEST")
            self.assertEqual(
                resp.json,
                {"error": {
                    "status": 400,
                    "message": "TEST is an invalid count number",
                }})

            self.assertEqual(resp.status_code, 400)
