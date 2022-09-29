from flask import Blueprint, jsonify
from nums_api.years.models import Year
from sqlalchemy.sql import func
import random

years = Blueprint("years", __name__)


@years.get("/<int:year>")
def get_year_fact(year):
    """ Route for getting a random fact about year.

    If fact found, returns JSON like:
        {fact: {
            "type": year,
            "id" : 1,
            "year" : 1,
            "fact_fragment": "text",
            "fact_statement": "text",
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
            'type': 'year',
            'id' : single_year_data.id,
            'year': single_year_data.year,
            'fact_fragment': single_year_data.fact_fragment,
            'fact_statement': single_year_data.fact_statement
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
            "type": year,
            "id" : 1,
            "year" : 1,
            "fact_fragment": "text",
            "fact_statement": "text",
            }}
    """
    # year_data = Year.query.order_by(func.random()).first()
    year_data = Year.query.all()

    single_year_data = random.choice(year_data)

    year_fact = {
        'type': 'year',
        'id' : single_year_data.id,
        'year': single_year_data.year,
        'fact_fragment': single_year_data.fact_fragment,
        'fact_statement': single_year_data.fact_statement
    }

    return jsonify(fact = year_fact)
