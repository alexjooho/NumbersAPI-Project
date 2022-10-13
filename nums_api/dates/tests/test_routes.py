from unittest import TestCase
from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from nums_api.dates.models import Date, DateLike

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

        DateLike.query.delete()
        Date.query.delete()

        self.d1 = Date(
            day_of_year=10,
            year=1900,
            fact_fragment='t1 fragment',
            fact_statement='t1 statement',
            was_submitted=False
        )

        self.d2 = Date(
            day_of_year=50,
            year=1900,
            fact_fragment='t2 fragment',
            fact_statement='t2 statement',
            was_submitted=False
        )

        self.d3 = Date(
            day_of_year=51,
            year=1901,
            fact_fragment='t3 fragment',
            fact_statement='t3 statement',
            was_submitted=False
        )

        self.d4 = Date(
            day_of_year=20,
            year=1902,
            fact_fragment='t4 fragment',
            fact_statement='t4 statement',
            was_submitted=False
        )

        db.session.add_all([self.d1, self.d2, self.d3, self.d4])
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
                    'fragment': 't1 fragment',
                    'statement': 't1 statement',
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


class DatesRangeRouteSpecificDateTestCase(DateRouteBaseTestCase):
    def test_get_dates_range_facts(self):
        """Test GET route for range of dates/month/day separated by ".." works
        and returns correct JSON response"""
        with app.test_client() as c:
            resp = c.get('/api/dates/1/10..2/19')

            self.assertEqual(resp.json,
                             {"facts": [{
                                 "number": 10,
                                 "year": 1900,
                                 "fragment": "t1 fragment",
                                 "statement": "t1 statement",
                                 "type": "date"
                             },
                                 {
                                 "number": 20,
                                 "year": 1902,
                                 "fragment": "t4 fragment",
                                 "statement": "t4 statement",
                                 "type": "date"
                             },
                                 {
                                 "number": 50,
                                 "year": 1900,
                                 "fragment": "t2 fragment",
                                 "statement": "t2 statement",
                                 "type": "date"
                             }]
                             })

            self.assertEqual(resp.status_code, 200)

    def test_get_dates_range_facts_with_commas(self):
        """Test GET route for range of dates/month/day separated by commas works
        and returns correct JSON response"""
        with app.test_client() as c:
            resp = c.get('/api/dates/1/10,1/20')

            self.assertEqual(resp.json,
                             {"facts": [{
                                 "number": 10,
                                 "year": 1900,
                                 "fragment": "t1 fragment",
                                 "statement": "t1 statement",
                                 "type": "date"
                             },
                                 {
                                 "number": 20,
                                 "year": 1902,
                                 "fragment": "t4 fragment",
                                 "statement": "t4 statement",
                                 "type": "date"
                             }
                             ]})

            self.assertEqual(resp.status_code, 200)

    def test_error_range_dates_with_no_facts(self):
        """Test GET route error msg if no facts were found for range of dates"""
        with app.test_client() as c:

            resp = c.get("api/dates/3/1..4/15")

            self.assertEqual(resp.json, {"error": {
                "status": 404,
                "message": "No facts for 3/1..4/15 were found",
            }})
            self.assertEqual(resp.status_code, 404)

    def test_error_range_dates_regex_doesnt_match(self):
        """Test for getting a facts of multiple dates with invalid regex."""
        with app.test_client() as c:

            resp = c.get("api/dates/applepie")

            self.assertEqual(resp.json, {"error": {
                "status": 400,
                "message": 'Invalid URL',
            }})
            self.assertEqual(resp.status_code, 400)

    def test_error_range_dates_out_of_bound(self):
        """Test for getting facts of multiple dates with out of bound dates.
        """
        with app.test_client() as c:

            resp = c.get("api/dates/13/31,1/10")

            self.assertEqual(resp.json, {"error": {
                "status": 400,
                "message": 'Invalid date: 13/31',
            }})
            self.assertEqual(resp.status_code, 400)


