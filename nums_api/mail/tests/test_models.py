from unittest import TestCase
from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from nums_api.mail.models import Email

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.drop_all()
db.create_all()


class EmailModelTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""

        Email.query.delete()

        self.m1 = Email(
            email="test@test.com"
        )

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

    def test_model(self):
        self.assertIsInstance(self.m1, Email)
        self.assertEqual(Email.query.count(), 0)

        db.session.add(self.m1)
        db.session.commit()

        self.assertEqual(Email.query.count(), 1)
        self.assertEqual(Email.query.filter_by(
            email="test@test.com").one().email, "test@test.com")
