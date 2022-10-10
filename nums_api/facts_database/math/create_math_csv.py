import csv
from nums_api.facts_database.utils.process_data import convert_data_files

# Paths to text files with data in json form
DATA_PATHS = [
    "data/wikipedia_1_100.txt",
    "data/wikipedia_101_200.txt",
    "data/wikipedia_201_300.txt"
    ]

MATH_CSV_HEADERS = [
    "number",
    "fact_fragment",
    "fact_statement",
    "was_submitted"
    ]

# Generate math.csv from list of dictionary data in math_facts
with open('math.csv', 'w') as math_csv:

    math_facts = convert_data_files(DATA_PATHS, "math")
    math_writer = csv.DictWriter(math_csv, fieldnames=MATH_CSV_HEADERS)
    math_writer.writeheader()

    # write each fact from math_facts to a row in math.csv
    for fact in math_facts:
        math_writer.writerow(dict(
            number = fact["number"],
            fact_fragment = fact["fact_fragment"],
            fact_statement = fact["fact_statement"],
            was_submitted = fact["was_submitted"],
        ))
