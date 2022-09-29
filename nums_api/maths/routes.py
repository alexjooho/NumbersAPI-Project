from flask import Blueprint, jsonify
from nums_api.maths.models import Math
from sqlalchemy.sql import func

math = Blueprint("math", __name__)


@math.get("/<int:number>")
def get_math_fact(number):
    """ GET route for a given number
    - validate the number (must be an integer)
    - query the number in Math Model
    - if query found, return JSON response with number data
        {number, fact_fragment, fact_statement, type}
    - else, return 404 err
    """
    num_fact = Math.query.filter_by(number = number).one_or_none()

    if num_fact:
        num = {
            'number': num_fact.number,
            'fact_fragment': num_fact.fact_fragment,
            'fact_statement': num_fact.fact_statement,
            'type': 'math'
        }
        return (jsonify(num), 200)
    else:
        error = { 'error': {
                    'message': f"A math fact for { number } not found",
                    'status': 404 } }
        return (jsonify(error), 404)

    # discuss JSON structure above ^ add type: math


@math.get("/random")
def get_math_fact_random():
    """ GET route for a random number
    - query random record from Math Model
    - create dict and return JSON response with number data
        {number, fact_fragment, fact_statement, type}
    """

    num_fact = Math.query.order_by(func.random()).first()

    num = {
            'number': num_fact.number,
            'fact_fragment': num_fact.fact_fragment,
            'fact_statement': num_fact.fact_statement,
            'type': 'math'
        }
    return (jsonify(num), 200)
