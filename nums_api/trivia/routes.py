from flask import Blueprint, jsonify
from nums_api.trivia.models import Trivia
from random import choice

trivia = Blueprint("trivia", __name__)


@trivia.get("/<number>")
def get_trivia_fact(number):
    """
    Route for getting trivia fact about a number.
    Returns json { number, fact } if number is valid, else will return error:
    { error: { message: f"A { category } fact for { number } not found", status: 404} }
    """
    
    trivia = Trivia.query.filter_by(number=number).first()
    
    if not trivia:
        error = {
            'error': {
                'message': f"A trivia fact for { number } not found",
                'status': 404
            }
        }
        
        return jsonify(error), 404

    return jsonify(number = number, fact = trivia.fact_statement)


@trivia.get("/random")
def get_trivia_fact_random():
    """
    Route for getting random trivia fact.
    Returns json { random: fact }
    """
    
    random_trivia = choice(Trivia.query.all())
    
    # session.query(Trivia).order_by(func.rand()).first()

    return jsonify( random = random_trivia.fact_fragment)