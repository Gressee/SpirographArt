"""
some general basic functions
"""


def clamp(val, min, max):
    if val < min:
        val = min
    elif val > max:
        val = max

    return val
