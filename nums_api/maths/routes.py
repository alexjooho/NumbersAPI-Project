from flask import Blueprint, jsonify, request
from nums_api.config import MAX_BATCH
from nums_api.helpers.batch import get_batch_nums
from nums_api.maths.models import Math
import random
import re

math = Blueprint("math", __name__)

@math.get("/<int:number>")
def get_math_fact(number):
    """Returns a random math fact in JSON about a number passed as a
    URL parameter.
        - If fact is found, returns JSON response:
        { "fact": {
            "number": number
            "fragment": fact_fragment
            "statement": fact_statement
            "type": "math"
        }}
        - If fact is not found, returns JSON response:
            { "error": {
                "message": f"A math fact for { number } not found",
                "status": 404 } }
    """
    facts = Math.query.filter_by(number=number).all()

    if (facts):
        random_fact = random.choice(facts)
        factInfo = {
            "number": random_fact.number,
            "fragment": random_fact.fact_fragment,
            "statement": random_fact.fact_statement,
            "type": "math"
        }
        return jsonify(fact=factInfo)
    else:
        error =  {
            "status": 404,
            "message": f"A math fact for { number } not found",
            }
        return (jsonify(error = error), 404)


@math.get("/<num>")
def get_batch_math_fact(num):
    """Returns a random math fact in JSON about a a batch of numbers passed as a
    URL parameter.
        - If facts are found, returns JSON response:
        { "facts": [
            {
                "number": "1"
                "fragment": "fact_fragment"
                "statement": "fact_statement"
                "type": "math"
            },
            {
                "number": "2"
                "fragment": "fact_fragment"
                "statement": "fact_statement"
                "type": "math"
            }, ...]
        }
        - If fact is not found, returns JSON response:
            { "error": {
                "message": "Invalid URL",
                "status": 400 } }
    """

    decimal_regex = r"^-?\d+(?:\.\d+)?(\.\.-?\d+(?:\.\d+)?)?(,-?\d+(?:\.\d+)?(\.\.-?\d+(?:\.\d+)?)?)*$"

    if not re.match(decimal_regex, num):
        error = {
            "message": "Invalid URL",
            "status": 400}
        return (jsonify(error = error), 400)

    try:
        nums_range = get_batch_nums(num)
    except Exception:
        return (jsonify(
            error={
                "message": str(Exception),
                "status": 400
            }), 400)

    facts = []

    for num in nums_range:
        fact = Math.query.filter_by(number=num).all()

        if fact:
            random_fact = random.choice(fact)

            factInfo = {
                "number": random_fact.number,
                "fragment": random_fact.fact_fragment,
                "statement": random_fact.fact_statement,
                "type": "math"
            }

            facts.append(factInfo)

    if not len(facts):
        error = {
            "status": 404,
            "message": f"No facts for { num } were found",
        }
        return (jsonify(error=error), 404)

    return jsonify(facts=facts)


@math.get("/random")
def get_math_fact_random():
    """
    Accepts a parameter "count" for number of random facts requested.

    Returns a random math fact in JSON about a random number.
        - Returns JSON response:
        { "fact": {
            "number": random number
            "fragment": fact_fragment
            "statement": fact_statement
            "type": "math"
        }}
    """
    count = request.args.get("count")
    numbers_facts = Math.query.all()

    if not count:
        number_fact = random.choice(numbers_facts)

        fact =  {
            "number": number_fact.year,
            "fragment": number_fact.fact_fragment,
            "statement": number_fact.fact_statement,
            "type": "math",
        }

        return jsonify(fact = fact)

    try:
        count = int(count)
    except ValueError:
        return (jsonify(
            error={
                "message": f"{ count } is an invalid count number",
                "status": 400
            }), 400)

    if count < 1:
        return (jsonify(
            error={
                "message": f"{ count } is an invalid count number",
                "status": 400
            }), 400)

    if count > MAX_BATCH:
        count = MAX_BATCH
    if count_query > len(numbers_facts):
        count_query = len(numbers_facts)

    facts = []

    random_numbers_facts = random.sample(numbers_facts, count_query)

    for year_fact in random_numbers_facts:
        fact = {
            "year": year_fact.year,
            "fragment": year_fact.fact_fragment,
            "statement": year_fact.fact_statement,
            "type": "year",
        }
        facts.append(fact)

    return jsonify(facts=facts)