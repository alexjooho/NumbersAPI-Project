from flask import Blueprint, jsonify
from models import Date
from random import choice, randint

dates = Blueprint("dates", __name__)

months_days = {
    1: 31,
    2: 29,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}


@dates.get("/<int: month>/<int: day>")
def get_date_fact(month, day):
    """route to retreive a random date fact on specified month/day
        returns json
        {
        'month': 12,
        'day': 30,
        'year': 1783,
        'fact_fragment': 'some fact frament',
        'fact_statement': 'some fact statement',
        'type': 'date'
        }
        returns error if month/day not in range
        """

    error_msg = {
        "message": f"A date fact for { month/day } not found",
        "status": 404
    }

    if (day > months_days[month]) or (not months_days[month]):
        return (jsonify(error=error_msg), 404)

    days = Date.date_to_day_of_year(month, day)

    try:
        date_fact_res = choice(Date.query.filter_by(day_of_year=days))
    except (IndexError):
        return (jsonify(error=error_msg), 404)

    date_fact = {
        'month': month,
        'day': day,
        'year': date_fact_res.year,
        'fact_fragment': date_fact_res.fact_fragment,
        'fact_statement': date_fact_res.fact_statement,
        'type': 'date'
    }

    return jsonify(date_fact)


@dates.get("/random")
def get_date_fact_random():
    """route to retreive a random date fact
    returns json
    {
    'month': 12,
    'day': 30,
    'year': 1783,
    'fact_fragment': 'some fact frament',
    'fact_statement': 'some fact statement',
    'type': 'date'
    }
    """

    random_fact = None

    # keep querying until there is a random fact
    while not random_fact:
        month = randint(1, 12)
        day = randint(1, months_days[month])
        days = Date.date_to_day_of_year(month, day)
        random_fact = choice(Date.query.filter_by(day_of_year=days))

    random_date_fact = {
        'month': month,
        'day': day,
        'year': random_fact.year,
        'fact_fragment': random_fact.fact_fragment,
        'fact_statement': random_fact.fact_statement,
        'type': 'date'
    }

    return jsonify(random_date_fact)
