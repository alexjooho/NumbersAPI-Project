from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TSVECTOR

class TSVector(sa.types.TypeDecorator):
    impl = TSVECTOR

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
