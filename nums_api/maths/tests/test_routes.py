from unittest import TestCase, mock
from unittest.mock import patch
from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from nums_api.maths.models import Math
import nums_api.maths.routes
# from nums_api.config import MAX_BATCH
import nums_api.config


app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config.from_object('nums_api.config.TestingConfig')

db.drop_all()
db.create_all()

class MathRouteBaseTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""
        self.client = app.test_client()

        Math.query.delete()

        self.m1 = Math(
            number=1,
            fact_fragment="the number for this m1 test fact fragment",
            fact_statement="1 is the number for m1 this test fact statement.",
            was_submitted=False
        )

        self.m2 = Math(
            number=2,
            fact_fragment="the number for this m2 test fact fragment",
            fact_statement="2 is the number for m2 this test fact statement.",
            was_submitted=False
        )

        self.m3 = Math(
            number=3,
            fact_fragment="the number for this m3 test fact fragment",
            fact_statement="3 is the number for m3 this test fact statement.",
            was_submitted=False
        )

        self.m4 = Math(
            number=3.14,
            fact_fragment="Ah pizza pai",
            fact_statement="3.14 is the number of pi",
            was_submitted=False
        )

        db.session.add(self.m1)
        db.session.add(self.m2)
        db.session.add(self.m3)
        db.session.add(self.m4)

        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)


class MathRouteNumberTestCase(MathRouteBaseTestCase):
    def test_get_math_fact(self):
        """Test GET route for math/number returns correct JSON response"""
        with app.test_client() as client:
            url = f"/api/math/{self.m1.number}"
            resp = client.get(url)

            data = resp.json
            self.assertEqual(data, {"fact": {
                "number": "1",
                "fragment": "the number for this m1 test fact fragment",
                "statement": "1 is the number for m1 this test fact statement.",
                "type": "math"
            }})
            self.assertEqual(resp.status_code, 200)

    def test_error_for_number_with_no_fact(self):
        """Test GET route for math/number returns 404 if number not found"""
        with app.test_client() as client:
            url = f"/api/math/0"
            resp = client.get(url)

            data = resp.json
            self.assertEqual(data, {'error': {
                'message': "A math fact for 0 not found",
                'status': 404}})
            self.assertEqual(resp.status_code, 404)

    def test_error_for_invalid_number(self):
        """Test GET route for math/number returns 404 if number not valid"""
        with app.test_client() as client:
            url = f"/api/math/minaj"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 400)

class MathRouteGetBatchMathFact(MathRouteBaseTestCase):
    def test_get_batch_math_fact(self):
        """Test GET route for batch math with '..' returns correct JSON response"""
        with app.test_client() as client:

            resp = client.get(f"/api/math/1..2")

            self.assertEqual(resp.json,
            {
                "facts":
                [
                    {
                        "number": "1",
                        "fragment": "the number for this m1 test fact fragment",
                        "statement": "1 is the number for m1 this test fact statement.",
                        "type": "math"
                    },
                    {
                        "number": "2",
                        "fragment": "the number for this m2 test fact fragment",
                        "statement": "2 is the number for m2 this test fact statement.",
                        "type": "math"
                    }
                ]
            })

            self.assertEqual(resp.status_code, 200)

    def test_get_batch_math_fact_error(self):
        """Test error handling for batch math facts"""

        with self.client as c:
            resp = c.get("/api/math/BLAH")

            self.assertEqual(resp.json, {
                "error": {
                    "message": "Invalid URL",
                    "status": 400}
            })
            self.assertEqual(resp.status_code, 400)

    def test_get_batch_math_fact_with_decimal(self):
        """Test getting a math fact with decimal"""

        with app.test_client() as client:

            resp = client.get(f"/api/math/3..3.14")

            self.assertEqual(resp.json,
            {
                "facts":
                [
                    {
                        "number": "3",
                        "fragment": "the number for this m3 test fact fragment",
                        "statement": "3 is the number for m3 this test fact statement.",
                        "type": "math"
                    },
                    {
                        "number": "3.14",
                        "fragment": "Ah pizza pai",
                        "statement": "3.14 is the number of pi",
                        "type": "math"
                    }
                ]
            })

            self.assertEqual(resp.status_code, 200)

    def test_range_math_with_no_facts(self):
            """Tests for getting a facts of multiple math seperated by comma, '..'
            and/or '-' works.
            """
            with self.client as c:

                resp = c.get("api/math/5,6,7")

                self.assertEqual(resp.json, {"error": {
                        "status": 404,
                        "message": "No facts for [5, 6, 7] were found",
                    }})
                self.assertEqual(resp.status_code, 404)