class DateRouteRandomDateTestCase(DateRouteBaseTestCase):
    def test_get_random_date_fact(self):
        """Test GET route for dates/random returns correct JSON response"""
        with app.test_client() as c:

            resp1 = c.get('/api/dates/1/10')  # this is test1 input month/day
            resp2 = c.get('/api/dates/2/19')  # this is test2 input month/day
            resp3 = c.get('/api/dates/2/20')  # this is test3 input month/day
            resp4 = c.get('/api/dates/1/20')  # this is test4 input month/day
            resp_list = [resp1.json, resp2.json, resp3.json, resp4.json]

            resp_random = c.get('/api/dates/random')

            data = resp_random.json

            self.assertIn(data, resp_list)

            self.assertEqual(resp_random.status_code, 200)

    def test_get_random_date_facts_count_is_defined(self):
        """Test GET route for dates/random if count param is specified,
        and returns correct JSON response"""
        with app.test_client() as c:

            resp1 = c.get('/api/dates/1/10')  # this is test1 input month/day
            resp2 = c.get('/api/dates/2/19')  # this is test2 input month/day
            resp3 = c.get('/api/dates/2/20')  # this is test3 input month/day
            resp4 = c.get('/api/dates/1/20')  # this is test4 input month/day
            resp_list = [resp1.json["fact"], resp2.json["fact"],
                        resp3.json["fact"], resp4.json["fact"]]

            resp_random = c.get('/api/dates/random?count=2')
            resp = resp_random.json

            self.assertIn(resp["facts"][0], resp_list)
            self.assertIn(resp["facts"][1], resp_list)
            with self.assertRaises(IndexError) as exc:
                resp["facts"][2]
                self.assertEqual(str(exc.exception), "list index out of range")

            self.assertEqual(resp_random.status_code, 200)

    def test_get_random_date_facts_count_exceeds_max_total_facts(self):
        """Test GET route for dates/random if count param exceeds total number
        of dates facts"""
        with app.test_client() as c:

            resp1 = c.get('/api/dates/1/10')  # this is test1 input month/day
            resp2 = c.get('/api/dates/2/19')  # this is test2 input month/day
            resp3 = c.get('/api/dates/2/20')  # this is test3 input month/day
            resp4 = c.get('/api/dates/1/20')  # this is test4 input month/day
            resp_list = [resp1.json["fact"], resp2.json["fact"],
                        resp3.json["fact"], resp4.json["fact"]]

            resp_random = c.get('/api/dates/random?count=60')
            resp = resp_random.json

            self.assertIn(resp["facts"][0], resp_list)
            self.assertIn(resp["facts"][1], resp_list)
            self.assertIn(resp["facts"][2], resp_list)
            self.assertIn(resp["facts"][3], resp_list)
            with self.assertRaises(IndexError) as exc:
                resp["facts"][4]
                self.assertEqual(str(exc.exception), "list index out of range")

            self.assertEqual(resp_random.status_code, 200)

    # tests route if count param exceeds max number:
    # unsuccesful in setting MAX_BATCH in testing environment to lower number (2)
    #
    # def test_get_random_date_facts_count_exceeds_max_batch(self):
    #     """Test GET route for dates/random if count param exceeds MAX_BATCH."""
    #     with app.test_client() as c:

    #         resp1 = c.get('/api/dates/1/10')  # this is test1 input month/day
    #         resp2 = c.get('/api/dates/2/19')  # this is test2 input month/day
    #         resp3 = c.get('/api/dates/2/20')  # this is test3 input month/day
    #         resp4 = c.get('/api/dates/1/20')  # this is test4 input month/day
    #         resp_list = [resp1.json["fact"], resp2.json["fact"],
    #                     resp3.json["fact"], resp4.json["fact"]]

    #         resp_random = c.get('/api/dates/random?count=60')
    #         resp = resp_random.json

    #         self.assertIn(resp["facts"][0], resp_list)
    #         self.assertIn(resp["facts"][1], resp_list)
    #         self.assertIn(resp["facts"][2], resp_list)
    #         self.assertIn(resp["facts"][3], resp_list)
    #         with self.assertRaises(IndexError) as exc:
    #             resp["facts"][4]
    #             self.assertEqual(str(exc.exception), "list index out of range")

    #         self.assertEqual(resp_random.status_code, 200)

    def test_get_random_date_facts_count_is_negative(self):
        """Test GET route for dates/random if count param is a negative number"""
        with app.test_client() as c:

            resp_random = c.get('/api/dates/random?count=-60')
            resp = resp_random.json

            self.assertEqual(
                resp,
                {"error": {
                    "status": 400,
                    "message": "-60 is an invalid count number",
                }})

            self.assertEqual(resp_random.status_code, 400)

    def test_get_random_date_facts_count_is_not_an_integer(self):
        """Test GET route for dates/random if count param is a not an integer"""
        with app.test_client() as c:

            resp_random = c.get('/api/dates/random?count=applepie')
            resp = resp_random.json

            self.assertEqual(
                resp,
                {"error": {
                    "status": 400,
                    "message": "applepie is an invalid count number",
                }})

            self.assertEqual(resp_random.status_code, 400)


