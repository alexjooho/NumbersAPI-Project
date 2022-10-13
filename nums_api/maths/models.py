from datetime import datetime
from nums_api.database import db


class Math(db.Model):
    """Math facts about numbers."""

    __tablename__ = "math"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    number = db.Column(
        db.Numeric,
        nullable=False,
    )

    # fact with no prefix, first word lowercase, no punctuation at the end
    fact_fragment = db.Column(
        db.String(300),
        nullable=False,
        unique=False,
    )

    # fact with prefix, first word is number, has punctuation at the end
    fact_statement = db.Column(
        db.String(350),
        nullable=False,
        unique=True,
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

class MathLike(db.Model):
    """Likes for math facts about numbers."""

    __tablename__ = "math_likes"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    
    fact_id = db.Column(
        db.Integer,
        db.ForeignKey("math.id", ondelete="cascade")
    )
    
    category = db.Column(
        db.String(5),
        nullable=False,
        default="math"
    )
    
    like_timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    like = db.relationship("Math", backref="likes")
