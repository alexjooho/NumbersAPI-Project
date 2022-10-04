from datetime import datetime
from nums_api.database import db


class Name(db.Model):
    """General trivia facts about names."""

    __tablename__ = "names"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    name = db.Column(
        db.String(100),
        nullable=False,
    )

    # fact with no prefix, first word lowercase, no punctuation at the end
    fact_fragment = db.Column(
        db.String(200),
        nullable=False,
        unique=True,
    )

    # fact with prefix, first word is number, has punctuation at the end
    fact_statement = db.Column(
        db.String(250),
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
