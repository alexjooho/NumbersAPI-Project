from flask import Blueprint

math = Blueprint("math", __name__)


@math.get("/<number>")
def get_math_fact(number):
    """FIXME
    Stub route for getting math fact about number.
    """

    return f"Some interesting math fact about {number}."


@math.get("/random")
def get_math_fact_random():
    """FIXME
    Stub route for getting math fact about random number.
    """

    return "Some interesting math fact about a random number."
