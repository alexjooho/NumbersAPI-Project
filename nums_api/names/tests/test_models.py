from unittest import TestCase
from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from nums_api.names.models import Name

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.drop_all()
db.create_all()

class NameModelTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""

        Name.query.delete()

        self.n1 = Name(
            name="NAMETEST",
            fact_fragment="the name for this n1 test",
            fact_statement="NAMETEST is the name for this n1 test fact statement.",
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
        """Test creating a new Name instance and adding it to the database"""
        self.assertIsInstance(self.n1, Name)
        self.assertEqual(Name.query.count(), 0)

        db.session.add(self.n1)
        db.session.commit()

        self.assertEqual(Name.query.count(), 1)
        self.assertEqual(Name.query.filter_by(name="NAMETEST").one().name, "NAMETEST")
