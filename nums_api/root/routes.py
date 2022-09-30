from flask import Blueprint, render_template, send_from_directory
import os
import markdown


root = Blueprint("root", __name__, template_folder='templates',
                 static_folder='static')


@root.get("/")
def homepage():
    """Show homepage:
        - Renders API docs from a markdown file to Jinja Templates.
    """

    with open("nums_api/documentation.md", "r", encoding="utf-8") as file:
        text = file.read()

    html = markdown.markdown(text, output_format="xhtml",
                             extensions=["fenced_code"])

    return render_template('index.html', documentation=html)

