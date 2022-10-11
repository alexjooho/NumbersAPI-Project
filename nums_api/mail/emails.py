from flask import Blueprint, current_app
# from nums_api import mail (doesnt work, cant access class methods)
from flask_mail import Message, Mail

emails = Blueprint("emails", __name__)

@emails.route("/")
def index():
    users = [
        { 'name': 'test 1', 'email': 'test1@gmail.com'},
        { 'name': 'test 2', 'email': 'test2@gmail.com' }]

    with current_app.app_context():
        mail = Mail()
    # with mail.connect() as conn:
    # (doest work) - AttributeError: module 'nums_api.mail' has no attribute 'connect')
        for user in users:
            message = '...this is a test email'
            subject = "hello, %s" % user['name']
            msg = Message(recipients=[user['email']],
                        body=message,
                        subject=subject)

            mail.send(msg)

            return 'emails sent successfully'