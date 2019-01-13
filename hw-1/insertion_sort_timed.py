import os
import time
import random


def generate_arr(size):
    return [random.randint(0, 10_000) for _ in range(size)]


def insertion_sort(lst):
    for idx in range(1, len(lst)):
        stored = lst[idx]
        pos = idx
        while pos > 0 and lst[pos - 1] > stored:
            lst[pos] = lst[pos - 1]
            pos -= 1

        lst[pos] = stored


sizes = [100, 500, 1_000, 2_500, 5_000, 10_000, 15_000, 20_000, 25_000, 50_000]


def current_milli(): return int(round(time.time() * 1000))


if __name__ == "__main__":
    lists = [generate_arr(size) for size in sizes]
    for idx, lst in enumerate(lists):
        start = current_milli()
        insertion_sort(lst)
        end = current_milli()

        print("[{} Elements] {}ms".format(sizes[idx], end - start))
