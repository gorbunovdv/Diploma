import bisect


class RankManager:
    @staticmethod
    def get_rank(cos_list, cos):
        return bisect.bisect(cos_list, cos)