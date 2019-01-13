def load_file():
    lines = []
    with open('data.txt', 'r') as f:
        for line in f:
            linearr = []
            for val in line.rstrip().split(' '):
                linearr.append(int(val))
            lines.append(linearr[1:len(linearr)]) # The first number is just a length for the rest of the array, with python gives for free with `len`

    return lines

def merge_sort(lst):

    if len(lst) > 1: # IF we have more processing to do
        middle = len(lst) // 2 #Floor division so we don't get a .5 index
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


import os
def write_file(lists):
    with open('merge.txt', 'w') as f:
        for lst in lists:
            f.write("{}{}".format(' '.join(str(s) for s in lst), os.linesep))


if __name__ == "__main__":
    lists = load_file()
    for lst in lists:
        merge_sort(lst)
    write_file(lists)
