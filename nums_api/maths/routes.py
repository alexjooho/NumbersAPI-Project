from flask import Blueprint, jsonify, request
from nums_api.maths.models import Math
import random

math = Blueprint("math", __name__)


@math.get("/<int:number>")
def get_math_fact(number):
    """Returns a random math fact in JSON about a number passed as a
    URL parameter.
    Accepts optional query parameter: notfound = "floor" or "ceil",
    returns the previous or next found number if number not found.

    - If math fact is found and/or notfound query is provided,
    returns JSON response:
        { "fact": {
            "number": number
            "fragment": fact_fragment
            "statement": fact_statement
            "type": "math"
        }}

    - If math fact is not found and notfound query is not provided,
    returns JSON response:
        { 'error': {
            'message': f"A math fact for { number } not found",
            'status': 404 } }
    """
    num_facts = Math.query.filter_by(number=number).all()
    notfound_query = request.args.get('notfound')

    if notfound_query == "floor" and not num_facts:
        num_query = (
            Math.query
                .filter(Math.number < number)
                .order_by(Math.number.desc())
                .first())
        if num_query:
            num_facts = Math.query.filter_by(number=num_query.number).all()

    if notfound_query == "ceil" and not num_facts:
        num_query = (
            Math.query
                .filter(Math.number > number)
                .order_by(Math.number.asc())
                .first())
        if num_query:
            num_facts = Math.query.filter_by(number=num_query.number).all()

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


@ math.get("/random")
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
