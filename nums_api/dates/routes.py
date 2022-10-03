from flask import Blueprint, jsonify
from nums_api.dates.models import Date
from random import random, choice, randint

dates = Blueprint("dates", __name__)


@dates.get("/<int:month>/<int:day>")
def get_date_fact(month, day):
    """route to retreive a random date fact on specified month/day
        returns json
        {fact: {
            'day_of_year': 120,
            'year': 1783,
            'fact_fragment': 'some fact frament',
            'fact_statement': 'some fact statement',
            'type': 'date'
            }
        }
        returns value error if month/day not in range
        returns 404 error if no fact for specified month/day
        """

    error_msg = {
        "message": f"A date fact for { month }/{ day } not found",
        "status": 404
    }

    try:
        days = Date.date_to_day_of_year(month, day)
    except ValueError as e:
        return (jsonify(error={
            "message": str(e),
            "status": 404
        }), 404)

    try:
        res = Date.query.filter_by(day_of_year=days).all()
        date_fact_res = choice(res)
    except (IndexError):
        return (jsonify(error=error_msg), 404)

    date_fact = {
        'day_of_year': date_fact_res.day_of_year,
        'year': date_fact_res.year,
        'fact_fragment': date_fact_res.fact_fragment,
        'fact_statement': date_fact_res.fact_statement,
        'type': 'date'
    }

    return jsonify(fact=date_fact)


@dates.get("/random")
def get_date_fact_random():
    """route to retreive a random date fact
    returns json
    {fact: {
        'day_of_year': 120,
        'year': 1783,
        'fact_fragment': 'some fact frament',
        'fact_statement': 'some fact statement',
        'type': 'date'
        }
    }
    """

    date_facts_res = Date.query.all()
    random_fact = choice(date_facts_res)

    random_date_fact = {
        'day_of_year': random_fact.day_of_year,
        'fact_fragment': random_fact.fact_fragment,
        'fact_statement': random_fact.fact_statement,
        'type': 'date'
    }

    return jsonify(fact=random_date_fact)
