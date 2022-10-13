from flask import Blueprint, jsonify, request
from nums_api.trivia.models import Trivia

search = Blueprint("search", __name__)

@search.get("/")
def get_search_results():
    """api/search/?query=aliquot"""
    
    args = request.args
    print("search query:", args)
    
    term = args["query"]
    print("search term:", term)
    
    results = Trivia.query.filter(Trivia.__ts_vector__.match(term)).all()
    print("results are:", results)
    
    return jsonify(results = "results")