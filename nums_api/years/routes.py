from flask import Blueprint, jsonify
from nums_api.years.models import Year
import random

years = Blueprint("years", __name__)


@years.get("/<int:year>")
def get_year_fact(year):
    """ Route for getting a random fact about year.

    If fact found, returns JSON like:
        {fact: {
            "year" : 1,
            "fragment": "text",
            "statement": "text",
            "type": year,
            }
        }

    If no fact found, returns error message like:
    { error:
        { "message": "A test fact for year test not found",
          "status": 404
        }
    }
    """

    year_data = Year.query.filter_by(year = year).all()

    if year_data:
        single_year_data = random.choice(year_data)
        year_fact = {
            'year': single_year_data.year,
            'fragment': single_year_data.fact_fragment,
            'statement': single_year_data.fact_statement,
            'type': 'year',
        }

        return jsonify(fact = year_fact)
    else:
        err = {
            'status': 404,
            'message': f"A fact for { year } not found",
        }
        return (jsonify(error = err), 404)

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
        'year': single_year_data.year,
        'fragment': single_year_data.fact_fragment,
        'statement': single_year_data.fact_statement,
        'type': 'year',
    }

    return jsonify(fact = year_fact)
