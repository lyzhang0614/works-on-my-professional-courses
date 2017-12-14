"""
TSP solved by simulate anneal
d*=423.741
"""

import numpy as np
import pandas as pd
from simulate_anneal import SA

cities = pd.Series([(41, 94), (37, 84), (54, 67), (25, 62), (7, 54), (2, 99),
                    (68, 58), (71, 44), (54, 62), (83, 69), (64, 60), (18, 54),
                    (22, 60), (83, 46), (91, 38), (25, 38), (24, 42), (58, 69),
                    (71, 71), (74, 78), (87, 76), (18, 40), (13, 40), (82, 7),
                    (62, 32), (58, 35), (45, 21), (41, 26), (44, 35), (4, 50)])  # 0-29:代表30个城市

distance_table = pd.DataFrame(np.zeros((30, 30)))
for i in np.arange(0, 30):
    for j in np.arange(0, 30):
        address_i = cities[i]
        address_j = cities[j]
        distance_ij = np.sqrt(np.square((address_i[0] - address_j[0])) + np.square((address_i[1] - address_j[1])))
        distance_table[i][j] = distance_ij

if __name__ == "__main__":
    # 模拟退火算法求解：
    sa = SA(distance_table, 30, 1000, 0.98, 0.001, 500)
    sa.run()
