import os
import time
import random


def merge_sort(lst):

    if len(lst) > 1:  # IF we have more processing to do
        middle = len(lst) // 2  # Floor division so we don't get a .5 index
        far_left = merge_sort(lst[:middle//2])
        left = merge_sort(lst[middle//2:middle])
        right = merge_sort(lst[middle:middle+middle//2])
        far_right = merge_sort(lst[middle+middle//2:])

        left = merge(far_left, left)
        right = merge(right, far_right)
        lst = merge(left, right)

    return lst


def merge(left, right):
    new_list = []
    left_counter, right_counter = 0, 0

    while left_counter < len(left) and right_counter < len(right):

        if left[left_counter] < right[right_counter]:
            new_list.append(left[left_counter])
            left_counter += 1
        else:
            new_list.append(right[right_counter])
            right_counter += 1

    # If there's still items in the left side to be added
    while left_counter < len(left):
        new_list.append(left[left_counter])
        left_counter += 1

    while right_counter < len(right):
        new_list.append(right[right_counter])
        right_counter += 1

    return new_list


sizes = [5000, 10000, 20000, 25000, 50000,
         100000, 200000, 500000, 1000000, 2000000]


def current_milli(): return int(round(time.time() * 1000))


def generate_arr(size): return [random.randint(0, 10000) for _ in range(size)]


def write_file(lists):
    with open('merge4.txt', 'w') as f:
        for lst in lists:
            f.write("{}{}".format(' '.join(str(s) for s in lst), os.linesep))


def print_lists(lists):
    for lst in lists:
        print("{}".format(' '.join(str(s) for s in lst)))


if __name__ == "__main__":
    print("===Testing 4-Way Merge Sort===")
    print("Generating Test Data...")
    lists = [generate_arr(size) for size in sizes]
    for idx, lst in enumerate(lists):
        start = current_milli()
        merge_sort(lst)
        end = current_milli()

        print("[{} Elements] {}ms".format(sizes[idx], end - start))
