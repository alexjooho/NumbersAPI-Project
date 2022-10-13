from datetime import datetime
from nums_api.database import db


class Trivia(db.Model):
    """General trivia facts about numbers."""

    __tablename__ = "trivia"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    number = db.Column(
        db.Integer,
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

class TriviaLike(db.Model):
    """Likes for trivia facts about numbers."""

    __tablename__ = "trivia_likes"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    
    fact_id = db.Column(
        db.Integer,
        db.ForeignKey("trivia.id")
    )
    
    category = db.Column(
        db.String(7),
        nullable=False,
        default="trivia"
    )
    
    like_timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    like = db.relationship("Trivia", backref="likes")