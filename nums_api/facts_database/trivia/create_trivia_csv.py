import csv
from nums_api.facts_database.utils.process_data import convert_data_files

# Paths to text files with data in json form
DATA_PATHS = [
    "data/wikipedia_1_100.txt",
    "data/wikipedia_101_200.txt",
    "data/wikipedia_201_300.txt"
    ]

TRIVIA_CSV_HEADERS = [
    "number",
    "fact_fragment",
    "fact_statement",
    "was_submitted"
    ]

# Generate trivia.csv from list of dictionary data in trivia_facts
with open('trivia.csv', 'w') as trivia_csv:

    trivia_facts = convert_data_files(DATA_PATHS, "trivia")
    trivia_writer = csv.DictWriter(trivia_csv, fieldnames=TRIVIA_CSV_HEADERS)
    trivia_writer.writeheader()

    # write each fact from trivia_facts to a row in trivia.csv
    for fact in trivia_facts:
        trivia_writer.writerow(dict(
            number = fact["number"],
            fact_fragment = fact["fact_fragment"],
            fact_statement = fact["fact_statement"],
            was_submitted = fact["was_submitted"],
        ))
