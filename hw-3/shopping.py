import pprint


def get_test_cases():
    cases = []
    with open("shopping.txt", "r") as f:
        case_count = int(f.readline())
        for _ in range(0, case_count):
            case = {}
            case['items'] = []
            for _ in range(0, int(f.readline())):
                item = {}
                line_split = f.readline().split(' ')
                item['price'] = int(line_split[0])
                item['weight'] = int(line_split[1])
                case['items'].append(item)

            case['family_members'] = []
            for _ in range(0, int(f.readline())):
                case['family_members'].append(int(f.readline()))

            cases.append(case)

    return cases


COMPLEXITY = 0


def naieve_recursion(capacity, items):

    if len(items) == 0 or capacity == 0:
        return 0

    if items[len(items) - 1]['weight'] > capacity:
        return naieve_recursion(capacity, items[:-1])
    else:
        first = naieve_recursion(
            capacity - items[len(items) - 1]['weight'], items[:-1]) + items[len(items) - 1]['price']
        second = naieve_recursion(capacity, items[:-1])

        return max(first, second)


def get_max_value_recursion(case):
    max_vals = []
    for member in case['family_members']:
        max_vals.append(naieve_recursion(member, case['items']))

    return max_vals


def bottom_up(capacity, items):
    value_table = []
    for row in range(len(items) + 1):
        value_table.append([])
        for column in range(capacity + 1):
            if row == 0 or column == 0:
                value_table[row].append(0)
            elif items[row - 1]['weight'] <= column:
                value_table[row].append(max(items[row - 1]['price'] + value_table[row - 1]
                                            [column - items[row - 1]['weight']], value_table[row - 1][column]))
            else:
                value_table[row].append(value_table[row - 1][column])

    return value_table[len(items)][capacity], value_table


def get_max_val_bottom_up(case):
    # pprint.pprint(case)
    max_vals = []
    for member in case['family_members']:
        max_vals.append(bottom_up(member, case['items']))

    return max_vals


def get_path(table, items):
    path = []

    current_max_capacity = len(table[len(table) - 1])

    for row in range(len(table))[::-1]:
        for column in range(len(table[row]))[::-1]:

            if current_max_capacity <= column or table[row][column] == table[row][column - 1]:
                continue

            if table[row][column] == table[row - 1][column]:
                break

            if (not row in path) and items[row - 1]['price'] != 0:
                path.append(row)
                current_max_capacity -= items[row - 1]['weight']


    return " ".join([str(x) for x in path][::-1])


cases = get_test_cases()
for idx, case in enumerate(cases):
    lst = get_max_val_bottom_up(case)
    print("Test Case {}".format(idx + 1))
    price = 0
    for person in lst:
        price += person[0]
    print("Total Price {}".format(price))
    print("Member Items")
    for fam_idx, person in enumerate(lst):
        print("{}: {}".format(fam_idx + 1, get_path(person[1], case['items'])))

    print()
