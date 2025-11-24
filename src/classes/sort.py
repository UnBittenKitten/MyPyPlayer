def merge_sort(lst, key=lambda x: x, reverse=False):
    if len(lst) <= 1:
        return lst
    
    mid = len(lst) // 2
    left = merge_sort(lst[:mid], key=key, reverse=reverse)
    right = merge_sort(lst[mid:], key=key, reverse=reverse)
    
    return merge(left, right, key, reverse)


def merge(left, right, key, reverse):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if reverse:
            if key(left[i]) > key(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        else:
            if key(left[i]) < key(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

    return result + left[i:] + right[j:]

if __name__ == "__main__":
    # USage Examples:
    words = ["banana", "Apple", "grape", "orange"]
    sorted_words = merge_sort(words, key=str.lower)
    print(sorted_words)

    sorted_wordsr = merge_sort(words, key=str.lower, reverse=True)
    print(sorted_wordsr)

    nums = [5, 2, 100, 23, 1]
    print(merge_sort(nums))

    print(merge_sort(nums, reverse=True))

    people = [
        {"name": "Carlos", "age": 30},
        {"name": "Ana", "age": 20},
        {"name": "Luis", "age": 25}
    ]

    sorted_people = merge_sort(people, key=lambda x: x["age"])
    print(sorted_people)

