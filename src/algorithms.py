def quick_sort(array, low, high):
    """Sorts a list recursively.

    Args:
        array (list): the list to be sorted.
        low (int): index of lowest item to be sorted
        high (int): index of highest item to be sorted.
    """
    def partition(array, low, high):
        """Partition array using a pivot value

        Args:
            array (list): the list to be sorted.
            low (int): index of lowest item to be sorted
            high (int): index of highest item to be sorted.

        Returns:
            The value of the pivot.
        """
        i = low + 1
        pivot = array[low]
        for j in range(low+1, high+1):
            if array[j] < pivot:
                array[j], array[i] = array[i], array[j]
                i += 1
        array[low], array[i-1] = array[i-1], array[low]
        return i - 1
    if low < high:
        pivot = partition(array, low, high)
        quick_sort(array, low, pivot-1)
        quick_sort(array, pivot+1, high)

def binary_search(search_term, array):
    """Searches for an item in an already sorted list.

    Args:
        search_term: term to be searched for in the list.
        array (list): list to be searched.
    """
    half_array = int(len(array)/2)
    if search_term == array[half_array]:
        return True
    elif len(array) == 1:
        return False
    elif search_term > array[half_array]:
        return binary_search(search_term, array[half_array:])
    else:
        return binary_search(search_term, array[:half_array])