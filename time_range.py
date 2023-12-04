from random import randint as random


def range_random() -> list:
    """Function for generating random ranges."""
    a = [random(36, 46), random(72, 82), random(96, 106)]
    b = [random(46, 56), random(82, 92), random(106, 108)]

    time_range = [(x, y) for x, y in zip(a, b)]

    return time_range
