# coding=utf-8

from collections import defaultdict

import numpy

from python.config.config import config
from python.logger.logger import Logger, IterableTicker, Ticker
from python.managers.nearest_neighbours_manager import NearestNeighboursManager
from python.managers.rank_manager import RankManager

logger = Logger("AcyclicGraphManager")

"""
    Менеджер для подсчета ациклического графа по морфологическим преобразованиям
"""
class AcyclicGraphManager:
    """
        Функция для подсчета и записи в файл ациклического графа по морфологическим преобразованиям
    """
    @classmethod
    def calculate_acyclic_graph(cls, word2vec, word_count_manager):
        morphological_transformations = (map(int, line.split()) for line in IterableTicker(logger, open(config["parameters"]["morphological_transformations_build"]["path"] + "/result.txt"), 10 ** 6))
        logger.info("Read all morphological transformations")
        fout = open(config["parameters"]["acyclic_graph"]["path"] + "/result.txt", "w")
        example_fout = open(config["parameters"]["acyclic_graph"]["path"] + "/example.txt", "w")
        for edge in cls.calc_acyclic_graph(word2vec, morphological_transformations, word_count_manager):
            if edge is not None:
                fout.write("%d %d %d %d\n" % edge)
                w1, w2, w3, w4 = edge
                example_fout.write("%s %s %s %s\n" % (word2vec.index2word[w1].word.encode('utf-8'),
                                                      word2vec.index2word[w2].word.encode('utf-8'),
                                                      word2vec.index2word[w3].word.encode('utf-8'),
                                                      word2vec.index2word[w4].word.encode('utf-8')))
        fout.close()
        example_fout.close()

    """
        Функция для подсчета ациклического графа по морфологическим преобразованиям
    """
    @classmethod
    def calc_acyclic_graph(cls, word2vec, morphological_transformations, word_count_manager):
        ticker = Ticker(logger, len(word2vec.index2word), "AcyclicGraphManager")
        edge_by_word = defaultdict(list)
        nearest_neighbours = NearestNeighboursManager.load_nearest_neighbours(word2vec)
        for word1, word2, word3, word4 in morphological_transformations:
            edge_by_word[word1].append((word1, word2, word3, word4))
        return map(lambda (word1, edge_list): cls.get_next_edge(word2vec, word_count_manager, nearest_neighbours, edge_list, ticker), edge_by_word.iteritems())

    """
        Функция для нахождения ребра, идущего из текущей вершины в ациклическом графе
    """
    @classmethod
    def get_next_edge(cls, word2vec, word_count_manager, nearest_neighbours, edges_list, ticker):
        ticker()
        edge_list = filter(lambda edge: word_count_manager.check_word_counts(word2vec, edge[0], edge[1]), edges_list)
        if len(edge_list) == 0:
            return None
        result = min(edge_list, key=lambda edge: cls.get_key(word2vec, nearest_neighbours, edge))
        return result

    """
        Функция для подсчета ключа, по которому упорядочиваются ребра при подсчете ациклического графа
    """
    @staticmethod
    def get_key(word2vec, nearest_neighbours, edge):
        word1, word2, word3, word4 = edge
        vc2 = word2vec.syn0[word1] + word2vec.syn0[word4] - word2vec.syn0[word3]
        vc2 /= numpy.linalg.norm(vc2)
        cos = numpy.dot(word2vec.syn0[word2] / numpy.linalg.norm(word2vec.syn0[word2]), vc2)
        return RankManager.get_rank(nearest_neighbours[word2], cos), -cos
