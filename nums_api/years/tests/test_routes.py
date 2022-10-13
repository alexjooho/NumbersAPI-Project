from unittest import TestCase
from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from nums_api.years.models import Year
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1 per day", "1 per hour"],
    storage_uri="memory://",
)

db.drop_all()
db.create_all()

class YearRouteTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""

        self.client = app.test_client()

        Year.query.delete()

        self.y1 = Year(
            year=1,
            fact_fragment="the year for the first test entry",
            fact_statement="1 is the year for this test fact statement.",
            was_submitted=False
        )
        self.y2 = Year(
            year=2,
            fact_fragment="the year for the second test entry",
            fact_statement="2 is the year for this test fact statement.",
            was_submitted=False
        )
        self.y3 = Year(
            year=3,
            fact_fragment="the year for the third test entry",
            fact_statement="3 is the year for this test fact statement.",
            was_submitted=False
        )

        db.session.add_all([self.y1, self.y2, self.y3])
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

class SingleYearRouteTestCase(YearRouteTestCase):
    def test_get_year_fact(self):
        """Tests for getting a single fact by year.
        Get a single fact about the year 1"""
        with self.client as c:
            limiter.enabled = False
            resp = c.get("/api/years/1")
            self.assertEqual(
                resp.json,
                {"fact": {
                    "year": 1,
                    "fragment": "the year for the first test entry",
                    "statement": "1 is the year for this test fact statement.",
                    "type": "year",
                }})

            self.assertEqual(resp.status_code, 200)

    def test_error_for_year_without_fact(self):
        """Tests for getting an error for a year without a fact.
        """
        with self.client as c:
            limiter.enabled = False
            resp = c.get("api/years/100000")
            self.assertEqual(
                resp.json,
                {"error": {
                    "status": 404,
                    "message": "A fact for 100000 not found",
                }})

            self.assertEqual(resp.status_code, 404)

class MultipleYearsRangeRouteTestCase(YearRouteTestCase):
    def test_range_years_double_period_syntax(self):
        """Tests for getting a range of years with '..' works"""
        with self.client as c:
            limiter.enabled = False
            resp = c.get("api/years/1..3")

            self.assertEqual(resp.json, {'facts':
            [{'fragment': 'the year for the first test entry',
             'statement': '1 is the year for this test fact statement.',
             'type': 'year',
             'year': 1},
            {'fragment': 'the year for the second test entry',
             'statement': '2 is the year for this test fact statement.',
             'type': 'year',
             'year': 2},
            {'fragment': 'the year for the third test entry',
             'statement': '3 is the year for this test fact statement.',
             'type': 'year',
             'year': 3}]})
            self.assertEqual(resp.status_code, 200)

    def test_multiple_years_separated_by_commas(self):
        """Tests for getting a facts of multiple years seperated by comma works.
        """
        with self.client as c:
            limiter.enabled = False
            resp = c.get("api/years/1,3")

            self.assertEqual(resp.json, {'facts':
            [{'fragment': 'the year for the first test entry',
             'statement': '1 is the year for this test fact statement.',
             'type': 'year',
             'year': 1},
            {'fragment': 'the year for the third test entry',
             'statement': '3 is the year for this test fact statement.',
             'type': 'year',
             'year': 3}]})
            self.assertEqual(resp.status_code, 200)

    def test_multiple_years_with_all_syntax_combo(self):
        """Tests for getting facts of multiple years seperated by comma and '..'
        works.
        """
        with self.client as c:
            limiter.enabled = False
            resp = c.get("api/years/0..1,3..5")

            self.assertEqual(resp.json, {'facts':
            [{'fragment': 'the year for the first test entry',
             'statement': '1 is the year for this test fact statement.',
             'type': 'year',
             'year': 1},
            {'fragment': 'the year for the third test entry',
             'statement': '3 is the year for this test fact statement.',
             'type': 'year',
             'year': 3}]})
            self.assertEqual(resp.status_code, 200)

    def test_range_years_with_no_facts(self):
        """Tests for getting facts of multiple years with no facts found.
        """
        with self.client as c:
            limiter.enabled = False
            resp = c.get("api/years/5,6..10")

            self.assertEqual(resp.json, {"error": {
                    "status": 404,
                    "message": "No facts for 5,6..10 were found",
                }})
            self.assertEqual(resp.status_code, 404)

    def test_invalid_year_url_input(self):
        """Test for invalid URL input for a year."""
        with self.client as c:
            limiter.enabled = False
            resp = c.get("api/years/BLAH")
            self.assertEqual(
                resp.json,
                {"error": {
                    "status": 400,
                    "message": "Invalid URL",
                }})

            self.assertEqual(resp.status_code, 400)

