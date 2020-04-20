def swap(arr, a, b):
    temp = arr[a]
    arr[a] = arr[b]
    arr[b] = temp
    return arr


def quick_sort(arr, first, last):
    print("Sorting:" + str(arr) + " indices " + str(first) + "-" + str(last))
    if first >= last:
        return arr
    a = int(first)
    b = int(last / 2)
    c = int(last)
    if arr[a] <= arr[b] <= arr[c] or arr[c] <= arr[b] <= arr[a]:
        pivot = b
    elif arr[b] <= arr[a] <= arr[c] or arr[c] <= arr[a] <= arr[b]:
        pivot = a
    else:
        pivot = c
    arr = swap(arr, pivot, first)
    pivot = first

    i = first + 1
    for j in range(first + 2, last + 1):
        if arr[j] < arr[pivot]:
            arr = swap(arr, i, j)
            i = i + 1
    if arr[i] < arr[pivot]:
        arr = swap(arr, pivot, i)
        pivot = i
    else:
        arr = swap(arr, pivot, i - 1)
        pivot = i - 1
    arr = quick_sort(arr, first, pivot - 1)
    arr = quick_sort(arr, pivot + 1, last)
    return arr


test = [34, 23, 333, 21, 57, 0, -12323, 85, 324]
result = quick_sort(test, 0, len(test) - 1)
print("result:" + str(result))