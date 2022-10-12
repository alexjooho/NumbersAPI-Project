from datetime import datetime, timedelta
from flask import Blueprint, current_app, render_template
from flask_mail import Message, Mail
from nums_api.mail.models import Email
from nums_api.dates.models import Date
from nums_api.years.models import Year
from nums_api.maths.models import Math
from nums_api.trivia.models import Trivia

emails = Blueprint("emails", __name__, template_folder="templates")


@emails.route("/")
def index():
    """Emails subscribers on a weekly basis

    - fetch subscribers from Email database
    - queries new_facts from databases [Date, Math, Trivia, Year,] from 1 weeks
    ago till current date
    - render html template with new_facts from each categories
    - sends email

    """
    current_date = datetime.now()
    one_week_ago = current_date - timedelta(weeks=1)

    databases = [Date, Math, Trivia, Year]
    new_facts = []

    for db in databases:
        facts = db.query.filter(
        db.added_at >= one_week_ago).filter(db.added_at < current_date
             ).all()
        new_facts.append(facts)

    facts = dict(enumerate(new_facts))

    subscribers = Email.query.all()

    with current_app.app_context():
        mail = Mail()
        for subscriber in subscribers:
            subject = "Weekly Numbers API new facts"
            msg = Message(recipients=[subscriber.email],
                          subject=subject,
                          html=render_template(
                              "emails.html",
                              date_facts=facts.get(0, None),
                              math_facts=facts.get(1, None),
                              trivia_facts=facts.get(2, None),
                              year_facts=facts.get(3, None),
                              ),
                          charset='utf-8')

            mail.send(msg)

        return f"emails sent successfully"
