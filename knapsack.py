import random
import time


class Knapsack:
    """Class to represent a Knapsack problem and its solution"""
    def __init__(self, b, w, cap, s, fs, ws):
        """Builds a Knapsack object"""
        self.b = b       # array of benefit per item
        self.w = w       # array of weight per item
        self.cap = cap   # capacity of the knapsack
        self.s = s       # solution to the problem (binary array 1-in 0-out)
        self.fs = fs     # objective value of solution s (sum of benefits)
        self.ws = ws     # used knapsack capacity of solution s (sum of weights)

    def greedy_build(self):
        """"Greedy initial solution build by best benefit/weight relation"""
        b, w, cap = self.b, self.w, self.cap
        t_init = time.time()
        bw = [b[i] / w[i] for i in range(len(b))]
        C = [i for i in range(len(b))]
        s = [0 for _ in range(len(b))]
        s_weight = 0
        s_benefit = 0
        while len(C) != 0:
            # select cmax
            max = float("-inf")
            cmax = -1
            for c in C:
                if bw[c] > max:
                    max = bw[c]
                    cmax = c
            # insert cmax in s if possible
            if s_weight + w[cmax] <= cap:
                s[cmax] = 1
                s_weight += w[cmax]
                s_benefit += b[cmax]
            C.remove(cmax)
        self.s = s
        self.fs = s_benefit
        self.ws = s_weight
        return self, time.time() - t_init

    def part_greedy_build(self, alpha):
        """"Greedy initial solution build by cheapest insertion heuristic"""
        b, w, cap = self.b, self.w, self.cap
        t_init = time.time()
        bw = [b[i] / w[i] for i in range(len(b))]
        C = [i for i in range(len(b))]
        s = [0 for _ in range(len(b))]
        s_weight = 0
        s_benefit = 0
        while len(C) != 0:
            # calculate gmin and gmax
            gmax = float("-inf")
            gmin = float("inf")
            for c in C:
                if bw[c] > gmax:
                    gmax = bw[c]
                if bw[c] < gmin:
                    gmin = bw[c]
            # create LCR
            LCR = []
            for c in C:
                if bw[c] >= gmax - alpha * (gmax - gmin):
                    LCR.append(c)
            # randomly select c
            c = random.choice(LCR)
            # insert cmax in s if possible
            if s_weight + w[c] <= cap:
                s[c] = 1
                s_weight += w[c]
                s_benefit += b[c]
            C.remove(c)
        self.s = s
        self.fs = s_benefit
        self.ws = s_weight
        return self, time.time() - t_init

    def swap(self, i, j):
        """Eval swap between items i (remove) and j (add)"""
        b, w, cap, s, fs, ws = self.b, self.w, self.cap, self.s, self.fs, self.ws
        if ws - w[i] + w[j] <= cap:
            fs = fs - b[i] + b[j]
        return fs

    def swap_move(self, i, j):
        """Do swap items i (remove) and j (add)"""
        b, w, cap, s, fs, ws = self.b, self.w, self.cap, self.s, self.fs, self.ws
        if ws - w[i] + w[j] <= cap:
            s[i] = 0
            s[j] = 1
            self.fs = fs - b[i] + b[j]
            self.ws = ws - w[i] + w[j]
        return self

    def swap_move_naive(self, i, j):
        """Naive (slow) swap items i (remove) and j (add)"""
        b, w, cap, s, fs, ws = self.b, self.w, self.cap, self.fs, self.ws
        if ws - w[i] + w[j] <= cap:
            s[i] = 0
            s[j] = 1
            self.fs = self.full_eval()
        return self

    def three_swap(self, i, j, k):
        """Eval removal (if in) or addition (if out) of itens i, j and k"""
        b, w, cap, s, fs, ws = self.b, self.w, self.cap, self.s, self.fs, self.ws
        if s[i] == 0:
            ws += w[i]
        else:
            ws -= w[i]
        if s[j] == 0:
            ws += w[j]
        else:
            ws -= w[j]
        if s[k] == 0:
            ws += w[k]
        else:
            ws -= w[k]
        if ws <= cap:
            if s[i] == 0:
                fs += b[i]
            else:
                fs -= b[i]
            if s[j] == 0:
                fs += b[j]
            else:
                fs -= b[j]
            if s[k] == 0:
                fs += b[k]
            else:
                fs -= b[k]
        return fs

    def three_swap_move(self, i, j, k):
        """Do remove (if in) or add (if out) items i, j and k"""
        b, w, cap, s, fs, ws = self.b, self.w, self.cap, self.s, self.fs, self.ws
        if s[i] == 0:
            ws += w[i]
        else:
            ws -= w[i]
        if s[j] == 0:
            ws += w[j]
        else:
            ws -= w[j]
        if s[k] == 0:
            ws += w[k]
        else:
            ws -= w[k]
        if ws <= cap:
            if s[i] == 0:
                fs += b[i]
                s[i] = 1
            else:
                fs -= b[i]
                s[i] = 0
            if s[j] == 0:
                fs += b[j]
                s[j] = 1
            else:
                fs -= b[j]
                s[j] = 0
            if s[k] == 0:
                fs += b[k]
                s[k] = 1
            else:
                fs -= b[k]
                s[k] = 0
        self.fs = fs
        self.ws = ws
        return self

    def three_swap_move_naive(self, i, j, k):
        """Naive (slow) remove (if in) or add (if out) items i, j and k"""
        b, w, cap, s, fs, ws = self.b, self.w, self.cap, self.s, self.fs, self.ws
        if s[i] == 0:
            ws += w[i]
        else:
            ws -= w[i]
        if s[j] == 0:
            ws += w[j]
        else:
            ws -= w[j]
        if s[k] == 0:
            ws += w[k]
        else:
            ws -= w[k]
        if ws <= cap:
            if s[i] == 0:
                s[i] = 1
            else:
                s[i] = 0
            if s[j] == 0:
                s[j] = 1
            else:
                s[j] = 0
            if s[k] == 0:
                s[k] = 1
            else:
                s[k] = 0
        self.fs = self.full_eval()
        self.ws = ws
        return self

    def full_eval(self):
        """Full objective function evaluation (please avoid it!)"""
        b, w, cap, s, fs, ws = self.b, self.w, self.cap, self.s, self.fs, self.ws
        fs = 0
        ws = 0
        for i in range(len(s)):
            if s[i] == 1:
                fs += b[i]
                ws += w[i]
                # infeasible
                if ws > cap:
                    fs -= 10000000
        return fs
