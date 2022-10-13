from flask import Blueprint, jsonify, request
from sqlalchemy import and_
from nums_api.database import db
from nums_api.years.models import Year, YearLike
import random
import re
from nums_api.helpers.batch import get_batch_nums
from nums_api.config import MAX_BATCH


years = Blueprint("years", __name__)


@years.get("/<int:year>")
def get_year_fact(year):
    """ Route for getting a random fact about year.
    If fact found, returns JSON:
        {fact: {
            "year" : 1,
            "fragment": "text",
            "statement": "text",
            "type": year,
            }
        }

    If no fact found, returns error message:
    { error:
        { "message": "A fact for year not found",
          "status": 404
        }
    }
    """
    year_facts = Year.query.filter_by(year=year).all()

    if year_facts:
        year_fact = random.choice(year_facts)
        fact = {
            "year": year_fact.year,
            "fragment": year_fact.fact_fragment,
            "statement": year_fact.fact_statement,
            "type": "year",
        }
        return jsonify(fact=fact)
    else:
        error = {
            "status": 404,
            "message": f"A fact for { year } not found",
        }
        return (jsonify(error=error), 404)


@years.get("/<years>")
def get_years_range_facts(years):
    """ Route for getting a random fact about multiple years.
    Example years input:
      - 2000..2005  (min..max inclusive of both)
      - 1979,45,1800 (individual years separated by comma)
      - 1990..1992,1800,1805 (both and in either order)

    If facts found, returns JSON:
        {facts: [
                    {
                    "year" : 2000,
                    "fragment": "text",
                    "statement": "text",
                    "type": year,
                    },
                    {
                    "year" : 2001,
                    "fragment": "text3",
                    "statement": "text3",
                    "type": year,
                    },
                ...]
        }

    If no facts found for year range, returns JSON:
        {error:
            { "message": "No facts for { years } were found",
            "status": 404
            }
        }

    If invalid URL syntax for year range, returns JSON:
        {error:
            { "message": "Invalid URL",
            "status": 400
            }
        }
    """
    years_regex = r"^([0-9]{1,4})(\.\.[0-9]{1,4})?((,[0-9]{1,4})?)*(\.\.[0-9]{1,4})?$"

    if not re.match(years_regex, years):
        error = {
            "status": 400,
            "message": "Invalid URL",
        }
        return (jsonify(error=error), 400)

    try:
        years_range = get_batch_nums(years)
    except Exception:
        return (jsonify(
            error={
                "message": str(Exception),
                "status": 400
            }), 400)

    facts = []

    for year in years_range:
        year_facts = Year.query.filter_by(year=year).all()

        if year_facts:
            year_fact = random.choice(year_facts)
            fact = {
                "year": year_fact.year,
                "fragment": year_fact.fact_fragment,
                "statement": year_fact.fact_statement,
                "type": "year",
            }
            facts.append(fact)

    if not len(facts):
        error = {
            "status": 404,
            "message": f"No facts for { years } were found",
        }
        return (jsonify(error=error), 404)

    return jsonify(facts=facts)


@years.get("/random")
def get_year_fact_random():
    """ Route for getting random fact about a single year, accepts an optional
    parameter of count for getting count number of random facts.
    Returns JSON if no count param:
        { fact: {
            "year" : year,
            "fragment": "fragment",
            "statement": "statement",
            "type": "year",
            }}

    If count param specified, returns JSON:
        {facts: [
                    {
                    "year" : year,
                    "fragment": "fragment",
                    "statement": "statement",
                    "type": "year",
                    },
                    {
                    "year" : year,
                    "fragment": "fragment",
                    "statement": "statement",
                    "type": "year",
                    },
                ...]
        }

    If count > MAX_BATCH, return MAX_BATCH count of facts.
    If count > total number of year facts, return total number of facts.
    """
    count_query = request.args.get("count")

    years_facts = Year.query.all()

    if not count_query:
        year_fact = random.choice(years_facts)

        fact = {
            "year": year_fact.year,
            "fragment": year_fact.fact_fragment,
            "statement": year_fact.fact_statement,
            "type": "year",
        }

        return jsonify(fact=fact)

    try:
        count_query = int(count_query)
    except ValueError:
        return (jsonify(
            error={
                "message": f"{ count_query } is an invalid count number",
                "status": 400
            }), 400)

    if count_query < 1:
        return (jsonify(
            error={
                "message": f"{ count_query } is an invalid count number",
                "status": 400
            }), 400)

    if count_query > MAX_BATCH:
        count_query = MAX_BATCH
    if count_query > len(years_facts):
        count_query = len(years_facts)

    facts = []

    random_years_facts = random.sample(years_facts, count_query)

    for year_fact in random_years_facts:
        fact = {
            "year": year_fact.year,
            "fragment": year_fact.fact_fragment,
            "statement": year_fact.fact_statement,
            "type": "year",
        }
        facts.append(fact)

    return jsonify(facts=facts)

@years.post("/like")
def like_year_fact():
    """
    Allows users to like a specific fact.
    
    Accepts JSON:
        { "fact": {
            "year": number,
            "statement": "fact_statement",
        }}
        
    If matching year is invalid or fact statement are not provided, 
    returns error JSON, i.e:
            { "error": {
                    "message": "Invalid year",
                    "status": 400
            }}
        OR
            { "error": {
                    "message": "No matching fact found for 4."
                    "status": 400
            }}

    If successful, returns 201 and success message:
        {
            "status": "success"
        }
    """
    
    #TODO: JSON validation, currently route will accept any additional JSON not specified in docstring.

    try:
        fact_year = int(request.json["fact"]["year"])
    except ValueError:
        return (jsonify(
            error={
                "message": "Invalid year",
                "status": 400
            }), 400)
    except KeyError: 
        return (jsonify(
            error={
                "message": "Please provide year.",
                "status": 400
            }), 400)    

    try:
        fact_statement = request.json["fact"]["statement"] 
    except KeyError:
        return (jsonify(
            error={
                "message": "Please provide a fact statement.",
                "status": 400
            }), 400)

    fact = Year.query.filter(
            and_(
                Year.year == fact_year,
                Year.fact_statement.like(fact_statement)
                )).first()    

    if not fact:
        return (jsonify(error={
                "message": f"No matching fact found for {fact_year}.",
                "status": 400
            }), 400)   
    
    else: 
        new_like = YearLike(fact_id=fact.id)
        db.session.add(new_like)
        db.session.commit()
        return jsonify(status="success"), 201
 
    