class MathRouteRandomTestCase(MathRouteBaseTestCase):
    def test_get_random_math_fact(self):
        """Test GET route for math/random returns correct JSON response"""
        with app.test_client() as client:

            resp1 = client.get(f"/api/math/{self.m1.number}")
            resp2 = client.get(f"/api/math/{self.m2.number}")
            resp3 = client.get(f"/api/math/3")
            resp4 = client.get(f"/api/math/3.14")

            resp_list = [resp1.json, resp2.json, resp3.json, resp4.json]

            resp_random = client.get("/api/math/random")

            data = resp_random.json
            self.assertIn(data, resp_list)
            self.assertEqual(resp_random.status_code, 200)

    def test_get_random_math_fact_with_count(self):
        """Test GET route for math/random returns correct JSON response
        with a param count"""
        with app.test_client() as client:

            resp1 = client.get(f"/api/math/{self.m1.number}")
            resp2 = client.get(f"/api/math/{self.m2.number}")
            resp3 = client.get(f"/api/math/3")
            resp4 = client.get(f"/api/math/3.14")


            resp_list = [resp1.json["fact"],
                         resp2.json["fact"],
                         resp3.json["fact"],
                         resp4.json["fact"],
                         ]

            resp_random = client.get(f"/api/math/random?count=2")

            data = resp_random.json

            self.assertIn(data["facts"][0], resp_list)
            self.assertIn(data["facts"][1], resp_list)

            self.assertEqual(resp_random.status_code, 200)

    def test_get_random_math_fact_with_count_negative_error(self):
        """Test error if count param is negative for random math facts."""
        with self.client as c:

            resp = c.get("api/math/random?count=-100")
            self.assertEqual(
                resp.json,
                {"error": {
                    "status": 400,
                    "message": "-100 is an invalid count number",
                }})

            self.assertEqual(resp.status_code, 400)

    def test_error_get_year_fact_random_count_is_not_an_integer(self):
        """Test error if count param is not an integer for random math facts."""
        with self.client as c:

            resp = c.get("api/math/random?count=applepie")
            self.assertEqual(
                resp.json,
                {"error": {
                    "status": 400,
                    "message": "applepie is an invalid count number",
                }})

            self.assertEqual(resp.status_code, 400)

# class test_max_batch(MathRouteBaseTestCase):
#     @mock.patch('nums_api.config.MAX_BATCH', 2)
#     def test_max_batch_math(self):

#             MAX_BATCH = 2
#             assert 2 == MAX_BATCH
#             self.maxDiff = None
#             with app.test_client() as client:

#                 resp = client.get(f"/api/math/1..3")

#                 self.assertEqual(resp.json,
#                 {
#                     "facts":
#                     [
#                         {
#                             "number": "3",
#                             "fragment": "the number for this m3 test fact fragment",
#                             "statement": "3 is the number for m3 this test fact statement.",
#                             "type": "math"
#                         },
#                         {
#                             "number": "3.14",
#                             "fragment": "Ah pizza pai",
#                             "statement": "3.14 is the number of pi",
#                             "type": "math"
#                         }
#                     ]
#                 })

#                 self.assertEqual(resp.status_code, 200)


# class test_max_batch(MathRouteBaseTestCase):
#     @patch('nums_api.config.MAX_BATCH')
#     def test_max_batch_math(self, mock_MAX_BATCH):
#         mock_MAX_BATCH = 1
#         # nums_api.config.MAX_BATCH = 2

#         self.maxDiff = None

#         with app.test_client() as client:
#             # nums_api.maths.routes.MAX_BATCH = 1
#             # nums_api.maths.routes.MAX_BATCH
#             # nums_api.config.MAX_BATCH = 1

#             resp = client.get(f"/api/math/1..3")

#             self.assertEqual(resp.json,
#             {
#                 "facts":
#                 [
#                     {
#                         "number": "1",
#                         "fragment": "the number for this m1 test fact fragment",
#                         "statement": "1 is the number for m1 this test fact statement.",
#                         "type": "math"
#                     },
#                     {
#                         "number": "2",
#                         "fragment": "the number for this m2 test fact fragment",
#                         "statement": "2 is the number for m2 this test fact statement.",
#                         "type": "math"
#                     }
#                 ]
#             })

#             self.assertEqual(resp.status_code, 200)