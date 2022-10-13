from flask import Blueprint, jsonify, request
from nums_api.config import MAX_BATCH
from nums_api.helpers.batch import get_batch_nums
from nums_api.maths.models import Math, MathLike
import random
import re

from sqlalchemy import and_
#TODO: how to import this from database.py?
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

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

    if facts:
        fact = random.choice(facts)
        factInfo = {
            "number": fact.number,
            "fragment": fact.fact_fragment,
            "statement": fact.fact_statement,
            "type": "math"
        }
        return jsonify(fact=factInfo)
    else:
        error = {
            "status": 404,
            "message": f"A math fact for { number } not found",
        }
        return (jsonify(error=error), 404)


@math.get("/<batch>")
def get_batch_math_fact(batch):
    """Returns a random math fact in JSON about a a batch of numbers passed as a
    URL parameter.
        - If facts are found, returns JSON response:
        { "facts": [
            {
                "number": "1",
                "fragment": "fact_fragment",
                "statement": "fact_statement",
                "type": "math"
            },
            {
                "number": "2",
                "fragment": "fact_fragment",
                "statement": "fact_statement",
                "type": "math"
            }, ...]
        }

        - If fact is not found, returns JSON response:
            { "error": {
                "message": "Invalid URL",
                "status": 400 } }

        - If one decimal number is passed, returns JSON response:
            { "fact": {
                "number": number,
                "fragment": "fact_fragment",
                "statement": "fact_statement",
                "type": "math"
            }}
    """

    decimal_regex = r"^-?\d+(?:\.\d+)?(\.\.-?\d+(?:\.\d+)?)?(,-?\d+(?:\.\d+)?(\.\.-?\d+(?:\.\d+)?)?)*$"

    if not re.match(decimal_regex, batch):
        error = {
            "message": "Invalid URL",
            "status": 400}
        return (jsonify(error=error), 400)

    try:
        nums_range = get_batch_nums(batch)
    except Exception:
        return (jsonify(
            error={
                "message": str(Exception),
                "status": 400
            }), 400)

    facts = []

    for num in nums_range:
        math_facts = Math.query.filter_by(number=num).all()

        if math_facts:
            fact = random.choice(math_facts)

            factInfo = {
                "number": fact.number,
                "fragment": fact.fact_fragment,
                "statement": fact.fact_statement,
                "type": "math"
            }

            facts.append(factInfo)

    if not len(facts):
        error = {
            "status": 404,
            "message": f"No facts for { batch } were found",
        }
        return (jsonify(error=error), 404)

    # Returns a single fact for requests with single numbers with decimal points
    # that did not go through the get_math_fact() route function.
    if len(facts) == 1:
        return jsonify(fact=facts[0])

    return jsonify(facts=facts)


@math.get("/random")
def get_math_fact_random():
    """
    Accepts a parameter "count" for number of random facts requested.

    Returns a random math fact in JSON about a random number.
        - Returns JSON response:
        { "fact": {
            "number": number,
            "fragment": "fact_fragment",
            "statement": "fact_statement",
            "type": "math"
        }}

    If count param specified, returns JSON:
        {facts: [
                    {
                    "number" : number,
                    "fragment": "fragment",
                    "statement": "statement",
                    "type": "math",
                    },
                    {
                    "number" : number,
                    "fragment": "fragment",
                    "statement": "statement",
                    "type": "math",
                    },
                ...]
        }

    If count > MAX_BATCH, returns MAX_BATCH number of requests.
    """
    count = request.args.get("count")
    numbers_facts = Math.query.all()

    if not count:
        number_fact = random.choice(numbers_facts)

        fact = {
            "number": number_fact.number,
            "fragment": number_fact.fact_fragment,
            "statement": number_fact.fact_statement,
            "type": "math",
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
    if count > len(numbers_facts):
        count = len(numbers_facts)

    facts = []

    random_numbers_facts = random.sample(numbers_facts, count)

    for number_fact in random_numbers_facts:
        fact = {
            "number": number_fact.number,
            "fragment": number_fact.fact_fragment,
            "statement": number_fact.fact_statement,
            "type": "math",
        }
        facts.append(fact)

    return jsonify(facts=facts)


@math.post("/like")
def like_math_fact():
    """
    Allows users to like a specific fact.
    
    Accepts JSON:
        { "fact": {
            "number": number,
            "statement": "fact_statement",
        }}
        
    If matching number is invalid or fact statement are not provided, 
    returns error JSON:
            { "error": {
                    "message": "Invalid number",
                    "status": 400
            }}
        OR
            { "error": {
                    "message": "No matching fact found for 4."
            }}

    If successful, returns 201 and success message:
        {
            "status": "success"
        }
    

    """
    
    #TODO: JSON validation, currently route will accept any additional JSON not specified in docstring.

    try:
        fact_number = int(request.json["fact"]["number"])
    except ValueError:
        try:
            fact_number = float(request.json["fact"]["number"]) 
        except ValueError:
            return (jsonify(
                error={
                    "message": "Invalid number",
                    "status": 400
                }), 400)

    try:
        fact_statement = request.json["fact"]["statement"] 
    except KeyError:
        return (jsonify(
            error={
                "message": "Invalid fact statement",
                "status": 400
            }), 400)
            

    fact = Math.query.filter(
            and_(
                Math.number == fact_number,
                Math.fact_statement.like(fact_statement)
                )).first()    

    if not fact:
        return jsonify(error={"message": f"No matching fact found for {fact_number}."})   
    
    else: 
        new_like = MathLike(fact_id=fact.id)
        db.session.add(new_like)
        db.session.commit()
        return jsonify(status="success"), 201
 
    