from datetime import datetime
from nums_api.database import db, TSVector
from sqlalchemy import Index


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

    __ts_vector__ = db.Column(TSVector(),db.Computed(
         "to_tsvector('english', fact_statement)",
         persisted=True))
         
    __table_args__ = (Index('ix_trivia___ts_vector__',
          __ts_vector__, postgresql_using='gin'),)
