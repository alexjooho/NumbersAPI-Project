from flask import Blueprint, jsonify, request
from nums_api.dates.models import Date
from nums_api.maths.models import Math
from nums_api.trivia.models import Trivia
from nums_api.years.models import Year

search = Blueprint("search", __name__)


@search.get("/")
def get_search_results():
    """Search all databases for facts using keywords with full text search
    functionality.
    Returns results in JSON response.

    Example search URL: api/search/?query=hinduism

    Response:
    {
  "results": {
    "dates": [],
    "math": [],
    "trivia": [
      {"statement": "8 is in Hinduism, it is the number of wealth, abundance.",
        "type": "trivia"}
        ],
    "years": [
        {"statement": "200 is the year that brahmanism evolves into Hinduism (approximate date).",
        "type": "years"
      }]}
      }
    """

    args = request.args
    print("search query:", args)

    term = args["query"]
    print("search term:", term)

    dates_results = Date.query.filter(Date.__ts_vector__.match(term)).all()
    math_results = Math.query.filter(Math.__ts_vector__.match(term)).all()
    trivia_results = Trivia.query.filter(
        Trivia.__ts_vector__.match(term)).all()
    years_results = Year.query.filter(Year.__ts_vector__.match(term)).all()

    dates_results = create_results_array(dates_results, "date")
    math_results = create_results_array(math_results, "math")
    trivia_results = create_results_array(trivia_results, "trivia")
    years_results = create_results_array(years_results, "years")

    results = {
        "dates": dates_results,
        "math": math_results,
        "trivia": trivia_results,
        "years": years_results
    }

    return jsonify(results=results)


def create_results_array(results, oftype):
    """Create a List from results of search query"""
    return [{"statement": r.fact_statement,
             "type": oftype
             }
            for r in results]
