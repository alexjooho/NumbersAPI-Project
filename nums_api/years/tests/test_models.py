from unittest import TestCase
from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from nums_api.years.models import Year, YearLike

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.drop_all()
db.create_all()

class YearModelTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""
        
        YearLike.query.delete()
        Year.query.delete()

        self.y1 = Year(
            year=1,
            fact_fragment="the year for this test fact fragment",
            fact_statement="1 is the year for this test fact statement.",
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
        self.assertIsInstance(self.y1, Year)
        self.assertEqual(Year.query.count(), 0)

        db.session.add(self.y1)
        db.session.commit()

        self.assertEqual(Year.query.count(), 1)
        self.assertEqual(Year.query.filter_by(year=1).one().year, 1)


class YearLikeModelTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""
        
        YearLike.query.delete()
        Year.query.delete()
        
        self.y1 = Year(
            year=1,
            fact_fragment="the year for this test fact fragment",
            fact_statement="1 is the year for this test fact statement.",
            was_submitted=False
        )

        db.session.add(self.y1)
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)
        
    def test_yearlike_model(self):
        """Test creating a new YearLike instance and adding it to the database"""

        self.assertEqual(YearLike.query.count(), 0)

        self.fact_to_like = Year.query.filter_by(year=1).one()
        
        self.new_yearlike = YearLike(
            fact_id = self.fact_to_like.id
        )
        
        db.session.add(self.new_yearlike)
        db.session.commit()
        
        self.assertEqual(YearLike.query.count(), 1)
        self.assertEqual(YearLike.query.filter_by(fact_id=self.fact_to_like.id).one().category, "year")


