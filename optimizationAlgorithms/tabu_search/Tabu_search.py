"""
TSP solved by Tabu search
"""

import random
from solution import Solution


class Tabu:
    def __init__(self, distance_table, city_num, max_iteration, t_len):
        self.distance_table = distance_table  # 距离矩阵
        self.city_num = city_num  # 城市数目
        self.max_iteration = max_iteration  # 最大迭代次数
        self.t_len = t_len  # 禁忌表长度
        self.t_table = []  # 禁忌表
        self.curr_sol = None  # 当前解
        self.min_len = -1  # 历史最短路径长度（当前最优目标）
        self.best_sol = None  # 历史最优路径
        self.neighbors = []  # 当前解的领域

        self.init_sol()

    def init_sol(self):  # 产生初始解
        path = list(range(0, 30))
        random.shuffle(path)
        sol = Solution(path)
        length = self.cal_len(path)
        sol.path_len = length
        self.curr_sol = sol
        self.min_len = length

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

    def produce_neighbor(self):  # 生成当前解的邻域解（2-opt），计算目标函数值
        for position1 in range(0, self.city_num - 1):
            for position2 in range(position1 + 1, self.city_num):
                new_sol = self.exchange_one(position1, position2)
                self.neighbors.append(new_sol)

    def exchange_one(self, position1, position2):  # 交换
        # 新路径
        new_path = list.copy(self.curr_sol.path)
        temp = new_path[position1]
        new_path[position1] = new_path[position2]
        new_path[position2] = temp
        # 计算长度
        new_len = self.cal_len(new_path)
        # 得到新方案（记录交换）
        new_sol = Solution(new_path)
        new_sol.path_len = new_len
        new_sol.exchange = (position1, position2)  # 记录交换
        return new_sol

    def best(self):  # 领域中择优
        # 排序
        self.sort_neighbors(0, len(self.neighbors) - 1)
        # 考察最优
        curr_sol = self.neighbors[0]
        min_len = curr_sol.path_len
        exchange = curr_sol.exchange

        # 更新当前最优值
        if min_len < self.min_len:
            self.min_len = min_len  # 更新最短路径长度
            self.best_sol = curr_sol
            self.curr_sol = curr_sol
            self.update_t_table(exchange)
        else:
            i = 0
            while exchange in self.t_table:
                i += 1
                curr_sol = self.neighbors[i]
                exchange = curr_sol.exchange
            self.curr_sol = curr_sol
            self.update_t_table(exchange)

    def sort_neighbors(self, left, right):  # 快速排序
        if left >= right:
            return
        key = self.neighbors[left]
        low = left
        high = right
        while left < right:
            while left < right and self.neighbors[right].path_len >= key.path_len:
                right -= 1
            self.neighbors[left] = self.neighbors[right]
            while left < right and self.neighbors[left].path_len <= key.path_len:
                left += 1
            self.neighbors[right] = self.neighbors[left]
        self.neighbors[right] = key
        self.sort_neighbors(low, left - 1)
        self.sort_neighbors(left + 1, high)

    def update_t_table(self, exchange):  # 更新禁忌表
        # 添加
        self.t_table.append(exchange)
        # 是否在禁忌表中
        if self.t_table.count(exchange) == 2:
            self.t_table.remove(exchange)
        else:
            if len(self.t_table) == 4:
                self.t_table.pop(0)

    def new(self):  # 产生新的解
        self.neighbors = []
        self.produce_neighbor()
        self.best()
