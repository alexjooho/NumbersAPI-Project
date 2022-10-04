from flask import Blueprint, jsonify, request
from nums_api.years.models import Year
import random

years = Blueprint("years", __name__)


@years.get("/<int:year>")
def get_year_fact(year):
    """Returns a random year fact in JSON about a number passed as a
    URL parameter.
    Accepts optional query parameter: notfound = "floor" or "ceil",
    returns the previous or next found number if number not found.

    - If fact found and/or notfound query is provided,
    returns JSON response:
        { "fact": {
            "year" : year,
            "fragment": fact_fragment,
            "statement": fact_statement,
            "type": "year",
            }
        }

    - If no fact found, returns error message like:
    { error:
        { "message": "A test fact for year test not found",
          "status": 404
        }
    }
    """

    year_data = Year.query.filter_by(year = year).all()
    notfound_query = request.args.get("notfound")

    if notfound_query == "floor" and not year_data:
        year_query = (
            Year.query
                .filter(Year.year < year)
                .order_by(Year.year.desc())
                .first())
        if year_query:
            year_data = Year.query.filter_by(year=year_query.year).all()

    if notfound_query == "ceil" and not year_data:
        year_query = (
            Year.query
                .filter(Year.year > year)
                .order_by(Year.year.asc())
                .first())
        if year_query:
            year_data = Year.query.filter_by(year=year_query.year).all()

    if year_data:
        single_year_data = random.choice(year_data)
        year_fact = {
            "year": single_year_data.year,
            "fragment": single_year_data.fact_fragment,
            "statement": single_year_data.fact_statement,
            "type": "year",
        }

        return jsonify(fact = year_fact)
    else:
        error = {
            "status": 404,
            "message": f"A fact for { year } not found",
        }
        return (jsonify(error = error), 404)

@years.get("/random")
def get_year_fact_random():
    """ Route for getting fact about random year.
        Returns JSON like:
        { fact: {
            "year" : 1,
            "fragment": "text",
            "statement": "text",
            "type": year,
            }}
    """

    year_data = Year.query.all()

    single_year_data = random.choice(year_data)

    year_fact = {
        "year": single_year_data.year,
        "fragment": single_year_data.fact_fragment,
        "statement": single_year_data.fact_statement,
        "type": "year",
    }

    return jsonify(fact = year_fact)
