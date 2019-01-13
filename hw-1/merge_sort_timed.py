import os
import time
import random


def generate_arr(size):
    return [random.randint(0, 10_000) for _ in range(size)]


def merge_sort(lst):

    if len(lst) > 1:  # IF we have more processing to do
        middle = len(lst) // 2  # Floor division so we don't get a .5 index
        left = merge_sort(lst[:middle])
        right = merge_sort(lst[middle:])

        # Merge happens in-place
        merge(lst, left, right)

    return lst


def merge(master_list, left, right):
    left_counter, right_counter, combined_counter = 0, 0, 0

    while left_counter < len(left) and right_counter < len(right):

        if left[left_counter] < right[right_counter]:
            master_list[combined_counter] = left[left_counter]
            left_counter += 1
        else:
            master_list[combined_counter] = right[right_counter]
            right_counter += 1

        combined_counter += 1

    # If there's still items in the left side to be added
    while left_counter < len(left):
        master_list[combined_counter] = left[left_counter]
        left_counter += 1
        combined_counter += 1

    while right_counter < len(right):
        master_list[combined_counter] = right[right_counter]
        right_counter += 1
        combined_counter += 1


sizes = [5_000, 10_000, 20_000, 25_000, 50_000,
         100_000, 200_000, 500_000, 1_000_000, 2_000_000]


def current_milli(): return int(round(time.time() * 1000))


if __name__ == "__main__":
    lists = [generate_arr(size) for size in sizes]
    for idx, lst in enumerate(lists):
        start = current_milli()
        merge_sort(lst)
        end = current_milli()

        print("[{} Elements] {}ms".format(sizes[idx], end - start))
