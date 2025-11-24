def merge_sort(lst, key=lambda x: x, reverse=False):
    if len(lst) > 1:  # Changed from <= 1 return to > 1 block
        mid = len(lst) // 2
        left = lst[:mid]
        right = lst[mid:]

        # Recurse on the slices (modifies them in place)
        merge_sort(left, key=key, reverse=reverse)
        merge_sort(right, key=key, reverse=reverse)

        # Merge the modified slices back into the main list
        merge(lst, left, right, key, reverse)


def merge(lst, left, right, key, reverse): # Added 'lst' as the target
    i = j = k = 0  # Added 'k' to track position in the main list

    while i < len(left) and j < len(right):
        if reverse:
            # Use key() for comparison
            condition = key(left[i]) >= key(right[j])
        else:
            condition = key(left[i]) <= key(right[j])

        if condition:
            lst[k] = left[i] # Overwrite lst instead of appending
            i += 1
        else:
            lst[k] = right[j] # Overwrite lst instead of appending
            j += 1
        k += 1

    # Handle remaining elements (cannot use + concatenation for in-place)
    while i < len(left):
        lst[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        lst[k] = right[j]
        j += 1
        k += 1

if __name__ == "__main__":
    # USage Examples:
    words = ["banana", "Apple", "grape", "orange"]
    merge_sort(words, key=str.lower)
    print(words)

    merge_sort(words, key=str.lower, reverse=True)
    print(words)
    nums = [5, 2, 100, 23, 1]
    merge_sort(nums)
    print(nums)

    merge_sort(nums, reverse=True)
    print(nums)

    people = [
        {"name": "Carlos", "age": 30},
        {"name": "Ana", "age": 20},
        {"name": "Luis", "age": 25}
    ]

    merge_sort(people, key=lambda x: x["age"])
    print(people)
