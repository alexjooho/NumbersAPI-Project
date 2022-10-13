from datetime import datetime
from nums_api.database import db


class Year (db.Model):
    """Year facts."""

    __tablename__ = "years"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    year = db.Column(
        db.Integer,
        nullable=False,
    )

    # fact with no prefix, first word lowercase, no punctuation at the end
    fact_fragment = db.Column(
        db.String(500),
        nullable=False,
    )

    # fact with prefix, first word is number, has punctuation at the end
    fact_statement = db.Column(
        db.String(550),
        nullable=False,
    )

    added_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    was_submitted = db.Column(
        db.Boolean,
        nullable=False,
    )
    
class YearLike(db.Model):
    """Likes for year facts about numbers."""

    __tablename__ = "year_likes"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    
    fact_id = db.Column(
        db.Integer,
        db.ForeignKey("years.id")
    )
    
    category = db.Column(
        db.String(5),
        nullable=False,
        default="year"
    )
    
    like_timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    like = db.relationship("Year", backref="likes")