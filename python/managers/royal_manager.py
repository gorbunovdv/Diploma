from python.managers.acyclic_graph_manager import AcyclicGraphManager
from python.managers.morphological_transformation_manager import MorphologicalTransformationManager
from python.managers.nearest_neighbours_manager import NearestNeighboursManager
from python.managers.word2vec_constructor import Word2VecConstructor
from python.managers.word_count_manager import WordCountManager


class RoyalManager:
    def __init__(self, word2vec):
        self.word2vec = word2vec

    def run(self):
        #NearestNeighboursManager.calculate_nearest_neighbours(self.word2vec)
        word_count_manager = WordCountManager()
        MorphologicalTransformationManager.calculate_morphological_transformations(self.word2vec, word_count_manager)
        AcyclicGraphManager.calculate_acyclic_graph(self.word2vec, word_count_manager)
        vocab = Word2VecConstructor.construct(self.word2vec, word_count_manager.count)
