from collections import defaultdict
from itertools import ifilter

import numpy
import pathos.multiprocessing
import multiprocessing

from python.config.config import config
from python.managers.nearest_neighbours_manager import NearestNeighboursManager
from python.managers.rank_manager import RankManager
from python.managers.word_count_manager import WordCountManager


class AcyclicGraphManager:
    pool = pathos.multiprocessing.Pool(processes=multiprocessing.cpu_count())

    @classmethod
    def calculate_acyclic_graph(cls, word2vec):
        morphological_transformations = [map(int, line.split()) for line in open(config["parameters"]["morphological_transformations_build"]["path"] + "/result.txt")]
        fout = open(config["parameters"]["acylic_graph"]["path"], "w")
        for edge in cls.calc_acyclic_graph(word2vec, morphological_transformations):
            fout.write("%d %d %d %d\n" % edge)
        fout.close()

    @classmethod
    def calc_acyclic_graph(cls, word2vec, morphological_transformations):
        word_count_manager = WordCountManager()
        edge_by_word = defaultdict(list)
        nearest_neighbours = NearestNeighboursManager.load_nearest_neighbours(word2vec)
        for word1, word2, word3, word4 in morphological_transformations:
            edge_by_word[word1].append((word1, word2, word3, word4))
        return list(cls.pool.imap(lambda edges_list: cls.get_next_edge(word2vec, word_count_manager, nearest_neighbours, edges_list), edge_by_word))

    @classmethod
    def get_next_edge(cls, word2vec, word_count_manager, nearest_neighbours, edges_list):
        return min(ifilter(lambda edge: word_count_manager.check_word_counts(edge[0], edge[1]), edges_list), key=lambda edge: cls.get_key(word2vec, nearest_neighbours, edge))

    @staticmethod
    def get_key(word2vec, nearest_neighbours, edge):
        word1, word2, word3, word4 = edge
        vc2 = word2vec.syn0[word1] + word2vec.syn0[word4] - word2vec.syn0[word3]
        vc2 /= numpy.linalg.norm(vc2)
        cos = numpy.dot(word2vec.syn0[word2], vc2)
        return RankManager.get_rank(nearest_neighbours, cos), cos
