from flask import Flask, request
from flask_cors import CORS

from nums_api.config import DATABASE_URL
from nums_api.database import connect_db
from nums_api.trivia.routes import trivia
from nums_api.maths.routes import math
from nums_api.dates.routes import dates
from nums_api.years.routes import years
from nums_api.root.routes import root
from nums_api.tracking.models import Tracking
from nums_api.helpers.batch import get_batch_nums
from nums_api.helpers.dates_batch import get_batch_dates

# create app and add configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


# register blueprints
app.register_blueprint(root)
app.register_blueprint(trivia, url_prefix='/api/trivia')
app.register_blueprint(math, url_prefix='/api/math')
app.register_blueprint(dates, url_prefix='/api/dates')
app.register_blueprint(years, url_prefix='/api/years')

# request tracking
@app.after_request
def track_request(response):
    """Track request item and category, update total number of requests in DB."""
    
    PATH_SPLIT_INDEX = 5
    
    if request.method != 'GET':
        return response
    
    # ignore responses from requests for things like css files
    try:
        if not response.json:
            return response
    except:
        pass

    # ignore invalid requests like /api/math/banana
    # also ignores requests to routes that don't have data like /api/math/23423423
    try:
        response.json["error"]
        return response
    except:
        pass

    # ensure route is parsable (/api/category/req_item(s)), otherwise return:
    try:
        [category, req_item] = request.path.lower()[PATH_SPLIT_INDEX:].split("/",1)
    except ValueError:
        return response
    
    # ignore responses for random:
    if req_item == "random":
        return response

    # req_item can be a single number like "5", or a batch request like "1..5, 9"
    # for simplicity, pass either format to get_batch_nums or get_batch_dates since 
    # there is useful logic there for converting dates and handing ints and floats
    if category != "dates":
        # takes in a string of numbers like "1..3, 5" and sets batch_container 
        # equal to a list of every number implied by the ".." like: [1, 2, 3, 5]
        batch_container = get_batch_nums(req_item)
    else:
        # takes in dates like "1/1..1/3, 1/5" and sets batch_container equal to a 
        # list of days represented as one of 366 like: [1, 2, 3, 5]
        batch_container = get_batch_dates(req_item)

    # loop through batch_container and write to DB:
    for item in batch_container:
        Tracking.update_request_count(item, category)

    return response
    

# allow CORS and connect app to database
CORS(app)
connect_db(app)

