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
from nums_api.dates.models import Date

# create app and add configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


# request tracking

@app.before_request
def track_request():
    """Track request item and category, update total number of requests in DB."""
    #intercept request
    #ignore random
    #check route for category
    #check the endpoint for req_item
    #write both to DB and increment num_reqs
    
    #if in DB, increment
    #if not in DB, create
    PATH_SPLIT_INDEX = 5
    VALID_CATEGORIES = ["dates", "trivia", "years", "names", "math"]
    
    [category, req_item] = request.path.lower()[PATH_SPLIT_INDEX:].split("/",1)
    
    print("category:", category, "req_item:", req_item)
    
    if req_item == "random":
        return
    
    if category not in VALID_CATEGORIES:
        return
    
    if category == "date":
        [month, day] = req_item.split("/")
        req_item = Date.date_to_day_of_year(int(month), int(day))
        
    print("POST PASS:","category:", category, "req_item:", req_item)
    
    print("request method:", request.method)
    print("HERE IS BEFORE REQUEST")


# register blueprints
app.register_blueprint(root)
app.register_blueprint(trivia, url_prefix='/api/trivia')
app.register_blueprint(math, url_prefix='/api/math')
app.register_blueprint(dates, url_prefix='/api/dates')
app.register_blueprint(years, url_prefix='/api/years')

# allow CORS and connect app to database
CORS(app)
connect_db(app)
