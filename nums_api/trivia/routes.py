from flask import Blueprint, jsonify, request
from nums_api.trivia.models import Trivia
from random import choice
import random
import re
from nums_api.helpers.batch import get_batch_nums

trivia = Blueprint("trivia", __name__)


@trivia.get("/<int:number>")
def get_trivia_fact(number):
    """
    Route for getting trivia fact about a number. The number is received from
    the url parameter.
    If the URL parameter is not a positive integer, it will return a 404 error.

    If url parameter is valid, returns json:
     { fact: { number, fragment, statement, type } }

    Otherwise it returns an error:
    { error: { message: f"A { category } fact for { number } not found", status: 404} }
    """

    trivia = Trivia.query.filter_by(number=number).all()
    if not trivia:
        error = {
            "status": 404,
            "message": f"A trivia fact for { number } not found"
        }

        return jsonify(error=error), 404

    random_trivia = choice(trivia)
    fact = {
        "number": random_trivia.number,
        "fragment": random_trivia.fact_fragment,
        "statement": random_trivia.fact_statement,
        "type": "trivia"
    }

    return jsonify(fact=fact)


@trivia.get("/random")
def get_trivia_fact_random():
    """
    Accepts a parameter "count" for number of random facts requested.

    Route for getting random trivia fact.
    Queries all rows in trivia table and randomly picks one
    Returns json:
    { fact: { number, fragment, statement, type } }
    """

    facts = []

    count = int(request.args.get("count") or 1)

    if count > 50:
        count = 50

    while count > 0:

        random_trivia = random.choice(Trivia.query.all())

        fact = {"fact": {
            "number": random_trivia.number,
            "fragment": random_trivia.fact_fragment,
            "statement": random_trivia.fact_statement,
            "type": "trivia"
        }}

        facts.append(fact)

        count -= 1

    if len(facts) == 1:
        return jsonify(facts[0])

    return jsonify(facts)


@trivia.get("/<num>")
def get_batch_trivia_fact(num):
    """Returns a random trivia fact in JSON about a a batch of numbers passed as a
    URL parameter.
        - If facts are found, returns JSON response:
        { "facts": [
            {
                "number": 1
                "fragment": fact_fragment
                "statement": fact_statement
                "type": "trivia"
            },
            {
                "number": 2
                "fragment": fact_fragment
                "statement": fact_statement
                "type": "trivia"
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
        fact = Trivia.query.filter_by(number=num).all()

        random_fact = random.choice(fact)

        factInfo = {
            "number": str(random_fact.number),
            "fragment": random_fact.fact_fragment,
            "statement": random_fact.fact_statement,
            "type": "trivia"
        }

        facts.append(factInfo)

    return jsonify(facts=facts)
