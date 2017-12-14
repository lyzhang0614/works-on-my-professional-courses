LEN_NONE = -1


class Solution(object):
    def __init__(self, path=None):
        self.path = path
        self.path_len = LEN_NONE
        self.exchange = None  # 通过该交换得到
