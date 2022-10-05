from flask import Blueprint, jsonify, request
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
        error = {"error": {
            "message": f"A math fact for { number } not found",
            "status": 404}}
        return (jsonify(error), 404)


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

    facts = []

    count = int(request.args.get("count") or 1)

    if count > 50:
        count = 50

    while count > 0:

        num_fact = random.choice(Math.query.all())

        fact = {"fact": {
            "number": num_fact.number,
                "fragment": num_fact.fact_fragment,
                "statement": num_fact.fact_statement,
                "type": "math"
                }}

        facts.append(fact)

        count -= 1

    if len(facts) == 1:
        return jsonify(facts[0])

    return jsonify(facts)


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
        error = {"error": {
            "message": "Invalid URL",
            "status": 400}}
        return (jsonify(error), 400)

    nums = get_batch_nums(num)
    facts = []

    for num in nums:
        fact = Math.query.filter_by(number=num).all()

        random_fact = random.choice(fact)

        factInfo = {
            "number": random_fact.number,
            "fragment": random_fact.fact_fragment,
            "statement": random_fact.fact_statement,
            "type": "math"
        }

        facts.append(factInfo)

    return jsonify(facts=facts)
