from flask import Blueprint, jsonify, request
from nums_api.trivia.models import Trivia
from random import choice

trivia = Blueprint("trivia", __name__)


@trivia.get("/<int:number>")
def get_trivia_fact(number):
    """Returns a random trivia fact in JSON about a number passed as a
    URL parameter.
    If the URL parameter is not a positive integer, it will return a 404 error.
    Accepts optional query parameter: notfound = "floor" or "ceil",
    returns the previous or next found number if number not found.

    - If url parameter is valid and/or notfound query is provided, returns json:
        { "fact": {
            "number": number
            "fragment": fact_fragment
            "statement": fact_statement
            "type": "math"
        }}

    - Otherwise, if url parameter is invalid and notfound query is not provided,
    returns an error:
        { 'error': {
            'message': f"A trivia fact for { number } not found",
            'status': 404 } }
    """
    trivia = Trivia.query.filter_by(number=number).all()
    notfound_query = request.args.get('notfound')

    if notfound_query == "floor" and not trivia:
        num_query = (
            Trivia.query
                .filter(Trivia.number < number)
                .order_by(Trivia.number.desc())
                .first())
        if num_query:
            trivia = Trivia.query.filter_by(number=num_query.number).all()

    if notfound_query == "ceil" and not trivia:
        num_query = (
            Trivia.query
                .filter(Trivia.number > number)
                .order_by(Trivia.number.asc())
                .first())
        if num_query:
            trivia = Trivia.query.filter_by(number=num_query.number).all()

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
