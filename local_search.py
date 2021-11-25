import knapsack
import random
import time


def get_swap_first_neighbor(p):
    """Get first neighbor regarding swap neighborhood. A neighbor represented as: [fs, i, j]"""
    V = []
    for i in range(len(p.b)):
        if p.s[i] == 1:
            for j in range(len(p.b)):
                if p.s[j] == 0:
                    fs_line = p.swap(i, j)
                    if fs_line > p.fs:
                        V.append([fs_line, i, j])
                        return V
    return V


def get_swap_neighbors(p):
    """Get all neighbors regarding swap neighborhood. A neighbor represented as: [fs, i, j]"""
    V = []
    for i in range(len(p.b)):
        if p.s[i] == 1:
            for j in range(len(p.b)):
                if p.s[j] == 0:
                    fs_line = p.swap(i, j)
                    if fs_line > p.fs:
                        V.append([fs_line, i, j])
    return V


def get_three_swap_neighbors(p):
    """Get all neighbors regarding 3-swap neighborhood. A neighbor represented as: [fs, i, j, k]"""
    V = []
    for i in range(len(p.b)):
        for j in range(i+1, len(p.b)):
            for k in range(j+1, len(p.b)):
                fs_line = p.three_swap(i, j, k)
                if fs_line > p.fs:
                    V.append([fs_line, i, j, k])
    return V


def descent(p):
    """Descent local search method (swap) for the knapsack problem"""
    t_init = time.time()
    V = get_swap_neighbors(p)
    while V:
        max_n = float("-inf")
        idx_n = -1
        for idx in range(len(V)):
            if V[idx][0] > max_n:
                max_n = V[idx][0]
                idx_n = idx
        i, j = V[idx_n][1], V[idx_n][2]
        p = p.swap_move(i, j)
        V = get_swap_neighbors(p)
    return p, time.time() - t_init


def descent_three_swap(p):
    """Descent local search method (3-swap) for the knapsack problem"""
    t_init = time.time()
    V = get_three_swap_neighbors(p)
    while V:
        max_n = float("-inf")
        idx_n = -1
        for idx in range(len(V)):
            if V[idx][0] > max_n:
                max_n = V[idx][0]
                idx_n = idx
        i, j, k = V[idx_n][1], V[idx_n][2], V[idx_n][3]
        p = p.three_swap_move(i, j, k)
        V = get_three_swap_neighbors(p)
    return p, time.time() - t_init


def first_improvement(p):
    """First improvement local search method (swap) for the knapsack problem"""
    t_init = time.time()
    V = get_swap_first_neighbor(p)
    while V:
        i, j = V[0][1], V[0][2]
        p = p.swap_move(i, j)
        V = get_swap_first_neighbor(p)
    return p, time.time() - t_init


def random_descent(p, it_max):
    """Random descent local search method (swap) for the knapsack problem"""
    t_init = time.time()
    it = 0
    while it < it_max:
        it += 1
        i = random.choice(range(0, len(p.b)))
        j = random.choice(range(0, len(p.b)))
        while p.s[i] == 0:
            i = random.choice(range(0, len(p.b)))
        while i == j or p.s[j] == 1:
            j = random.choice(range(0, len(p.b)))
        fs_line = p.swap(i, j)
        if fs_line > p.fs:
            p = p.swap_move(i, j)
    return p, time.time() - t_init


def vnd(p, k_max):
    """Variable neighborhood descent method for the knapsack problem (k=1: swap k=2: 3-swap)"""
    t_init = time.time()
    k = 1
    while k <= k_max:
        p_line = knapsack.Knapsack(p.b, p.w, p.cap, p.s[:], p.fs, p.ws)
        if k == 1:
            p, t = descent(p_line)
        elif k == 2:
            p, t = descent_three_swap(p_line)
        if p_line.fs > p.fs:
            p = knapsack.Knapsack(p_line.b, p_line.w, p_line.cap, p_line.s[:], p_line.fs, p_line.ws)
            k = 1
        else:
            k += 1
    return p, time.time() - t_init
