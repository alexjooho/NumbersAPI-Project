import nltk, json
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


def pos_tags(text):
    """Returns the parts of speech of all the words in the text.
    Example: [('first word', 'POS'), ...]
    """

    words_list = word_tokenize(text)
    words_pos_tags = nltk.pos_tag(words_list)
    return words_pos_tags

def load_json_data(path):
    """Loads a text file with data in json form and
    returns a list of iterable dictionaries."""

    with open(path, 'r') as file:
        json_data = file.read()
        data = json.loads(json_data)
        return data

def convert_day_of_year_to_date(day_of_year):
    """Converts a day of the year (1-366) to a date (month day).

        >>> convert_day_of_year_to_date(1)
        "January 1"

        >>> convert_day_of_year_to_date(59)
        "February 28"

        >>> convert_day_of_year_to_date(60)
        "February 29"

        >>> convert_day_of_year_to_date(61)
        "March 1"

        >>> convert_day_of_year_to_date(366)
        "December 31"
    """

    DAYS_IN_MONTHS = [31,29,31,30,31,30,31,31,30,31,30,31]
    MONTHS = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
        ]

    i = 0
    days_in_month = DAYS_IN_MONTHS[i]
    day = day_of_year

    while day > days_in_month:
        i+=1
        day = day - days_in_month
        days_in_month = DAYS_IN_MONTHS[i]

    date = f"{MONTHS[i]} {day}"

    return date