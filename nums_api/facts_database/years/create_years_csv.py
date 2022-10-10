import csv
from nums_api.facts_database.utils.process_data import convert_data_files

# Paths to text files with data in json form
DATA_PATHS = [
    "data/wikipedia_-99_0.txt",
    "data/wikipedia_1_100.txt",
    "data/wikipedia_101_200.txt",
    "data/wikipedia_201_300.txt",
    "data/wikipedia_301_400.txt",
    "data/wikipedia_401_500.txt",
    "data/wikipedia_501_600.txt",
    "data/wikipedia_601_700.txt",
    "data/wikipedia_701_800.txt",
    "data/wikipedia_801_900.txt",
    "data/wikipedia_901_1000.txt",
    "data/wikipedia_1001_1100.txt",
    "data/wikipedia_1101_1200.txt",
    "data/wikipedia_1201_1300.txt",
    "data/wikipedia_1301_1400.txt",
    "data/wikipedia_1401_1500.txt",
    "data/wikipedia_1501_1600.txt",
    "data/wikipedia_1601_1700.txt",
    "data/wikipedia_1701_1800.txt",
    "data/wikipedia_1801_1900.txt",
    "data/wikipedia_1901_2000.txt",
    "data/wikipedia_2001_2100.txt",
    ]

YEARS_CSV_HEADERS = [
    "year",
    "fact_fragment",
    "fact_statement",
    "was_submitted"
    ]

# Generate years.csv from list of dictionary data in years_facts
with open('years.csv', 'w') as years_csv:

    years_facts = convert_data_files(DATA_PATHS, "years")
    years_writer = csv.DictWriter(years_csv, fieldnames=YEARS_CSV_HEADERS)
    years_writer.writeheader()

    # write each fact from math_facts to a row in math.csv
    for fact in years_facts:
        years_writer.writerow(dict(
            year = fact["year"],
            fact_fragment = fact["fact_fragment"],
            fact_statement = fact["fact_statement"],
            was_submitted = fact["was_submitted"],
        ))
