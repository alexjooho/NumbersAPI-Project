from unittest import TestCase
from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from nums_api.dates.models import Date
from nums_api.years.models import Year
from nums_api.tracking.models import Tracking

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.drop_all()
db.create_all()

class TrackingAfterRequestTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""
        self.client = app.test_client()

        Tracking.query.delete()

        self.y1 = Year(
            year=1,
            fact_fragment="the year for the first test entry",
            fact_statement="1 is the year for this test fact statement.",
            was_submitted=False
        )
        self.d1 = Date(
            day_of_year=61,
            year=1999,
            fact_fragment="the date for the second test entry",
            fact_statement="3/1/1999 is the date for this test fact statement.",
            was_submitted=False
        )

        db.session.add_all([self.y1,self.d1])
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)


    def test_tracking_updates_on_successful_request(self):
        """Tests for updating tracker count on successful single fact request."""
        with self.client as c:
            
            test = Tracking.query.get(("1", "years"))
            self.assertEqual(test, None)
            
            resp = c.get("/api/years/1")
            self.assertEqual(resp.status_code, 200)  
            
            test = Tracking.query.get(("1", "years"))
            self.assertEqual(test.num_reqs, 1)
            
    def test_tracking_updates_on_successful_dates_request(self):
        """Tests for updating tracker count on successful date single fact request."""
        with self.client as c:
            
            test = Tracking.query.get(("61", "dates"))
            self.assertEqual(test, None)
            
            resp = c.get("/api/dates/3/1")
            self.assertEqual(resp.status_code, 200)  
            
            test = Tracking.query.get(("61", "dates"))
            self.assertEqual(test.num_reqs, 1)

    def test_tracking_updates_on_good_route_but_missing_fact(self):
        with self.client as c:
            
            test = Tracking.query.get(("2", "years"))
            self.assertEqual(test, None)
            
            resp = c.get("/api/years/2")
            self.assertEqual(resp.status_code, 404)  
            
            test = Tracking.query.get(("2", "years"))
            self.assertEqual(test.num_reqs, 1)


    def test_tracking_does_not_update_on_bad_route(self):
        with self.client as c:
            
            test = Tracking.query.get(("BADREQUEST", "math"))
            self.assertEqual(test, None)
            
            resp = c.get("/api/math/BADREQUST")
            self.assertEqual(resp.status_code, 404)  
            
            test = Tracking.query.get(("BADREQUEST", "math"))
            self.assertEqual(test, None)

    def test_tracking_does_not_update_on_random_request(self):
        with self.client as c:
            
            test = Tracking.query.count()
            self.assertEqual(test, 0)
            
            resp = c.get("/api/years/random")
            self.assertEqual(resp.status_code, 200)  
            
            test = Tracking.query.count()
            self.assertEqual(test, 0)