# by: isaac timothy lyne 
# https://github.com/IsaacTimothyLyne

"""
Python implementation of the bubble sorting algorithm.
This module contains a function that takes a list of numbers as input and returns a sorted list.
"""

def bubble_sort(items, order='asc'):
    """
    Sorts a list of numbers using the bubble sorting algorithm.

    Args:
        items (list): A list of numbers to be sorted.
        order (str): The order to sort the list. Can be either 'asc' for ascending or 'desc' for descending.
                     Defaults to 'asc'.

    Returns:
        list: A sorted list of numbers.
    """
    if order == 'asc':
        for i in range(len(items)):
            for j in range(len(items)-i-1):
                if items[j] > items[j+1]:
                    items[j], items[j+1] = items[j+1], items[j]
    elif order == 'desc':
        for i in range(len(items)):
            for j in range(len(items)-i-1):
                if items[j] < items[j+1]:
                    items[j], items[j+1] = items[j+1], items[j]
    else:
        raise ValueError("Invalid order specified. Must be either 'asc' or 'desc'.")

    return items
