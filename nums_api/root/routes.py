from flask import Blueprint, render_template

root = Blueprint("root", __name__, template_folder='templates')


@root.get("/")
def homepage():
    """Show homepage:

        - Renders API docs from a markdown file to Jinja Templates.

    """

    return render_template('base.html')
