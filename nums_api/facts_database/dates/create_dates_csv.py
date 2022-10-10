import csv
from nums_api.facts_database.utils.process_data import convert_data_files

# Paths to text files with data in json form
DATA_PATHS = [
    "data/wikipedia_1_100.txt",
    "data/wikipedia_101_200.txt",
    "data/wikipedia_201_300.txt",
    "data/wikipedia_301_400.txt",
    ]

DATES_CSV_HEADERS = [
    "day_of_year",
    "year",
    "fact_fragment",
    "fact_statement",
    "was_submitted"
    ]

# Generate dates.csv from list of dictionary data in dates_facts
with open('dates.csv', 'w') as dates_csv:

    dates_facts = convert_data_files(DATA_PATHS, "dates")
    dates_writer = csv.DictWriter(dates_csv, fieldnames=DATES_CSV_HEADERS)
    dates_writer.writeheader()

    # write each fact from date_facts to a row in dates.csv
    for fact in dates_facts:
        dates_writer.writerow(dict(
            day_of_year = fact["day_of_year"],
            year = fact["year"],
            fact_fragment = fact["fact_fragment"],
            fact_statement = fact["fact_statement"],
            was_submitted = fact["was_submitted"],
        ))
