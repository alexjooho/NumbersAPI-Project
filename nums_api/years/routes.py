from flask import Blueprint

years = Blueprint("years", __name__)


@years.get("/<year>")
def get_year_fact(year):
    """FIXME
    Stub route for getting fact about year.
    """

    return f"Some interesting fact about the year {year}."


@years.get("/random")
def get_year_fact_random():
    """FIXME
    Stub route for getting fact about random year.
    """

    return "Some interesting fact about a random year."
