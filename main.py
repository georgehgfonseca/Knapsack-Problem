from knapsack import Knapsack
import util
import random
import local_search

# ==================== lecture test problem data and solution ==========================
# dataset = "test_8_items"
# cap = 10
# b = [6, 7, 9, 11, 5, 9, 3]
# w = [4, 4, 6,  7, 3, 5, 2]
# # solution
# s_ini = [0, 0, 1, 0, 0, 0, 1]
# fs_ini = 12
# ws_ini = 8
# p_ini = Knapsack(b, w, cap, s_ini, fs_ini, ws_ini)
# t = 0.00

# =================== real problem data and greedy initial solution ===================
dataset = "Datasets/large_scale/knapPI_1_100_1000_1"
p_ini = util.read_knapsack(dataset)
random.seed(0)  # change/remove to allow new random behavior (and solutions)
p_ini, t = p_ini.greedy_build()

# =============================== results table header ================================
print("=" * 13 + " " + f'{dataset:42}' + " " + "=" * 13)
print(f'| Method               |                   s* |                 t(s) |')
print(f'| Greedy init. soln.   | {round(p_ini.fs, 2):20.2f} | {round(t, 2):20.2f} |')

# =============================== local search methods ================================
p = Knapsack(p_ini.b, p_ini.w, p_ini.cap, p_ini.s[:], p_ini.fs, p_ini.ws)
p, t = local_search.descent(p)
print(f'| Descent Swap         | {round(p.fs, 2):20.2f} | {round(t, 2):20.2f} |')

p = Knapsack(p_ini.b, p_ini.w, p_ini.cap, p_ini.s[:], p_ini.fs, p_ini.ws)
p, t = local_search.first_improvement(p)
print(f'| First Improv. Swap   | {round(p.fs, 2):20.2f} | {round(t, 2):20.2f} |')

p = Knapsack(p_ini.b, p_ini.w, p_ini.cap, p_ini.s[:], p_ini.fs, p_ini.ws)
p, t = local_search.random_descent(p, 1000)
print(f'| Random Descent Swap  | {round(p.fs, 2):20.2f} | {round(t, 2):20.2f} |')

p = Knapsack(p_ini.b, p_ini.w, p_ini.cap, p_ini.s[:], p_ini.fs, p_ini.ws)
p, t = local_search.vnd(p, 2)
print(f'| VND Swap & 3-Swap    | {round(p.fs, 2):20.2f} | {round(t, 2):20.2f} |')
print("=" * 70)
# =====================================================================================
