from unittest import TestCase
from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from nums_api.years.models import Year

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.drop_all()
db.create_all()

class YearRouteTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""
        self.client = app.test_client()
        
        Year.query.delete()
        
        y1 = Year(
            year=1,
            fact_fragment="the year for the first test entry",
            fact_statement="First test for year 1",
            was_submitted=False
        )
        y2 = Year(
            year=2,
            fact_fragment="the year for the second test entry",
            fact_statement="2 is the year for this test fact statement.",
            was_submitted=False
        )
        y3 = Year(
            year=1,
            fact_fragment="the year for the third test entry",
            fact_statement="Another test for year 1.",
            was_submitted=False
        )

        db.session.add_all([y1,y2,y3])
        db.session.commit()
        
        self.y1_yr = y1.year
        self.y2_yr = y2.year
        self.y3_yr = y3.year
        

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)
    
    def test_single_fact_route(self):
        """Tests for getting a single fact by year."""
        with self.client as c:
    
            resp = c.get("/api/years/1")
            self.assertEqual(resp.status_code, 200)
            print('response object', resp)
            # self.assertIn("year 1", resp)

            #Test failure on non-existant year:
            # resp = c.get("/years/100000")
            
            # self.assertEqual(resp.status_code, 404)
            # self.assertIn("not found", resp.error)
            