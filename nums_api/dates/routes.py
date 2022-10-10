from flask import Blueprint, jsonify, request
from nums_api.dates.models import Date
import random
import re
from nums_api.helpers.dates_batch import get_batch_dates
from nums_api.config import MAX_BATCH

dates = Blueprint("dates", __name__)


@dates.get("/<int:month>/<int:day>")
def get_date_fact(month, day):
    """Route to retrieve a random date fact on specified month/day.
        Returns JSON
        {fact: {
            "number": 120,
            "year": 1783,
            "fragment": "Some fact fragment",
            "statement": "Some fact statement",
            "type": "date"
            }
        }
        Returns JSON 400 error if month/day not in range:
        {"error": {
                "message": "Invalid value for month/day",
                "status": 400
        }}
        Returns JSON 404 error if no fact for specified month/day:
        {"error": {
                "message": "A date fact for 1/30 not found",
                "status": 404
        }}
        """

    try:
        day = Date.date_to_day_of_year(month, day)
    except ValueError as e:
        return (jsonify(
            error={
                "message": str(e),
                "status": 400
            }), 400)

    try:
        res = Date.query.filter_by(day_of_year=day).all()
        date_fact_res = random.choice(res)
    except (IndexError):
        return (jsonify(
            error={
                "message": f"A date fact for { month }/{ day } not found",
                "status": 404
            }), 404)

    date_fact = {
        "number": date_fact_res.day_of_year,
        "year": date_fact_res.year,
        "fragment": date_fact_res.fact_fragment,
        "statement": date_fact_res.fact_statement,
        "type": "date"
    }

    return jsonify(fact=date_fact)

@dates.get("/<path:dates>")
def get_dates_range_facts(dates):
    """Route to retrieve a random date fact on a range of multiple dates.
        Example of dates input:
          - 1/10..1/20,2/30 (both and in either order)
          - 1/1..1/31 (min..max inclusive of both)
          - 1/1,1/5,2/15 (individual dates separated by comma)

        Returns JSON
        {facts: [{
            "number": 10,
            "year": 1783,
            "fragment": "Some fact fragment",
            "statement": "Some fact statement",
            "type": "date"
            }, ...
        ]}

        Returns JSON 400 error if dates are invalid.
            {"error": {
                    "message": "Invalid value for month/day",
                    "status": 400
            }}

        If no facts found for dates range, returns JSON:
            {error:
                { "message": "No facts for { dates } were found",
                "status": 404
                }
            }

        If invalid URL syntax for year range, returns JSON:
            {error:
                { "message": "Invalid URL",
                "status": 400
                }
            }
    """
    dates_regex = r"([0-9]{1,2}\/[0-9]{1,2})(\.\.[0-9]{1,2}\/[0-9]{1,2})?((,[0-9]{1,2}\/[0-9]{1,2})+(\.\.[0-9]{1,2}\/[0-9]{1,2})?)?"

    if not re.match(dates_regex, dates):
        error = {
            "status": 400,
            "message": "Invalid URL",
        }
        return (jsonify(error=error), 400)

    try:
        dates_range = get_batch_dates(dates)
    except Exception as exc:
        return (jsonify(
            error={
                "message": str(exc),
                "status": 400
            }), 400)

    facts = []

    for date in dates_range:
        date_facts = Date.query.filter_by(day_of_year=date).all()

        if date_facts:
            date_fact = random.choice(date_facts)
            fact = {
                "number": date_fact.day_of_year,
                "year": date_fact.year,
                "fragment": date_fact.fact_fragment,
                "statement": date_fact.fact_statement,
                "type": "date"
            }
            facts.append(fact)

    if not len(facts):
        error = {
            "status": 404,
            "message": f"No facts for { dates } were found",
        }
        return (jsonify(error=error), 404)

    return jsonify(facts=facts)


@dates.get("/random")
def get_date_fact_random():
    """Route to retrieve a random date fact, accepts an optional
    parameter of count for getting count number of random facts.
    Returns JSON if no count param:
        {fact: {
            "number": 120,
            "year": 1783,
            "fragment": "Some fact fragment",
            "statement": "Some fact statement",
            "type": "date"
            }
        }
    If count param specified, returns JSON:
        {facts: [
            {
            "number": 120,
            "year": 1783,
            "fragment": "Some fact fragment",
            "statement": "Some fact statement",
            "type": "date"
            },
        ...]
        }

    If count > MAX_BATCH, return MAX_BATCH count of facts.
    If count > total number of year facts, return total number of facts.
    """
    count_query = request.args.get("count")

    date_facts = Date.query.all()

    if not count_query:
        random_fact = random.choice(date_facts)

        random_date_fact = {
            "number": random_fact.day_of_year,
            "year": random_fact.year,
            "fragment": random_fact.fact_fragment,
            "statement": random_fact.fact_statement,
            "type": "date"
        }

        return jsonify(fact=random_date_fact)

    try:
        count_query = int(count_query)
    except ValueError:
        return (jsonify(
            error={
                "message": f"{ count_query } is an invalid count number",
                "status": 400
            }), 400)

    if count_query < 1:
        return (jsonify(
            error={
                "message": f"{ count_query } is an invalid count number",
                "status": 400
            }), 400)

    if count_query > MAX_BATCH:
        count_query = MAX_BATCH
    if count_query > len(date_facts):
        count_query = len(date_facts)

    facts = []

    random_dates_facts = random.sample(date_facts, count_query)

    for date_fact in random_dates_facts:
        fact = {
            "number": date_fact.day_of_year,
            "year": date_fact.year,
            "fragment": date_fact.fact_fragment,
            "statement": date_fact.fact_statement,
            "type": "date",
        }
        facts.append(fact)

    return jsonify(facts=facts)