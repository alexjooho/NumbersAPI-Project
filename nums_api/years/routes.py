from flask import Blueprint, jsonify, request
from nums_api.years.models import Year
import random
import re
from nums_api.helpers.batch import get_batch_nums
from nums_api.config import MAX_BATCH


years = Blueprint("years", __name__)

@years.get("/<int:year>")
def get_year_fact(year):
    """ Route for getting a random fact about year.
    If fact found, returns JSON:
        {fact: {
            "year" : 1,
            "fragment": "text",
            "statement": "text",
            "type": year,
            }
        }

    If no fact found, returns error message:
    { error:
        { "message": "A fact for year not found",
          "status": 404
        }
    }
    """
    year_facts = Year.query.filter_by(year=year).all()

    if year_facts:
        year_fact = random.choice(year_facts)
        fact = {
            "year": year_fact.year,
            "fragment": year_fact.fact_fragment,
            "statement": year_fact.fact_statement,
            "type": "year",
        }
        return jsonify(fact=fact)
    else:
        error = {
            "status": 404,
            "message": f"A fact for { year } not found",
        }
        return (jsonify(error=error), 404)


@years.get("/<years>")
def get_years_range_facts(years):
    """ Route for getting a random fact about multiple years.
    If facts found, returns JSON:
        {facts: [
                    {
                    "year" : 1,
                    "fragment": "text",
                    "statement": "text",
                    "type": year,
                    },
                    {
                    "year" : 3,
                    "fragment": "text3",
                    "statement": "text3",
                    "type": year,
                    },
                ...]
        }

    If no facts found for year range, returns JSON:
        {error:
            { "message": "No facts for { years } were found",
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
    years_regex = r"^([0-9]{1,4})(\.\.[0-9]{1,4})?(-[0-9]{1,4})?((,[0-9]{1,4})?)*(\.\.[0-9]{1,4})?(-[0-9]{1,4})?$"

    if not re.match(years_regex, years):
        error = {
            "status": 400,
            "message": "Invalid URL",
        }
        return (jsonify(error=error), 400)

    years = re.sub(r"-", "..", years, flags=re.DOTALL)

    try:
        years_range = get_batch_nums(years)
    except Exception:
        return (jsonify(
            error={
                "message": str(Exception),
                "status": 400
            }), 400)

    facts = []

    for year in years_range:
        year_facts = Year.query.filter_by(year=year).all()

        if year_facts:
            year_fact = random.choice(year_facts)
            fact = {
                "year": year_fact.year,
                "fragment": year_fact.fact_fragment,
                "statement": year_fact.fact_statement,
                "type": "year",
            }
            facts.append(fact)

    if not len(facts):
        error = {
            "status": 404,
            "message": f"No facts for { years } were found",
        }
        return (jsonify(error=error), 404)

    return jsonify(facts=facts)


@years.get("/random")
def get_year_fact_random():
    """ Route for getting random fact about a single year, accepts an optional
    parameter of count for getting count number of random facts.
    Returns JSON if no count param:
        { fact: {
            "year" : year,
            "fragment": "fragment",
            "statement": "statement",
            "type": "year",
            }}

    If count param specified, returns JSON:
        {facts: [
                    {
                    "year" : year,
                    "fragment": "fragment",
                    "statement": "statement",
                    "type": "year",
                    },
                    {
                    "year" : year,
                    "fragment": "fragment",
                    "statement": "statement",
                    "type": "year",
                    },
                ...]
        }

    If count > MAX_BATCH, return MAX_BATCH count.
    """
    count_query = request.args.get("count")

    years_facts = Year.query.all()

    if not count_query:
        year_fact = random.choice(years_facts)

        fact = {
            "year": year_fact.year,
            "fragment": year_fact.fact_fragment,
            "statement": year_fact.fact_statement,
            "type": "year",
        }

        return jsonify(fact=fact)

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
    if count_query > len(years_facts):
        count_query = len(years_facts)

    facts = []

    random_years_facts = random.sample(years_facts, count_query)

    for year_fact in random_years_facts:
        fact = {
            "year": year_fact.year,
            "fragment": year_fact.fact_fragment,
            "statement": year_fact.fact_statement,
            "type": "year",
        }
        facts.append(fact)

    return jsonify(facts=facts)
