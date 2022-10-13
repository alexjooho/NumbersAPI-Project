from unittest import TestCase
from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from nums_api.maths.models import Math, MathLike

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

        MathLike.query.delete()
        Math.query.delete()

        self.m1 = Math(
            number=1,
            fact_fragment="the number for this m1 test fact fragment",
            fact_statement="1 is the number for m1 test fact statement.",
            was_submitted=False
        )

        self.m2 = Math(
            number=2,
            fact_fragment="the number for this m2 test fact fragment",
            fact_statement="2 is the number for m2 test fact statement.",
            was_submitted=False
        )

        self.m3 = Math(
            number=3,
            fact_fragment="the number for this m3 test fact fragment",
            fact_statement="3 is the number for m3 test fact statement.",
            was_submitted=False
        )

        self.m4 = Math(
            number=3.14,
            fact_fragment="the number for this m4 test fact fragment",
            fact_statement="3.14 is the number for m4 test fact statement.",
            was_submitted=False
        )

        db.session.add_all([self.m1, self.m2, self.m3, self.m4])

        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)


class SingleMathRouteTestCase(MathRouteBaseTestCase):
    def test_get_math_fact(self):
        """Test GET route for math/number returns correct JSON response"""
        with app.test_client() as client:
            url = f"/api/math/{self.m1.number}"
            resp = client.get(url)

            data = resp.json
            self.assertEqual(data, {"fact": {
                "number": "1",
                "fragment": "the number for this m1 test fact fragment",
                "statement": "1 is the number for m1 test fact statement.",
                "type": "math"
            }})
            self.assertEqual(resp.status_code, 200)

    def test_error_for_number_with_no_fact(self):
        """Test GET route for math/number returns 404 if number not found"""
        with app.test_client() as client:
            url = "/api/math/0"
            resp = client.get(url)

            data = resp.json
            self.assertEqual(data, {'error': {
                'message': "A math fact for 0 not found",
                'status': 404}})
            self.assertEqual(resp.status_code, 404)

    def test_error_for_invalid_number(self):
        """Test GET route for math/number returns 404 if number not valid"""
        with app.test_client() as client:
            url = "/api/math/minaj"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 400)


class MathRouteGetBatchMathFact(MathRouteBaseTestCase):
    def test_get_batch_math_fact(self):
        """Test GET route for batch math with '..' returns correct JSON response"""
        with app.test_client() as client:
            resp = client.get("/api/math/1..2")

            self.assertEqual(resp.json,
                             {
                                 "facts":
                                 [
                                     {
                                         "number": "1",
                                         "fragment": "the number for this m1 test fact fragment",
                                         "statement": "1 is the number for m1 test fact statement.",
                                         "type": "math"
                                     },
                                     {
                                         "number": "2",
                                         "fragment": "the number for this m2 test fact fragment",
                                         "statement": "2 is the number for m2 test fact statement.",
                                         "type": "math"
                                     }
                                 ]
                             })

            self.assertEqual(resp.status_code, 200)

    def test_get_batch_math_separated_by_commas(self):
        """Tests for getting math facts for numbers seperated
        by comma works.
        """
        with self.client as c:
            resp = c.get("/api/math/1,2")

            self.assertEqual(resp.json,
                             {
                                 "facts":
                                 [
                                     {
                                         "number": "1",
                                         "fragment": "the number for this m1 test fact fragment",
                                         "statement": "1 is the number for m1 test fact statement.",
                                         "type": "math"
                                     },
                                     {
                                         "number": "2",
                                         "fragment": "the number for this m2 test fact fragment",
                                         "statement": "2 is the number for m2 test fact statement.",
                                         "type": "math"
                                     },
                                 ]
                             })

            self.assertEqual(resp.status_code, 200)

    def test_multiple_numbers_with_all_syntax_combo(self):
        """Tests for getting a facts for multiple numbers seperated by comma or by '..'
        """
        with self.client as c:

            resp = c.get("api/math/1..2,3.14")

            self.assertEqual(resp.json, {
                "facts":
                [
                    {
                        "number": "1",
                        "fragment": "the number for this m1 test fact fragment",
                        "statement": "1 is the number for m1 test fact statement.",
                        "type": "math"
                    },
                    {
                        "number": "2",
                        "fragment": "the number for this m2 test fact fragment",
                        "statement": "2 is the number for m2 test fact statement.",
                        "type": "math"
                    },
                    {
                        "number": "3.14",
                        "fragment": "the number for this m4 test fact fragment",
                        "statement": "3.14 is the number for m4 test fact statement.",
                        "type": "math"
                    }
                ]
            })
            self.assertEqual(resp.status_code, 200)

    def test_get_batch_math_fact_with_decimal(self):
        """Test getting a math fact with decimal"""

        with app.test_client() as client:

            resp = client.get("/api/math/3..3.14")

            self.assertEqual(resp.json,
                             {
                                 "facts":
                                 [
                                     {
                                         "number": "3",
                                         "fragment": "the number for this m3 test fact fragment",
                                         "statement": "3 is the number for m3 test fact statement.",
                                         "type": "math"
                                     },
                                     {
                                         "number": "3.14",
                                         "fragment": "the number for this m4 test fact fragment",
                                         "statement": "3.14 is the number for m4 test fact statement.",
                                         "type": "math"
                                     }
                                 ]
                             })

            self.assertEqual(resp.status_code, 200)

    def test_get_batch_math_fact_error(self):
        """Test error handling for batch math facts"""

        with self.client as c:
            resp = c.get("/api/math/TEST..TEST")

            self.assertEqual(resp.json, {
                "error": {
                    "message": "Invalid URL",
                    "status": 400}
            })
            self.assertEqual(resp.status_code, 400)

    def test_range_math_with_no_facts(self):
        """Tests for getting multiple math facts separated by comma
        where there are no facts available."""
        with self.client as c:

            resp = c.get("api/math/5,6,7")

            self.assertEqual(resp.json, {"error": {
                "status": 404,
                "message": "No facts for 5,6,7 were found",
            }})
            self.assertEqual(resp.status_code, 404)

    def test_invalid_math_url_input(self):
        """Test for invalid URL input for a number."""
        with self.client as c:

            resp = c.get("api/math/TEST")
            self.assertEqual(
                resp.json,
                {"error": {
                    "status": 400,
                    "message": "Invalid URL",
                }})

            self.assertEqual(resp.status_code, 400)


