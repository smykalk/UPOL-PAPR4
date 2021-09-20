import threading
from random import randint
#import sys

# sys.setrecursionlimit(1500)


def random_list(length, from_value=1, to_value=1000):
    random_list = [randint(from_value, to_value) for i in range(length)]
    return random_list


def parallel_merge_sort(arr, thread_count):
    if len(arr) > 1:
        mid = len(arr)//2

        left = arr[:mid]
        right = arr[mid:]

        # 2 or more available threads
        if thread_count > 1:
            t1 = threading.Thread(target=parallel_merge_sort,
                                  args=(left, thread_count - 1))
            t1.start()
            parallel_merge_sort(right, 1)
            t1.join()

        # 1 available thread
        else:
            parallel_merge_sort(left, 1)
            parallel_merge_sort(right, 1)

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1


x = random_list(1000)


print(x)

print()
print()

parallel_merge_sort(x, 10)

print(x)
