BATCH_LIMIT = 50

def get_batch_nums(num_ranges:str, parse_value=int):
    """Parses a batch request string into a list of individual numbers
    Example: Accepts ""13..15,20" and returns [13, 14, 15, 20]
    """

    nums = []
    count = 0
    ranges = num_ranges.split(",")

    for r in ranges:
        bounds = r.split("..")
        if len(bounds) == 1:
            if count == BATCH_LIMIT:
                return
            nums.append(parse_value(bounds[0]))

        elif len(bounds) == 2:
            min_bound = parse_value(bounds[0])
            max_bound = parse_value(bounds[1])
            for n in range(min_bound, max_bound + 1):
                if count == BATCH_LIMIT:
                    return
                nums.append(n)
                count += 1
        else:
            #TODO: ask how we should handle this
            print("Unexpected number of bounds in range: " + len(bounds))
    return nums

