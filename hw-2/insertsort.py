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

def insertion_sort(lst):
    for idx in range(1, len(lst)):
        stored = lst[idx]
        pos = idx
        while pos > 0 and lst[pos - 1] > stored:
            lst[pos] = lst[pos - 1]
            pos -= 1

        lst[pos] = stored


import os
def write_file(lists):
    with open('insertion.txt', 'w') as f:
        for lst in lists:
            f.write("{}{}".format(' '.join(str(s) for s in lst), os.linesep))


if __name__ == "__main__":
    lists = load_file()
    for lst in lists:
        insertion_sort(lst)
    write_file(lists)
