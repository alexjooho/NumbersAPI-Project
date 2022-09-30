from flask import Blueprint, jsonify
from nums_api.trivia.models import Trivia
from random import choice

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
    Route for getting random trivia fact.
    Queries all rows in trivia table and randomly picks one
    Returns json:
    { fact: { number, fragment, statement, type } }
    """

    random_trivia = choice(Trivia.query.all())

    fact = {
        "number": random_trivia.number,
        "fragment": random_trivia.fact_fragment,
        "statement": random_trivia.fact_statement,
        "type": "trivia"
    }

    return jsonify(fact=fact)
