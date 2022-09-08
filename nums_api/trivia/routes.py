from flask import Blueprint

trivia = Blueprint("trivia", __name__)


@trivia.get("/<number>")
def get_trivia_fact(number):
    """FIXME
    Stub route for getting trivia fact about number.
    """

    return f"Some interesting trivia fact about {number}."


@trivia.get("/random")
def get_trivia_fact_random():
    """FIXME
    Stub route for getting trivia fact about random number.
    """

    return "Some interesting trivia fact about a random number."
