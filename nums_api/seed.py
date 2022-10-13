from nums_api import app
from nums_api.database import db
from nums_api.maths.models import Math, MathLike
from nums_api.trivia.models import Trivia
from nums_api.years.models import Year
from nums_api.dates.models import Date
from csv import DictReader

# import all models - necessary for create_all()

db.drop_all(app=app)
db.create_all(app=app)


# inserts math facts from math.csv into 'math' table in DB
with open('facts_database/math/math.csv') as math:
    math_facts = []

    for data in DictReader(math):
        fact = {
            "number": data["number"],
            "fact_fragment": data["fact_fragment"],
            "fact_statement": data["fact_statement"],
            "was_submitted": True if data["was_submitted"] == "True" else False
        }
        math_facts.append(fact)

    db.session.bulk_insert_mappings(Math, math_facts)


# inserts trivia facts from trivia.csv into 'trivia' table in DB
with open('facts_database/trivia/trivia.csv') as trivia:
    trivia_facts = []

    for data in DictReader(trivia):
        fact = {
            "number": data["number"],
            "fact_fragment": data["fact_fragment"],
            "fact_statement": data["fact_statement"],
            "was_submitted": True if data["was_submitted"] == "True" else False
        }
        trivia_facts.append(fact)

    db.session.bulk_insert_mappings(Trivia, trivia_facts)


# inserts year facts from years.csv into 'years' table in DB
with open('facts_database/years/years.csv') as years:
    years_facts = []

    for data in DictReader(years):
        fact = {
            "year": data["year"],
            "fact_fragment": data["fact_fragment"],
            "fact_statement": data["fact_statement"],
            "was_submitted": True if data["was_submitted"] == "True" else False
        }
        years_facts.append(fact)

    db.session.bulk_insert_mappings(Year, years_facts)


# inserts dates facts from dates.csv into 'dates' table in DB
with open('facts_database/dates/dates.csv') as dates:
    dates_facts = []

    for data in DictReader(dates):
        fact = {
            "day_of_year": data["day_of_year"],
            "year": data["year"],
            "fact_fragment": data["fact_fragment"],
            "fact_statement": data["fact_statement"],
            "was_submitted": True if data["was_submitted"] == "True" else False
        }
        dates_facts.append(fact)

    db.session.bulk_insert_mappings(Date, dates_facts)


db.session.commit()