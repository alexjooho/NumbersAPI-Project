from flask import Blueprint, jsonify
from nums_api.dates.models import Date
from random import choice

dates = Blueprint('dates', __name__)


@dates.get('/<int:month>/<int:day>')
def get_date_fact(month, day):
    """Route to retrieve a random date fact on specified month/day.
        Returns JSON
        {fact: {
            'number': 120,
            'year': 1783,
            'fragment': 'Some fact fragment',
            'statement': 'Some fact statement',
            'type': 'date'
            }
        }
        Returns JSON 400 error if month/day not in range:
        {'error': {
                'message': 'Invalid value for month/day',
                'status': 400
        }}
        Returns JSON 404 error if no fact for specified month/day:
        {'error': {
                'message': 'A date fact for 1/30 not found',
                'status': 404
        }}
        """

    try:
        days = Date.date_to_day_of_year(month, day)
    except ValueError as e:
        return (jsonify(
            error={
                'message': str(e),
                'status': 400
            }), 400)

    try:
        res = Date.query.filter_by(day_of_year=days).all()
        date_fact_res = choice(res)
    except (IndexError):
        return (jsonify(
            error={
                'message': f'A date fact for { month }/{ day } not found',
                'status': 404
            }), 404)

    date_fact = {
        'number': date_fact_res.day_of_year,
        'year': date_fact_res.year,
        'fragment': date_fact_res.fact_fragment,
        'statement': date_fact_res.fact_statement,
        'type': 'date'
    }

    return jsonify(fact=date_fact)


@dates.get("/random")
def get_date_fact_random():
    """Route to retrieve a random date fact.
    Returns JSON
    {fact: {
        'number': 120,
        'year': 1783,
        'fragment': 'Some fact fragment',
        'statement': 'Some fact statement',
        'type': 'date'
        }
    }
    """

    date_facts_res = Date.query.all()
    random_fact = choice(date_facts_res)

    random_date_fact = {
        'number': random_fact.day_of_year,
        'year': random_fact.year,
        'fragment': random_fact.fact_fragment,
        'statement': random_fact.fact_statement,
        'type': 'date'
    }

    return jsonify(fact=random_date_fact)
