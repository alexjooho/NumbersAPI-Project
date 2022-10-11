import math
from nums_api.config import MAX_BATCH


def get_batch_nums(num_ranges:str):
    """Parses a batch request string into a list of individual numbers
    For decimals, rounds to nearest integer.

        >>> get_batch_nums("3.14..7,10")
        [3.14, 4, 5, 6, 7, 10]

        >>> get_batch_nums("0..4,3.14")
        [0, 1, 2, 3, 4, 3.14]

        >>> get_batch_nums("0..10..15")
        Traceback (most recent call last):
        ...
        Exception: Unexpected number of bounds in range: 3
    """
    nums = []
    count = 0
    ranges = num_ranges.split(",")

    for r in ranges:
        bounds = r.split("..")
        if len(bounds) == 1:
            if count == MAX_BATCH:
                return
            nums.append(int_or_float(bounds[0]))

        elif len(bounds) == 2:
            min_num = int_or_float(bounds[0])
            max_num = int_or_float(bounds[1])
            if isinstance(min_num, float):
                nums.append(min_num)
            min_bound = math.ceil(min_num)
            max_bound = math.floor(max_num)
            for n in range(min_bound, max_bound + 1):
                if count == MAX_BATCH:
                    return
                nums.append(n)
                count += 1
            if isinstance(max_num, float):
                nums.append(max_num)
        else:
            raise Exception("Unexpected number of bounds in range: " + str(len(bounds)))
    return nums

def int_or_float(num_string):
    """Turns a number string into an int or float.

        >>> int_or_float("10")
        10

        >>> int_or_float("10.0")
        10.0

        >>> int_or_float("3.14")
        3.14
    """
    try:
        return int(num_string)
    except ValueError:
        return float(num_string)
