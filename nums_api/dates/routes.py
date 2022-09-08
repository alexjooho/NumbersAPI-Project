from flask import Blueprint

dates = Blueprint("dates", __name__)


@dates.get("/<month>/<day>")
def get_date_fact(month, day):
    """FIXME
    Stub route for getting fact about date.
    """

    return f"Some interesting fact about the date {month}/{day}."


@dates.get("/random")
def get_date_fact_random():
    """FIXME
    Stub route for getting fact about random date.
    """

    return "Some interesting fact about a random date."
