from unittest import TestCase
from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from nums_api.dates.models import Date
from nums_api.maths.models import Math
from nums_api.trivia.models import Trivia
from nums_api.years.models import Year


app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.drop_all()
db.create_all()

class SearchRouteTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""
        self.client = app.test_client()
        
        Trivia.query.delete()
        Math.query.delete()
        Date.query.delete()
        Year.query.delete()

        self.m1 = Math(
            number=1,
            fact_fragment="test math",
            fact_statement="test Apple.",
            was_submitted=False
        )

        self.t1 = Trivia(
            number=2,
            fact_fragment="test trivia",
            fact_statement="test Banana.",
            was_submitted=False
        )

        self.d1 = Date(
            day_of_year=3,
            year=1,
            fact_fragment="test date",
            fact_statement="test Carrot.",
            was_submitted=False
        )
        
        self.y1 = Year(
            year=1,
            fact_fragment="test year",
            fact_statement="test Durian.",
            was_submitted=False
        )

        db.session.add_all([self.t1, self.m1, self.y1, self.d1])
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)
        
class TestSearchFunctionality(SearchRouteTestCase):
    def test_get_all_results(self):
        """Test GET route for search returns all search terms with a common word"""
        with self.client as c:
            url = "/api/search/?query=test"
            resp = c.get(url)
            data = resp.json
            
            self.assertEqual(data, {"results": {
                "dates" : [{"statement": "test Carrot.", "type": "date"}],
                "math" : [{"statement": "test Apple.", "type": "math"}],
                "trivia" : [{"statement": "test Banana.", "type": "trivia"}],
                "years" : [{"statement": "test Durian.", "type": "years"}],
                }})
                
            self.assertEqual(resp.status_code, 200)
            
    def test_get_unique_results(self):
        """Test GET route for search returns only results with word"""
        with self.client as c:
            url = "/api/search/?query=apple"
            resp = c.get(url)
            data = resp.json
            
            self.assertEqual(data, {"results": {
                "dates" : [],
                "math" : [{"statement": "test Apple.", "type": "math"}],
                "trivia" : [],
                "years" : [],
                }})
                
            self.assertEqual(resp.status_code, 200)