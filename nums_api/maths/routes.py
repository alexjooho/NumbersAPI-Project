from flask import Blueprint, jsonify
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
            { 'error': {
                'message': f"A math fact for { number } not found",
                'status': 404 } }
    """
    num_facts = Math.query.filter_by(number=number).all()

    if num_facts:
        num_fact = random.choice(num_facts)
        fact = {'fact': {
            'number': num_fact.number,
            'fragment': num_fact.fact_fragment,
            'statement': num_fact.fact_statement,
            'type': 'math'
        }}
        return jsonify(fact)
    else:
        error = {'error': {
            'message': f"A math fact for { number } not found",
            'status': 404}}
        return (jsonify(error), 404)


@math.get("/random")
def get_math_fact_random():
    """Returns a random math fact in JSON about a random number.
        - Returns JSON response:
        { "fact": {
            "number": random number
            "fragment": fact_fragment
            "statement": fact_statement
            "type": "math"
        }}
    """

    num_fact = random.choice(Math.query.all())

    fact = {'fact': {
        'number': num_fact.number,
            'fragment': num_fact.fact_fragment,
            'statement': num_fact.fact_statement,
            'type': 'math'
            }}
    return jsonify(fact)


@math.get("/<num>")
def get_batch_math_fact(num):
    """Returns a random math fact in JSON about a a batch of numbers passed as a
    URL parameter.
        - If facts are found, returns JSON response:
        { "fact": {
            "number": number
            "fragment": fact_fragment
            "statement": fact_statement
            "type": "math"
        }}
        - If fact is not found, returns JSON response:
            { 'error': {
                'message': f"A math fact for { number } not found",
                'status': 404 } }
    """

    decimal_regex = r"^-?\d+(?:\.\d+)?(\.\.-?\d+(?:\.\d+)?)?(,-?\d+(?:\.\d+)?(\.\.-?\d+(?:\.\d+)?)?)*$"
    if not re.match(decimal_regex, num):
        error = {'error': {
            'message': f"A math fact not found.",
            'status': 404}}
        return (jsonify(error), 404)

    nums = get_batch_nums(num)

    # TODO: do something to get the facts

    return jsonify(nums)
