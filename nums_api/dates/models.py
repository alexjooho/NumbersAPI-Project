from datetime import datetime
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST


class Date (db.Model):
    """Date facts."""

    __tablename__ = "dates"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    # store date as integer that represents the 1-indexed day of a leap year
    # 1 - 366: February 28th is always 59 & March 1st is always 61
    # can't use date field, we're dealing with some historical dates- think about
    # the calendar changes across history (Postgres  follows the Gregorian
    # calendar rules for all dates,)
    day_of_year = db.Column(
        db.Integer,
        nullable=False,
    )

    year = db.Column(
        db.Integer,
        nullable=False,
    )

    # fact with no prefix, first word lowercase, no punctuation at the end
    fact_fragment = db.Column(
        db.String(200),
        nullable=False,
    )

    # fact with prefix, first word is number, has punctuation at the end
    fact_statement = db.Column(
        db.String(250),
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

    @classmethod
    def date_to_day_of_year(cls, month, day):
        """
        Converts month and day to day of the year (1-366)

            >>> Date.date_to_day_of_year(1, 1)
            1

            >>> Date.date_to_day_of_year(2, 28)
            59

            >>> Date.date_to_day_of_year(2, 29)
            60

            >>> Date.date_to_day_of_year(3, 1)
            61

            >>> Date.date_to_day_of_year(12, 31)
            366
        """