from flask import Blueprint, jsonify, request
from nums_api.trivia.models import Trivia
from random import choice
import random
import re
from nums_api.helpers.batch import get_batch_nums
from nums_api.config import MAX_BATCH

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


@trivia.get("/<batch>")
def get_batch_trivia_fact(batch):
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

        If no facts found for trivia range, returns JSON:
        {error:
            { "message": "No facts for { trivia } were found",
            "status": 404
            }
        }

        -     If invalid URL syntax for trivia range, returns JSON:
            { "error": {
                "message": "Invalid URL",
                "status": 400 } }
    """

    decimal_regex = r"^-?\d+(?:\.\d+)?(\.\.-?\d+(?:\.\d+)?)?(,-?\d+(?:\.\d+)?(\.\.-?\d+(?:\.\d+)?)?)*$"

    print(MAX_BATCH)
    if not re.match(decimal_regex, batch):
        error = {
            "status": 400,
            "message": "Invalid URL"}
        return (jsonify(error=error), 400)

    try:
        nums = get_batch_nums(batch)
    except Exception:
        return (jsonify(
            error={
                "message": str(Exception),
                "status": 400
            }), 400)

    facts = []

    for num in nums:
        trivia_fact = Trivia.query.filter_by(number=num).all()

        if (trivia_fact):
            random_fact = random.choice(trivia_fact)

            factInfo = {
                "number": str(random_fact.number),
                "fragment": random_fact.fact_fragment,
                "statement": random_fact.fact_statement,
                "type": "trivia"
            }

            facts.append(factInfo)

    if not len(facts):
        error = {
            "status": 404,
            "message": f"No facts for { batch } were found",
        }
        return (jsonify(error=error), 404)

    return jsonify(facts=facts)


@trivia.get("/random")
def get_trivia_fact_random():
    """
    Accepts a parameter "count" for number of random facts requested.

    Route for getting random trivia fact.
    Queries all rows in trivia table and randomly picks one
    Returns json:
            { fact:{
                "number" : number,
                "fragment" : "fragment",
                "statement" : "statement",
                "type" : "type"
            }}

     If count param specified, returns JSON:
        {facts: [
                    {
                    "number" : number,
                    "fragment": "fragment",
                    "statement": "statement",
                    "type": "trivia",
                    },
                    {
                    "number" : number,
                    "fragment": "fragment",
                    "statement": "statement",
                    "type": "trivia",
                    },
                ...]
        }

        If count > MAX_BATCH, return MAX_BATCH count.
    """
    count = request.args.get("count")

    trivia_facts = Trivia.query.all()

    if not count:
        trivia_fact = random.choice(trivia_facts)

        fact = {
            "number": trivia_fact.number,
            "fragment": trivia_fact.fact_fragment,
            "statement": trivia_fact.fact_statement,
            "type": "trivia",
        }

        return jsonify(fact=fact)

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
    if count > len(trivia_facts):
        count = len(trivia_facts)

    facts = []

    random_trivia_facts = random.sample(trivia_facts, count)

    for trivia_fact in random_trivia_facts:
        fact = {
            "number": trivia_fact.number,
            "fragment": trivia_fact.fact_fragment,
            "statement": trivia_fact.fact_statement,
            "type": "trivia",
        }
        facts.append(fact)

    return jsonify(facts)
