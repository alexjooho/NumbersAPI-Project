import math
from nums_api.maths.models import Math
import random
<<<<<<< HEAD

BATCH_LIMIT = 50
=======
from nums_api.config import MAX_BATCH as BATCH_LIMIT

>>>>>>> 9f45e0deec7280ccc50d3cacaa685578aef08f71

def get_batch_nums(num_ranges:str):
    """Parses a batch request string into a list of individual numbers
    For decimals, rounds to nearest integer.
    Ex 1: Accepts "13..15,20" and returns [13, 14, 15, 20]
    Ex 2: Accepts "3.14..7,10" returns [3.14, 4, 5, 6, 7, 10]
    Ex 3: Accepts "0..4,3.14" returns [0, 1, 2, 3, 4, 3.14]
    """
    nums = []
    count = 0
    ranges = num_ranges.split(",")

    for r in ranges:
        bounds = r.split("..")
        if len(bounds) == 1:
            if count == BATCH_LIMIT:
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
                if count == BATCH_LIMIT:
                    return
                nums.append(n)
                count += 1
            if isinstance(max_num, float):
                nums.append(max_num)
        else:
            raise Exception("Unexpected number of bounds in range: " + len(bounds))
    return nums

def int_or_float(num_string):
    """Turns a number string into an int or float.
    Ex 1: "3.14" -> 3.14
    Ex 2: "10" -> 10
    """
    try:
        return int(num_string)
    except ValueError:
        return float(num_string)

<<<<<<< HEAD

=======
#--------------------------------------------------
# Need to move this somwehre
def get_facts(num, type):
    """ Get a fact for a single number """

    facts = Math.query.filter_by(number=num).all()

    if facts:
        random_fact = random.choice(facts)
        fact = {'fact': {
            f"{type}": random_fact.number,
            'fragment': random_fact.fact_fragment,
            'statement': random_fact.fact_statement,
            'type': type
        }}
        return fact
>>>>>>> 9f45e0deec7280ccc50d3cacaa685578aef08f71
