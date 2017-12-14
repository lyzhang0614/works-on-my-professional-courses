"""
TSP solved by simulate anneal
"""

import random
import math
from solution import Solution


class SA:
    def __init__(self, distance_table, city_num, t0, speed, min_t, inner_iteration):
        self.distance_table = distance_table  # 距离矩阵
        self.city_num = city_num  # 城市数目
        self.inner_iteration = inner_iteration  # 内部最大迭代次数
        self.t = t0  # 初始温度
        self.speed = speed  # 退火速率
        self.min_t = min_t  # 最低温度
        self.curr_sol = None  # 当前解

        self.init_sol()

    def init_sol(self):  # 产生初始解
        path = list(range(0, 30))
        random.shuffle(path)
        path_len = self.cal_len(path)
        sol = Solution(path)
        sol.path_len = path_len
        self.curr_sol = sol

    def cal_len(self, path):  # 计算路径长度（目标函数值）
        length = 0
        for i in range(0, self.city_num):
            a = path[i]
            if i != self.city_num - 1:
                b = path[i + 1]
            else:
                b = path[0]
            length = length + self.distance_table[a][b]
        return length

    def generate(self):  # 产生领域解（2-opt）
        position1 = 0
        position2 = 0
        while position1 == position2:
            position1 = random.randint(0, self.city_num - 1)
            position2 = random.randint(0, self.city_num - 1)
        # 新路径
        new_path = list.copy(self.curr_sol.path)
        temp = new_path[position1]
        new_path[position1] = new_path[position2]
        new_path[position2] = temp
        # 计算长度
        new_len = self.cal_len(new_path)
        # 得到新方案
        new_sol = Solution(new_path)
        new_sol.path_len = new_len
        return new_sol

    def update_t(self):  # 退温
        self.t = self.t * self.speed

    def run(self):
        k = 0
        while self.min_t <= self.t:  # 算法终止准则
            i = 0
            while i <= self.inner_iteration:  # 抽样稳定准则
                new_sol = self.generate()
                a = -(new_sol.path_len - self.curr_sol.path_len) / self.t
                x = math.exp(a)
                r = random.random()
                if min([1, x]) >= r:
                    self.curr_sol = new_sol
                i += 1
            print(k, ':', self.curr_sol.path_len)
            k += 1
            self.update_t()
        print(self.curr_sol.path)
