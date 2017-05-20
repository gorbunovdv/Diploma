# coding=utf-8
from python.config.config import config
from python.logger.logger import Logger
from python.managers.acyclic_graph_manager import AcyclicGraphManager
from python.managers.evaluate_manager import EvaluateManager
from python.managers.morphological_transformation_manager import MorphologicalTransformationManager
from python.managers.nearest_neighbours_manager import NearestNeighboursManager
from python.managers.vector_builder import VectorBuilder, OffsetVectorBuilder
from python.managers.word2vec_constructor import Word2VecConstructor
from python.managers.word_count_manager import WordCountManager

logger = Logger("RoyalManager")

"""
    Главный менеджер программы: осуществляет подсчет ближайших соседей, подсчет морфологических преобразований, подсчет ациклического графа, подсчет новых векторов и записать новых моделей Word2Vec
"""
class RoyalManager:
    def __init__(self, word2vec):
        self.word2vec = word2vec

    def run(self):
#        fin = open(config["parameters"]["morphological_transformations_build"]["path"] + "/result.txt")
#        fout = open(config["parameters"]["morphological_transformations_build"]["path"] + "/examples.txt", "w")
#        for a, b, c, d in map(lambda line: map(int, line.strip().split()), fin.readlines()):
#            fout.write("{} {} {} {}\n".format(
#                self.word2vec.index2word[a].word.encode('utf-8'),
#                self.word2vec.index2word[b].word.encode('utf-8'),
#                self.word2vec.index2word[c].word.encode('utf-8'),
#                self.word2vec.index2word[d].word.encode('utf-8')
#            ))
#        fout.close()
        NearestNeighboursManager.calculate_nearest_neighbours(self.word2vec)
        word_count_manager = WordCountManager()
        MorphologicalTransformationManager.calculate_morphological_transformations(self.word2vec, word_count_manager)
        AcyclicGraphManager.calculate_acyclic_graph(self.word2vec, word_count_manager)
        builder = VectorBuilder(self.word2vec, word_count_manager.count)
        builder_offset = OffsetVectorBuilder(self.word2vec, word_count_manager.count)
        initial_vocab = self.word2vec.generate_vocab()
        for dataset in config["parameters"]["evaluation"]["dataset_paths"]:
           for vc, name in [(builder, "vocab"), (builder_offset, "offset_vocab"), (initial_vocab, "initial_vocab")]:
               fin = open(dataset, "r")
               fout = open(config["parameters"]["evaluation"]["result_folder"] + "/" + dataset.replace("/", "__").replace(".", "") + '__' + name, "w")
               logger.info("Path: {}".format(config["parameters"]["evaluation"]["result_folder"] + "/" + dataset.replace("/", "__") + '__' + name))
               EvaluateManager.evaluate(fin, fout, vc)
               fout.close()
