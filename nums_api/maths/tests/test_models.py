from unittest import TestCase
from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from nums_api.maths.models import Math

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.drop_all()
db.create_all()

class MathModelTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""

        Math.query.delete()

        self.m1 = Math(
            number=1.5,
            fact_fragment="the number for this m1 test fact fragment",
            fact_statement="1.5 is the number for m1 this test fact statement.",
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
        self.assertIsInstance(self.m1, Math)
        self.assertEqual(Math.query.count(), 0)

        db.session.add(self.m1)
        db.session.commit()

        self.assertEqual(Math.query.count(), 1)
        self.assertEqual(Math.query.filter_by(number=1.5).one().number, 1.5)
