"""
TSP solved by genetic algorithm
including selection, crossover, mutation
"""

import random

class Genetic:
    def __init__(self, distance_table, city_num, pop_size, p_cross, p_mutation, target_len, max_generation):
        self.distance_table = distance_table  # 距离矩阵
        self.city_num = city_num  # 城市数目
        self.pop_size = pop_size  # 种群大小
        self.p_cross = p_cross  # 交叉概率
        self.p_mutation = p_mutation  # 变异概率
        self.target_len = target_len  # 目标最短路径
        self.max_generation = max_generation  # 最大迭代次数
        self.pop = []  # 种群
        self.fits = []  # 适应度
        self.min_len = 0  # 最短路径
        self.best_sol = None  # 最优路径方案
        self.init_pop()  # 产生初始种群

    def init_pop(self):  # 种群的产生（编码：城市序列）
        for i in range(self.pop_size):
            sol = list(range(0, 30))
            random.shuffle(sol)  # 路径方案
            if sol not in self.pop:
                self.pop.append(sol)

    def cal_len(self, sol):  # 计算路径长度
        length = 0
        for i in range(0, self.city_num):
            a = sol[i]
            if i != self.city_num - 1:
                b = sol[i + 1]
            else:
                b = sol[0]
            length = length + self.distance_table[a][b]
        return length

    def evaluate(self):  # 适应度评价
        self.fits = []
        for i in range(len(self.pop)):
            length = self.cal_len(self.pop[i])  # 路径长度
            fit = 1.0 / length  # 适应度
            self.fits.append(fit)

    # 遗传算子实现：
    def select_one(self):  # 选择（轮盘赌选择算法）
        parent = []
        r = random.random()
        c_fits = 0
        for i in range(0, self.pop_size):
            c_fits += self.fits[i] / sum(self.fits)
            if c_fits >= r:
                parent = self.pop[i]
                break
        return parent

    def g_code(self, child):  # Grefenstette编码
        code_child = []
        for i in range(self.city_num):
            count = 0
            for j in range(0, i):
                if child[j] <= child[i]:
                    count = count + 1
            b_i = child[i] - count  # b[i]=a[i]-(a0到a[i-1]中小于等于ai的元素个数
            code_child.append(b_i)
        return code_child

    def decode(self, code_child):  # 反Grefenstette编码
        child = list.copy(code_child)
        for i in range(self.city_num - 1, -1, -1):
            for j in range(i - 1, -1, -1):
                if child[j] <= child[i]:
                    child[i] = child[i] + 1
        de_child = child
        return de_child

    def crossover(self, parent1, parent2):  # 交叉
        # 交叉点随机
        position1 = 0
        position2 = 0
        while position1 == position2:
            position1 = random.randint(1, self.city_num - 2)
            position2 = random.randint(1, self.city_num - 2)
        # 进行交叉
        if position1 < position2:
            child = parent1[0:position1] + parent2[position1:position2+1] + parent1[position2 + 1:self.city_num]
        else:
            child = parent1[0:position2] + parent2[position2:position1+1] + parent1[position1 + 1:self.city_num]
        return child

    def mutate(self, child):  # 变异（位置交换）
        position1 = 0
        position2 = 0
        while position1 == position2:
            position1 = random.randint(0, self.city_num - 1)
            position2 = random.randint(0, self.city_num - 1)
        temp = child[position1]
        child[position1] = child[position2]
        child[position2] = temp
        return child

    def generate(self):  # 产生下一代
        child_pop = []
        self.evaluate()
        self.min_len = 1.0 / max(self.fits)
        index = self.fits.index(max(self.fits))
        self.best_sol = self.pop[index]
        child_pop.append(self.best_sol)  # 把最好的个体加入下一代
        while len(child_pop) < self.pop_size:
            child_pop.append(self.new_child())
        self.pop = child_pop

    def new_child(self):  # 选择、交叉、变异产生新个体
        parent1 = self.select_one()
        # 按概率交叉：
        r_cross = random.random()
        if r_cross < self.p_cross:
            parent2 = self.select_one()
            # 编码（防止无效子代）
            p1 = self.g_code(parent1)
            p2 = self.g_code(parent2)
            # 交叉
            code_child = self.crossover(p1, p2)
            # 解码
            child = self.decode(code_child)
        else:
            child = parent1
        # 按概率突变:
        r_mutate = random.random()
        if r_mutate < self.p_mutation:
            child = self.mutate(child)
        return child
