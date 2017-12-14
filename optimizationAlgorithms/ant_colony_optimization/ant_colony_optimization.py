"""
TSP solved by ant colony optimization
"""
import numpy as np
import pandas as pd
from solution import Solution
from ant import Ant
import random


class ACO:
    def __init__(self, distance_table, city_num, ant_num, max_iteration, alpha, beta, rou):
        self.distance_table = distance_table  # 距离矩阵
        self.city_num = city_num  # 城市数目
        self.ant_num = ant_num  # 蚂蚁数目
        self.ants = []  # 蚂蚁集合
        self.max_iteration = max_iteration  # 迭代次数
        self.sols = []  # 当前解集
        self.best_sol = None  # 当前最优解
        self.min_len = 0  # 当前最短路径长度

        # 控制参数：
        self.alpha = alpha  # 启发因子-信息素的重要程度
        self.beta = beta  # 期望因子-城市间距离（能见度）的重要程度
        self.rou = rou  # 信息素残留参数（持久性）

        self.tao_matrix = None  # 信息素矩阵
        self.delta_tao_matrix = None  # 信息增量矩阵

        self.init_matrix()

    def init_ants(self):  # 初始化蚂蚁集合
        self.ants = []
        for i in range(0, self.ant_num):  # 将m个蚂蚁随机置于n个顶点上
            start_city = random.randint(0, self.city_num - 1)
            ant = Ant(self.city_num, self.distance_table, self.alpha, self.beta, self.rou, start_city)
            ant.no_visited_cites.remove(start_city)
            self.ants.append(ant)

    def init_matrix(self):  # 信息素浓度矩阵初始化
        self.tao_matrix = pd.DataFrame(np.ones((self.city_num, self.city_num)))  # 初始化为1
        self.delta_tao_matrix = pd.DataFrame(np.zeros((self.city_num, self.city_num)))  # 增量初始化为0

    def get_sols(self, NC):  # 获取当前解集
        self.sols = []
        for k in range(0, self.ant_num):
            city_j = -1
            while len(self.ants[k].visited_cities) < 30:
                city_j = self.ants[k].next(NC, self.tao_matrix)
            self.ants[k].visited_len += self.distance_table[city_j][self.ants[k].start_city]
            for i in range(0, self.city_num):  # 更新本次循环中留在ij上的信息量
                city_i = self.ants[k].visited_cities[i]
                if i == self.city_num - 1:
                    j = 0
                else:
                    j = i + 1
                city_j = self.ants[k].visited_cities[j]
                delta_tao = 1.0 / self.distance_table[city_i][city_j]  # ij间信息增量
                self.delta_tao_matrix[city_i][city_j] += delta_tao
            # 得到蚂蚁k走出的解
            sol = Solution(self.ants[k].visited_cities)
            sol.path_len = self.ants[k].visited_len
            self.sols.append(sol)

    def find_best(self, NC):  # 获取当前最优解
        self.min_len = self.sols[0].path_len
        for k in range(1, self.ant_num):
            if self.sols[k].path_len < self.min_len:
                self.min_len = self.sols[k].path_len
                self.best_sol = self.sols[k]
        print(NC, ':', self.min_len)
        print(self.best_sol.path)

    def update_tao_matrix(self):  # 更新信息素矩阵
        self.tao_matrix = self.rou * self.tao_matrix + self.delta_tao_matrix

    def ants_run(self):  # 蚁群转移获得解集
        NC = 0
        while NC < self.max_iteration:
            self.init_ants()
            self.get_sols(NC)
            self.find_best(NC)
            self.update_tao_matrix()
            NC += 1
