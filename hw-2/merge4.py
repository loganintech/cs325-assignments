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


def load_file():
    lines = []
    with open('data.txt', 'r') as f:
        for line in f:
            linearr = []
            for val in line.rstrip().split(' '):
                linearr.append(int(val))
            # The first number is just a length for the rest of the array, with python gives for free with `len`
            lines.append(linearr[1:len(linearr)])

    return lines


import os


def write_file(lists):
    with open('merge4.txt', 'w') as f:
        for lst in lists:
            f.write("{}{}".format(' '.join(str(s) for s in lst), os.linesep))

def print_lists(lists):
    for lst in lists:
        print("{}".format(' '.join(str(s) for s in lst)))

if __name__ == "__main__":
    lists = load_file()
    for i in range(len(lists)):
        lists[i] = merge_sort(lists[i])
    print_lists(lists)
