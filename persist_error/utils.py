"""
Utility functions.

"""
import random


def search_dictionary_list(dict_list, search_key, search_value):
    """
    Search through a list of dictionary for particular key value pair.

    :param list dict_list: list of dictionaries
    :param str search_key: the key to search for
    :param search_value: the value to look for
    :return: a list of matching dictionaries
    :rtype: list

    """
    result = list(filter(lambda x: x[search_key] == search_value, dict_list))
    return result


def select_delay_seconds(low=300, high=900):
    """
    Randomly select message delay seconds within the
    given interval (inclusive on both bounds).

    :param int low: inclusive lower bound; defaults to 300 seconds
    :param int high: inclusive upper bound; defaults to 900 seconds -- the maximum delay allowed by SQS
    :return: random number between the interval
    :rtype: int

    """
    return random.randint(low, high)
