from knapsack import Knapsack


def read_knapsack(file_path):
    """"Read a Knapsack problem instance formatted as
        http://artemisa.unicauca.edu.co/~johnyortega/instances_01_KP/"""
    file = open(file_path, "r")
    b = []
    w = []
    # s = []
    # read header
    line = file.readline()
    line = line.split(" ")
    n = int(line[0])
    cap = int(line[1])
    for line in file:
        # read item
        line = line.strip().split(" ")
        if len(line) < 3:
            b.append(int(line[0]))
            w.append(int(line[1]))
        # else:
        #     s = [int(line[i]) for i in range(len(line))]  # s = [0, 0, 0, 0, 0, 0, 1, 0 ...]
    p = Knapsack(b, w, cap, None, None, None)
    return p
