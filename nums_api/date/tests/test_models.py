from unittest import TestCase
from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from nums_api.date.models import Date

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.drop_all()
db.create_all()


class DateModelTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""

        Date.query.delete()

        self.d1 = Date(
            day_of_year = 1,
            year = 1,
            fact_fragment = "the date of d1 fact fragment",
            fact_statement = "1/1/1 is the date of d1 fact statement",
            was_submitted = True
        )

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)
        
    def test_model(self):
        self.assertIsInstance(self.d1, Date)
        self.assertEqual(Date.query.count(), 0)
        
        db.session.add(self.d1)
        db.session.commit()
        
        self.assertEqual(Date.query.count(), 1)
        self.assertEqual(Date.query.filter_by(day_of_year=1).one().year, 1)