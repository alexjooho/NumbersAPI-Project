from unittest import TestCase
from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from nums_api.tracking.models import Tracking

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.drop_all()
db.create_all()

class YearRouteTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""
        Tracking.query.delete()

        self.track1 = Tracking(
            req_item = "test_item",
            category = "test_cat",
            num_reqs = 1
        )

        db.session.add(self.track1)
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)
        
    def test_update_existing_row(self):
        """Test the existing row is found and updates correctly."""
        
        Tracking.update_request_count("test_item", "test_cat")
        self.assertEqual(Tracking.query.count(), 1)
        
        test1 = Tracking.query.get(("test_item", "test_cat"))
        self.assertEqual(test1.num_reqs, 2)
        
    def test_create_new_row(self):
        """Test an unfound requests is added to table."""
        
        self.assertEqual(Tracking.query.count(), 1)
        Tracking.update_request_count("test_item2","test_cat2")
        self.assertEqual(Tracking.query.count(), 2)
        
        test2 = Tracking.query.get(("test_item2", "test_cat2"))
        self.assertEqual(test2.num_reqs, 1)
        
    def test_multiple_items_with_same_name_or_category(self):
        """Test that items with same name/category but different
        category/name can exist harmonously."""
        
        self.assertEqual(Tracking.query.count(), 1)
        
        Tracking.update_request_count("test_item","test_cat2")
        self.assertEqual(Tracking.query.count(), 2)
        
        Tracking.update_request_count("test_item2","test_cat")
        self.assertEqual(Tracking.query.count(), 3)
        
    def test_req_item_as_a_number_adds_correctly(self):
        """Test adding a request item input as a number"""
        
        self.assertEqual(Tracking.query.count(), 1)
        
        Tracking.update_request_count(1,"test_cat")
        self.assertEqual(Tracking.query.count(), 2)
        
        test = Tracking.query.get(("1", "test_cat"))
        self.assertEqual(test.num_reqs, 1)