class DateRoutePostLikeTestCase(DateRouteBaseTestCase):          
    def test_success_post_date_fact_like(self):
        """Test successful POST request to like a fact"""
        with app.test_client() as c:
            
            resp = c.post("/api/dates/like", 
                            json={"fact": {
                                    "number": 10,
                                    "year": 1900,
                                    "statement": "t1 statement"
                                }})

            self.assertEqual(resp.json, {"status": "success"})
            self.assertEqual(resp.status_code, 201)
            
    def test_failure_post_date_bad_date_number(self):
        """Test successful POST request to like a fact"""
        with app.test_client() as c:
            
            resp = c.post("/api/dates/like", 
                            json={"fact": {
                                    "number": "BAD_NUMBER",
                                    "year": 1900,
                                    "statement": "t1 statement"
                                }})

            self.assertEqual(resp.json, 
                {
                    "error": {
                        "message": "Invalid number for date or year. Please format as whole number.",
                        "status": 400
                    }
                })
            self.assertEqual(resp.status_code, 400)
        
    def test_failure_post_date_no_fact_statement(self):
        """Test successful POST request to like a fact"""
        with app.test_client() as c:
            
            resp = c.post("/api/dates/like", 
                            json={"fact": {
                                    "number": 10,
                                    "year": 1900,
                                }})

            self.assertEqual(resp.json, 
                {
                    "error": {
                        "message": "Please provide a fact statement.",
                        "status": 400
                    }
                })
            self.assertEqual(resp.status_code, 400)
            
    def test_failure_post_date_num_too_large(self):
        """Test successful POST request to like a fact"""
        with app.test_client() as c:
            
            resp = c.post("/api/dates/like", 
                            json={"fact": {
                                    "number": 400,
                                    "year": 1900,
                                    "statement": "t1 statement"
                                }})

            self.assertEqual(resp.json, 
                {
                    "error": {
                        "message": "Date number must be less than 366.",
                        "status": 400
                    }
                })
            self.assertEqual(resp.status_code, 400)
            
    def test_failure_post_date_bad_fact_statement(self):
        """Test successful POST request to like a fact"""
        with app.test_client() as c:
            
            resp = c.post("/api/dates/like", 
                            json={"fact": {
                                    "number": 10,
                                    "year": 1900,
                                    "statement": "MISMATCHED STATEMENT"
                                }})

            self.assertEqual(resp.json, 
                {
                    "error": {
                        "message": "No matching fact found for day 10 in year 1900.",
                        "status": 400
                    }
                })
            self.assertEqual(resp.status_code, 400)
            