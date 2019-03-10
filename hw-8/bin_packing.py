import sys


def load_from_file(name):

    test_cases = []
    with open(name, 'r') as f:
        test_count = int(f.readline())

        for test in range(test_count):
            capacity = int(f.readline())
            item_count = f.readline()
            items = [int(x) for x in f.readline().strip().split(' ')]

            test_cases.append({
                "capacity": capacity,
                "items": items,
            })

    return test_cases


def first_fit(weights, capacity):
    bins = []
    for weight in weights:
        # bin is a reserved keyword
        found_bin = False
        # print(f"Bins: {bins}")
        for bn in range(len(bins)):
            # print(f"Bin: {bn}, Weight: {weight}")
            if bins[bn] >= weight:
                bins[bn] -= weight
                found_bin = True
                break

        if not found_bin:
            bins.append(capacity - weight)

    return len(bins)


def first_fit_decreasing(weights, capacity):
    weights.sort(reverse=True)

    return first_fit(weights, capacity)


def best_fit(weights, capacity):
    bins = []
    for weight in weights:

        mn = capacity + 1
        bin_idx = 0
        for bn in range(len(bins)):
            if bins[bn] >= weight and bins[bn] - weight < mn:
                bin_idx = bn
                mn = bins[bn] - weight

        if mn == capacity + 1:
            bins.append(capacity - weight)
        else:
            bins[bin_idx] -= weight

    return len(bins)


if __name__ == "__main__":
    data = load_from_file(sys.argv[1])
    for i, case in enumerate(data):
        items = case['items']
        capacity = case['capacity']

        ff = first_fit(items, capacity)
        bf = best_fit(items, capacity)
        ffd = first_fit_decreasing(items, capacity)
        print("[Case {}] First Fit: {}, First Fit Decreasing: {}, Best Fit: {}".format(
            i, ff, ffd, bf))
