from collections import defaultdict


class GShare:
    """docstring for GShare"""
    def __init__(self, g_history_bits=9):
        self.g_history_bits = g_history_bits
        self.history = [0 for i in xrange(self.g_history_bits)]
        self.pattern_history_table = defaultdict(list)
        self.init_pattern_history_table()

    def init_pattern_history_table(self):
        for i in range(2**self.g_history_bits):
            idx = bin(i)[2:]
            idx = (self.g_history_bits - len(idx)) * "0" + idx
            self.pattern_history_table[idx] = [0, 1]

    def format_pc(self, pc):
        return bin(pc)[2:][-self.g_history_bits:]

    def xor(self, pc):
        y = int(pc, 2) ^ int("".join([str(x) for x in self.history]), 2)
        return '{0:b}'.format(y)

    def make_prediction(self, pc):
        pc = self.format_pc(pc)
        idx = self.xor(pc)
        pred = self.pattern_history_table[idx]
        if pred == [0, 0] or pred == [0, 1]:
            return 0
        else:
            return 1

    def train_predictor(self, pc, outcome):
        pc = self.format_pc(pc)
        self.history.append(outcome)
        self.history = self.history[1:]
        idx = self.xor(pc)
        pred = self.pattern_history_table[idx]
        if outcome == 1:
            if pred == [0, 0]:
                self.pattern_history_table[idx] = [0, 1]
            elif pred == [0, 1]:
                self.pattern_history_table[idx] = [1, 0]
            elif pred == [1, 0]:
                self.pattern_history_table[idx] = [1, 1]
            elif pred == [1, 1]:
                self.pattern_history_table[idx] = [1, 1]
        if outcome == 0:
            if pred == [0, 0]:
                self.pattern_history_table[idx] = [0, 0]
            elif pred == [0, 1]:
                self.pattern_history_table[idx] = [0, 0]
            elif pred == [1, 0]:
                self.pattern_history_table[idx] = [0, 1]
            elif pred == [1, 1]:
                self.pattern_history_table[idx] = [1, 0]
