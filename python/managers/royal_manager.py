from python.config.config import config
from python.managers.acyclic_graph_manager import AcyclicGraphManager
from python.managers.morphological_transformation_manager import MorphologicalTransformationManager
from python.managers.nearest_neighbours_manager import NearestNeighboursManager
from python.managers.word_count_manager import WordCountManager


class RoyalManager:
    def __init__(self, word2vec):
        self.word2vec = word2vec

    def run(self):
        #NearestNeighboursManager.calculate_nearest_neighbours(self.word2vec)
        #word_count_manager = WordCountManager()
        #MorphologicalTransformationManager.calculate_morphological_transformations(self.word2vec, word_count_manager)
        #AcyclicGraphManager.calculate_acyclic_graph(self.word2vec, word_count_manager)

        graph = [map(int, line.split()) for line in open(config["parameters"]["acyclic_graph"]["path"])]
        words = [[self.word2vec.index2word[i].word for i in cgraph] for cgraph in graph]
        for word1, word2, word3, word4 in words:
            print word1, word2, word3, word4
