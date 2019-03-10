import random

with open("random_packing.txt", "w") as f:

    pack_count = 5000
    f.write("{}\n".format(pack_count))
    for i in range(pack_count):
        number_of_weights = random.randint(20, 100)
        bin_capacity = random.randint(10, 20)
        weights = [str(random.randint(2, bin_capacity))
                   for _ in range(number_of_weights)]

        f.write("{}\n".format(number_of_weights))
        f.write("{}\n".format(bin_capacity))
        f.write("{}\n".format(" ".join(weights)))
