from flask import Blueprint, jsonify

from nums_api.maths.routes import Math

math = Blueprint("math", __name__)


@math.get("/<number>")
def get_math_fact(number):
    """FIXME
    Stub route for getting math fact about number.
    """
    numData = Math.query.filter_by(number = number).one_or_none()

    if numData:
        # structure
        return jsonify(numData, 200)
    else:
        error = { 'error': {
                    'message': f"A number fact for { number } not found",
                    'status': 404 } }
        return (jsonify(error), 404)

    # discuss JSON structure above ^


@math.get("/random")
def get_math_fact_random():
    """FIXME
    Stub route for getting math fact about random number.
    """

    return "Some interesting math fact about a random number."
