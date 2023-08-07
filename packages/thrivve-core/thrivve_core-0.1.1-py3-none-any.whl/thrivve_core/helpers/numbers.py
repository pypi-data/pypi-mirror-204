def fix_number(number):
    if isinstance(number, float) or isinstance(number, int):
        return round(number, 2)

    return 0