class YearsRandomRouteTestCase(YearRouteTestCase):
    def test_get_year_fact_random(self):
        """Test for getting a single fact on a random year (default, no count
        param)."""
        with self.client as c:
            limiter.enabled = False
            y1_resp = c.get("api/years/1")
            y2_resp = c.get("api/years/2")
            y3_resp = c.get("api/years/3")

            resp_list = [y1_resp.json, y2_resp.json, y3_resp.json]

            random_resp = c.get("api/years/random")

            self.assertIn(random_resp.json, resp_list)
            self.assertEqual(random_resp.status_code, 200)

    def test_get_year_facts_random_count_is_defined(self):
        """Test for getting a count number of random year facts if count param
        is specified."""
        with self.client as c:
            limiter.enabled = False
            y1_resp = c.get("api/years/1")
            y2_resp = c.get("api/years/2")
            y3_resp = c.get("api/years/3")

            resp_list = [
                y1_resp.json["fact"],
                y2_resp.json["fact"],
                y3_resp.json["fact"]
                ]

            random_resp = c.get("api/years/random?count=2")
            resp = random_resp.json

            self.assertIn(resp["facts"][0], resp_list)
            self.assertIn(resp["facts"][1], resp_list)
            with self.assertRaises(IndexError) as exc:
                resp["facts"][2]
                self.assertEqual(str(exc.exception), "list index out of range")
                self.assertEqual(random_resp.status_code, 200)


    def test_get_year_fact_random_count_exceeds_max_total_facts(self):
        """Test for getting a count number that exceeds total number of random
        year facts."""
        with self.client as c:
            limiter.enabled = False
            y1_resp = c.get("api/years/1")
            y2_resp = c.get("api/years/2")
            y3_resp = c.get("api/years/3")

            resp_list = [
                y1_resp.json["fact"],
                y2_resp.json["fact"],
                y3_resp.json["fact"]
                ]

            random_resp = c.get("api/years/random?count=100")
            resp = random_resp.json

            self.assertIn(resp["facts"][0], resp_list)
            self.assertIn(resp["facts"][1], resp_list)
            self.assertIn(resp["facts"][2], resp_list)
            with self.assertRaises(IndexError) as exc:
                resp["facts"][3]
                self.assertEqual(str(exc.exception), "list index out of range")
            self.assertEqual(random_resp.status_code, 200)

    # tests route if count param exceeds max number:
    # unsuccesful in setting MAX_BATCH in testing environment to lower number (2)
    #
    # def test_get_year_fact_random_count_exceeds_max_batch(self):
    #     """Test for getting a count number that exceeds MAX_BATCH."""
    #     with self.client as c:

    #         y1_resp = c.get("api/years/1")
    #         y2_resp = c.get("api/years/2")
    #         y3_resp = c.get("api/years/3")

    #         resp_list = [
    #             y1_resp.json["fact"],
    #             y2_resp.json["fact"],
    #             y3_resp.json["fact"]
    #             ]

    #         random_resp = c.get("api/years/random?count=100")
    #         resp = random_resp.json

    #         self.assertIn(resp["facts"][0], resp_list)
    #         self.assertIn(resp["facts"][1], resp_list)
    #         self.assertIn(resp["facts"][2], resp_list)
    #         with self.assertRaises(IndexError) as exc:
    #             resp["facts"][3]
    #             self.assertEqual(str(exc.exception), "list index out of range")
    #         self.assertEqual(random_resp.status_code, 200)

    def test_error_get_year_fact_random_count_is_negative(self):
        """Test error if count param is negative for random year facts."""
        with self.client as c:
            limiter.enabled = False
            resp = c.get("api/years/random?count=-100")
            self.assertEqual(
                resp.json,
                {"error": {
                    "status": 400,
                    "message": "-100 is an invalid count number",
                }})

            self.assertEqual(resp.status_code, 400)

    def test_error_get_year_fact_random_count_is_not_an_integer(self):
        """Test error if count param is not an integer for random year facts."""
        with self.client as c:
            limiter.enabled = False
            resp = c.get("api/years/random?count=applepie")
            self.assertEqual(
                resp.json,
                {"error": {
                    "status": 400,
                    "message": "applepie is an invalid count number",
                }})

            self.assertEqual(resp.status_code, 400)

class YearRouteTestCaseWithLimiter(YearRouteTestCase):
    def test_get_year_fact_with_limiter(self):
        """Tests limiter for get year fact route"""
        with self.client as c:
            limiter.enabled = True
            resp1 = c.get("/api/years/1")
            resp2 = c.get("/api/years/2")

            self.assertEqual(resp2.status_code, 429)

    def test_range_years_with_limiter(self):
        """Tests limiter for get range year facts route"""
        with self.client as c:
            limiter.enabled = True
            resp1 = c.get("api/years/1..3")
            resp2 = c.get("api/years/1..2")

            self.assertEqual(resp2.status_code, 429)

    def test_random_years_with_limiter(self):
        """Tests limiter for get random year fact route"""
        with self.client as c:
            limiter.enabled = True
            resp1 = c.get("api/years/random")
            resp2 = c.get("api/years/random")

            self.assertEqual(resp2.status_code, 429)