class MathRouteRandomTestCase(MathRouteBaseTestCase):
    
    
    def test_get_random_math_fact(self):
        """Test GET route for math/random returns correct JSON response"""
        with app.test_client() as client:

            resp1 = client.get("/api/math/1")
            resp2 = client.get("/api/math/2")
            resp3 = client.get("/api/math/3")
            resp4 = client.get("/api/math/3.14")

            resp_list = [resp1.json, resp2.json, resp3.json, resp4.json]

            resp_random = client.get("/api/math/random")

            data = resp_random.json
            self.assertIn(data, resp_list)
            self.assertEqual(resp_random.status_code, 200)

    def test_get_random_math_fact_with_count(self):
        """Test GET route for math/random returns correct JSON response"""
        with app.test_client() as client:

            resp1 = client.get("/api/math/1")
            resp2 = client.get("/api/math/2")
            resp3 = client.get("/api/math/3")
            resp4 = client.get("/api/math/3.14")

            resp_list = [resp1.json["fact"],
                         resp2.json["fact"],
                         resp3.json["fact"],
                         resp4.json["fact"],
                         ]

            resp_random = client.get("/api/math/random?count=2")

            data = resp_random.json
            self.assertIn(data["facts"][0], resp_list)
            self.assertIn(data["facts"][1], resp_list)
            self.assertIs(len(data["facts"]), 2)

            self.assertEqual(resp_random.status_code, 200)

    #test_get_math_fact_random_count_exceeds_max(self) does not work without
    # mocked MAX_BATCH variable

    # def test_get_math_fact_random_count_exceeds_max(self):
    #     """Test for getting a count number that exceeds total number of random
    #     number facts."""
    #     with self.client as c:

    #         t1_resp = c.get("api/math/1")
    #         t2_resp = c.get("api/math/2")
    #         t3_resp = c.get("api/math/3")
    #         t4_resp = c.get("api/math/3.14")


    #         resp_list = [
    #             t1_resp.json["fact"],
    #             t2_resp.json["fact"],
    #             t3_resp.json["fact"],
    #             t4_resp.json["fact"],
    #         ]

    #         random_resp = c.get("api/math/random?count=100")
    #         resp = random_resp.json


    #         self.assertIn(resp["facts"][0], resp_list)
    #         self.assertIn(resp["facts"][1], resp_list)
    #         self.assertIn(resp["facts"][2], resp_list)
    #         self.assertIn(resp["facts"][3], resp_list)

    #         with self.assertRaises(IndexError) as exc:
    #             resp["facts"][4]
    #             self.assertEqual(str(exc.exception), "list index out of range")
    #         self.assertEqual(random_resp.status_code, 200)

    def test_error_get_math_fact_random_count_is_negative(self):
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

    def test_error_get_math_fact_random_count_is_not_an_integer(self):
        """Test error if count param is not an integer for random math facts."""
        with self.client as c:

            resp = c.get("api/math/random?count=TEST")
            self.assertEqual(
                resp.json,
                {"error": {
                    "status": 400,
                    "message": "TEST is an invalid count number",
                }})

            self.assertEqual(resp.status_code, 400)



class MathRoutePostLikeTestCase(MathRouteBaseTestCase):          
    def test_success_post_math_fact_like(self):
        """Test successful POST request to like a fact"""
        with app.test_client() as c:
            
            resp = c.post("/api/math/like", 
                            json={"fact": {
                                    "number": 3.14,
                                    "statement": "3.14 is the number for m4 test fact statement."
                                }})

            self.assertEqual(resp.json, {"status": "success"})
            self.assertEqual(resp.status_code, 201)
            
    def test_failure_post_math_bad_number(self):
        """Test POST failure when bad number provided."""
        with app.test_client() as c:
            
            resp =  c.post("/api/math/like", 
                            json={"fact": {
                                    "number": "BADNUMBER",
                                    "statement": "3.14 is the number for m4 test fact statement."
                                }})

            self.assertEqual(resp.json, 
                    {
                        "error": {
                            "message": "Invalid number",
                            "status": 400
                        }
                    })
            self.assertEqual(resp.status_code, 400)
        
    def test_failure_post_math_no_fact_statement(self):
        """Test POST failure when no fact statement is provided."""
        with app.test_client() as c:
            
            resp = c.post("/api/math/like", 
                            json={"fact": {
                                    "number": 3.14,
                                }})


            self.assertEqual(resp.json, 
                    {
                        "error": {
                            "message": "Please provide a fact statement",
                            "status": 400
                        }
                    })
            self.assertEqual(resp.status_code, 400)

    def test_failure_post_math_bad_fact_statement(self):
        """Test POST failure when number does not match existing fact statement."""
        with app.test_client() as c:
            
            resp = c.post("/api/math/like", 
                            json={"fact": {
                                    "number": 3.14,
                                    "statement": "MISMATCHED STATEMENT"
                                }})
            self.assertEqual(resp.json, 
                {
                    "error": {
                        "message": "No matching fact found for 3.14.",
                        "status": 400
                    }
                })
            self.assertEqual(resp.status_code, 400)
            