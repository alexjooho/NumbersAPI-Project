from unittest import TestCase
from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from nums_api.mail.models import Email
from flask_mail import Mail

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.drop_all()
db.create_all()


class EmailRouteBaseTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""
        self.client = app.test_client()

        Email.query.delete()

        self.m1 = Email(
            email="testA@example.com",
        )

        self.m2 = Email(
            email="testB@example.com",
        )

        db.session.add_all([self.m1, self.m2])

        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)


class SendEmailRouteTestCase(EmailRouteBaseTestCase):
    def test_sent_Email_fact(self):
        """Test GET route for sending email works"""
        mail = Mail(app)
        with app.test_client() as client:
            with mail.record_messages() as outbox:
                url = "/api/emails/"
                resp = client.get(url)
                
                assert len(outbox) == 2
                assert outbox[0].subject == "Weekly Numbers API new facts"
                self.assertEqual(resp.status_code, 200)