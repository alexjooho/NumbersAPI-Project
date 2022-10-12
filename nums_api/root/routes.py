from flask import Blueprint, render_template, flash, redirect
from nums_api.mail.models import Email
from nums_api.mail.forms import EmailAddForm

# from datetime import date
# import requests
import markdown

root = Blueprint("root", __name__, template_folder='templates',
                 static_folder='static')

@root.route("/", methods=["GET", "POST"])
def homepage():
    """Show homepage:
        - Renders API docs from a markdown file to Jinja Templates.
    """

    # currDate = date.today()
    # resp = requests.get(f"http://localhost:5001/api/date/{currDate.month}/{currDate.day}")
    # date_data = resp.json()
    # couldn't use this yet because no database data


    with open("nums_api/documentation.md", "r", encoding="utf-8") as file:
        text = file.read()

    html = markdown.markdown(text, output_format="xhtml",
                             extensions=["fenced_code"])
    form = EmailAddForm()

    if form.validate_on_submit():
        email = Email.subscribe(
            form.email.data)

        if email:
            flash(f"{email.email} added!", "success")

        else: flash("Invalid email.", 'danger')

        return redirect("/")

    return render_template('index.html',
                            documentation=html,
                            form=form)

