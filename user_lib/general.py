from dateutil.parser import parse


def dictionary_merge(dictionaries):
    try:
        results = {}
        for d in dictionaries:
            results = {**results, **d}
        return results
    except Exception as e:
        print(e)


# move to calendar
def is_date(string, fuzzy=True):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False


# move to calendar
def parse_date(string, fuzzy=True):
    """
    recieves amy format

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        return parse(string, fuzzy=fuzzy)
    except Exception as e:
        print(e)
