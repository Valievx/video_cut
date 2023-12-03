from random import randint as random


def range_random():
    """Function for generating random ranges."""
    a = [random(36, 46), random(72, 82), random(96, 106)]
    b = [random(46, 56), random(82, 92), random(106, 108)]

    time_range = [(x, y) for x, y in zip(a, b)]

    return time_range


# Вызываем функцию и получаем случайные значения
time_ranges = range_random()

# Считаем общую сумму и вычисляем разницу между вторым и первым значением в каждом кортеже
full_time_clip = sum([y - x for x, y in time_ranges])
