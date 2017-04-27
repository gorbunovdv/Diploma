# coding=utf-8

"""
    Менеджер для быстрого поиска ранга бинарным поиском
"""
class RankManager:
    @staticmethod
    def get_rank(cos_list, cos):
        l, r = 0, len(cos_list)
        while r - l > 1:
            m = (l + r) // 2
            if cos_list[m] < cos:
                r = m
            else:
                l = m
        return l