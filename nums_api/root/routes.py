from flask import Blueprint, render_template
from jinja_markdown import MarkdownExtension
import markdown




root = Blueprint("root", __name__, template_folder='templates')


@root.get("/")
def homepage():
    """Show homepage:

        - Renders API docs from a markdown file to Jinja Templates.

    """

    with open("nums_api/documentation.md", "r", encoding="utf-8") as file:
        text = file.read()

    html = markdown.markdown(text,output_format="xhtml", extensions=["fenced_code"])

    # md_template_string = markdown.markdown('## URL Structure')
    # print(md_template_string)
    # md = Markdown(md)

    return render_template('home.html', documentation=html)
