
import math
import random


class Ant(object):
    def __init__(self, city_num, distance_table, alpha, beta, rou, start_city):
        self.city_num = city_num  # 要访问的城市数目
        self.distance_table = distance_table  # 城市间的距离矩阵

        self.start_city = start_city
        self.visited_cities = [start_city]  # 已经走过的城市路径
        self.visited_len = 0  # 已经走过的路径长度
        self.curr_city = start_city  # 当前所在的城市
        self.no_visited_cites = None  # 未访问的城市集合

        self.p_moves = []  # 城市间的转移概率（当前城市->未访问城市）

        # 控制参数：
        self.alpha = alpha  # 启发因子-信息素的重要程度
        self.beta = beta  # 期望因子-城市间距离（能见度）的重要程度
        self.rou = rou  # 信息素残留参数（持久性）

        self.init_matrix()

    def init_matrix(self):  # 初始化矩阵
        self.no_visited_cites = list(range(0, self.city_num))

    def cal_p_move(self, tao_matrix):  # 计算转移概率
        for j in range(0, len(self.no_visited_cites)):
            city_j = self.no_visited_cites[j]
            anta_j = 1.0 / self.distance_table[self.curr_city][city_j]  # 转移到城市j的期望程度
            tao_j = tao_matrix[self.curr_city][city_j]  # ij间的信息素浓度
            sum_tao_anta = 0
            for v in range(0, len(self.no_visited_cites)):
                city_v = self.no_visited_cites[v]
                tao_v = tao_matrix[self.curr_city][city_v]
                anta_v = 1.0 / self.distance_table[self.curr_city][city_v]
                sum_tao_anta += math.pow(tao_v, self.alpha) * math.pow(anta_v, self.beta)
            p_j = (math.pow(tao_j, self.alpha) * math.pow(anta_j, self.beta)) / sum_tao_anta
            self.p_moves.append((city_j, p_j))

    def cusum_p_move(self):  # 概率累加
        cp_moves = []
        cp_j = 0
        for j in range(0, len(self.no_visited_cites)):
            city_j = self.p_moves[j][0]
            cp_j += self.p_moves[j][1]
            cp_moves.append((city_j, cp_j))
        return cp_moves

    def next(self, NC, tao_matrix):  # 选择并走到下一个城市
        city_j = -1
        self.p_moves = []
        if NC == 0 and len(self.visited_cities) == 1:  # 刚开始,随机返回一个城市
            j = random.randint(0, self.city_num-2)
            city_j = self.no_visited_cites[j]
        else:  # 按转移概率选
            self.cal_p_move(tao_matrix)
            cp_moves = self.cusum_p_move()
            r = random.random()
            for i in range(0, len(self.no_visited_cites)):
                if cp_moves[i][1] >= r:
                    city_j = cp_moves[i][0]
                    break
        self.visited_len += self.distance_table[self.curr_city][city_j]
        self.curr_city = city_j
        self.visited_cities.append(city_j)
        self.no_visited_cites.remove(city_j)
        return city_j
