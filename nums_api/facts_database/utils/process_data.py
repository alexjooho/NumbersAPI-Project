import datetime
from nums_api.facts_database.utils.helpers import (
    pos_tags, load_json_data, convert_day_of_year_to_date)


def convert_data_files(paths, type):
    """Given a list of paths to json text files, returns a list of
    facts in the form of a dictionary.
        facts = [ fact, .... ]
        fact: {
            "number" or "year" or "day_of_year" depending on fact type,
            "fact_fragment": "fragment"
            "fact_statement": "statement"
            "was_submitted": True or False (bool)
            "year": "year" for facts of type = "dates"
        }
    """

    facts = []

    for path in paths:
        data = load_json_data(path)

        # for each number entry in data file
        for number_entry in data:

            # for each fact entry of a number entry (key)
            for fact_entry in data[number_entry]:

                if fact_entry["self"] == False:
                    fact = create_fact(number_entry, fact_entry, type)
                    facts.append(fact)

    return(facts)


def create_fact(number_entry, fact_entry, type):
    """Returns a dictionary object from a fact_entry, with the number_entry
    added as a type key.

    fact_entry of type == "dates" will also have an additional key ("years")

        fact: {
            "key": "number" or "year",
            "fact_fragment": "fragment",
            "fact_statement": "statement",
            "was_submitted": True or False (bool),
            "year": "year" for facts of type = "dates"
        }
    """

    if type == "dates":
        fact = {
            "day_of_year": number_entry,
            "year": fact_entry.get("year"),
            "fact_fragment": create_fragment(fact_entry),
            "fact_statement": create_statement(number_entry, fact_entry, type),
            "was_submitted": True if fact_entry.get("manual") == "true" else False
        }

    else:
        key = "year" if type == "years" else "number"
        fact = {
            key: number_entry,
            "fact_fragment": create_fragment(fact_entry),
            "fact_statement": create_statement(number_entry, fact_entry, type),
            "was_submitted": True if fact_entry.get("manual") == "true" else False
        }

    return fact


def create_fragment(fact_entry):
    """Returns a string fragment from a fact entry that has a key "text".

        fact_entry: {
            "text": "fact text",
            "self": "true" or "false",
            "pos": "Parts of speech" (optional),
            "manual": "true" or false" (optional)
        }
    """

    fragment = fact_entry["text"]
    words_pos_tags = pos_tags(fragment)
    first_word_pos = words_pos_tags[0][1]

    # if fact text ends of with a period, remove period for fragment
    if fragment[-1] == ".":
        fragment = fragment[0:-1]

    # if the first word pos is not a NNP/NNPS: noun, proper, singular/plural
    if first_word_pos not in ["NNP", "NNPS"]:
        fragment = fragment[0].lower() + fragment[1:]

    return fragment


def create_statement(number_entry, fact_entry, type):
    """Returns a string statement constructed from a fact entry with
    a key "text" .

        number_entry = "an entry data point"
        fact_entry: {
            "text": "fact text",
            "self": "true" or "false",
            "pos": "Parts of speech" (optional),
            "manual": "true" or false" (optional)
            }
    """

    fragment = create_fragment(fact_entry)

    if type == "years":
        # checks year vs current year to construct statement
        curr_year = datetime.date.today().year

        if int(number_entry) < 0 :
            return f"{-int(number_entry)} BC is the year that {fragment}."

        elif int(number_entry) > curr_year:
            return f"{number_entry} will be the year that {fragment}."

        else:
            return f"{number_entry} is the year that {fragment}."

    elif type == "dates":
        date = convert_day_of_year_to_date(int(number_entry))

        # checks if a year is provided with the date to construct statement
        if fact_entry.get("year"):
            year = int(fact_entry["year"])

            if year < 0:
                return f"{date} is the day in {-year} BC that {fragment}."
            else:
                return f"{date} is the day in {year} that {fragment}."

        else:
            return f"{date} is the day that {fragment}."

    return f"{number_entry} is {fragment}."

