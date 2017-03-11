from python.managers.morphological_transformation_manager import MorphologicalTransformationManager
from python.managers.nearest_neighbours_manager import NearestNeighboursManager


class RoyalManager:
    def __init__(self, word2vec):
        self.word2vec = word2vec

    def run(self):
        #NearestNeighboursManager.calculate_nearest_neighbours(self.word2vec)
        MorphologicalTransformationManager.calculate_morphological_transformations(self.word2vec)