from nums_api import app
from nums_api.database import db

# import all models - necessary for create_all()

db.drop_all(app=app)
db.create_all(app=app)
