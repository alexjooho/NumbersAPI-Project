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

class DateModelTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""
        
        Date.query.delete()

        self.d1 = Date(
            day_of_year=1,
            year=1,
            fact_fragment="the date of d1 fact fragment",
            fact_statement="January 1st is the date of d1 fact statement",
            was_submitted=False
        )

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

    def test_model(self):
        """Test creating a new Date instance and adding it to the database"""
        self.assertIsInstance(self.d1, Date)
        self.assertEqual(Date.query.count(), 0)

        db.session.add(self.d1)
        db.session.commit()

        self.assertEqual(Date.query.count(), 1)
        self.assertEqual(Date.query.filter_by(day_of_year=1).one().year, 1)

    def test_invalid_inputs(self):
        """Test invalid day/month inputs raise errors"""
        # Good month, bad day
        with self.assertRaises(ValueError) as exc:
            Date.date_to_day_of_year(1, 0)
        self.assertEqual(str(exc.exception), "Invalid value for day")
        with self.assertRaises(ValueError) as exc:
            Date.date_to_day_of_year(2, 30)
        self.assertEqual(str(exc.exception), "Invalid value for day")
        
        # Bad month, good day
        with self.assertRaises(ValueError) as exc:
            Date.date_to_day_of_year(0, 1)
        self.assertEqual(str(exc.exception), "Invalid value for month")
        with self.assertRaises(ValueError) as exc:
            Date.date_to_day_of_year(13, 1)
        self.assertEqual(str(exc.exception), "Invalid value for month")

class DateLikeModelTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""
        
        DateLike.query.delete()
        Date.query.delete()

        self.d1 = Date(
            day_of_year=1,
            year=1,
            fact_fragment="the date of d1 fact fragment",
            fact_statement="January 1st is the date of d1 fact statement",
            was_submitted=False
        )
        
        db.session.add(self.d1)
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)
        
    def test_datelike_model(self):
        """Test creating a new DateLike instance and adding it to the database"""

        self.assertEqual(DateLike.query.count(), 0)

        self.date_to_like = Date.query.filter_by(day_of_year=1).one()
        
        self.new_datelike = DateLike(
            fact_id = self.date_to_like.id
        )
        
        db.session.add(self.new_datelike)
        db.session.commit()
        
        self.assertEqual(DateLike.query.count(), 1)
        self.assertEqual(DateLike.query.filter_by(fact_id=self.date_to_like.id).one().category, "date")

