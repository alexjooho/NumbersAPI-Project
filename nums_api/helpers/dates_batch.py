from nums_api.dates.models import Date
from nums_api.config import MAX_BATCH


def get_batch_dates(num_ranges:str):
    """Parses a batch request string into a list of individual numbers
    For decimals, rounds to nearest integer.

        >>> get_batch_dates("1/13..1/15,2/20")
        [13, 14, 15, 51]

        >>> get_batch_dates("13/13..1/15,2/20")
        Traceback (most recent call last):
        ...
        Exception: Invalid date: 13/13

        >>> get_batch_dates("13/13..1/15..2/20")
        Traceback (most recent call last):
        ...
        Exception: Unexpected number of bounds in range: 3
    """
    dates = []
    count = 0
    ranges = num_ranges.split(",")

    for r in ranges:
        bounds = r.split("..")
        if len(bounds) == 1:
            if count == MAX_BATCH:
                return
            dates.append(convert_date_to_num(bounds[0]))

        elif len(bounds) == 2:
            min_date = convert_date_to_num(bounds[0])
            max_date = convert_date_to_num(bounds[1])
            for n in range(min_date, max_date + 1):
                if count == MAX_BATCH:
                    return
                dates.append(n)
                count += 1
        else:
            raise Exception("Unexpected number of bounds in range: " + str(len(bounds)))
    return dates

def convert_date_to_num(date):
    month = int(date.split("/")[0])
    day = int(date.split("/")[1])
    try:
        days = Date.date_to_day_of_year(month, day)
    except ValueError:
        raise Exception("Invalid date: " + str(date))
    return days