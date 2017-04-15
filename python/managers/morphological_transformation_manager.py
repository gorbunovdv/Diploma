from random import shuffle

import numpy

from python.config.config import config
from python.logger.logger import Ticker, Logger
from python.managers.nearest_neighbours_manager import NearestNeighboursManager
from python.managers.word_count_manager import WordCountManager
from python.transformations_iterator.transformations_iterator import TransformationsReader

logger = Logger("MorphologicalTransformationManager")


class MorphologicalTransformationManager:
    @classmethod
    def calculate_morphological_transformations(cls, word2vec):
        fout = open(config["parameters"]["morphological_transformations_build"]["path"] + "/result.txt", "w")
        reader = TransformationsReader(config["parameters"]["transformations_filter"]["filtered_path"])
        classTicker = Ticker(logger, 0, "classTicker", 100)
        classTicker2 = Ticker(logger, 0, "splitClassTicker", 100)
        syn0norm = numpy.array(word2vec.syn0, copy=True)
        syn0norm /= numpy.linalg.norm(syn0norm, axis=1)[:, numpy.newaxis]
        min_cos = float(config["parameters"]["morphological_transformations_build"]["min_cos"])
        max_rank = int(config["parameters"]["morphological_transformations_build"]["max_rank"])
        nearest_neighbours = NearestNeighboursManager.load_nearest_neighbours(word2vec)[:, max_rank]
        for i in range(len(nearest_neighbours)):
            nearest_neighbours[i] = max(nearest_neighbours[i], min_cos)
        word_count_manager = WordCountManager()
        PIECE = 5000
        for clazz in reader.foreachClass(word2vec):
            clazz = filter(lambda transformation: word_count_manager.check_word_counts(word2vec, transformation.from_word, transformation.to_word), clazz)
            shuffle(clazz)
            split_count = (len(clazz) + PIECE - 1) / PIECE
            for i in range(split_count):
                l, r = max(0, min(i * PIECE, len(clazz) - PIECE)), min(len(clazz), (i + 1) * PIECE)
                cls.process_class(clazz[l:r], word2vec, syn0norm, fout, nearest_neighbours)
                classTicker2()
            if split_count > 1:
                logger.info("Split class with size {} into {} pieces".format(len(clazz), split_count))
            classTicker()
        fout.close()

    @classmethod
    def process_class(cls, clazz, word2vec, syn0norm, fout, nearest_neighbours):
        PA, B = syn0norm[[transformation.from_word for transformation in clazz]], syn0norm[[transformation.to_word for transformation in clazz]]
        threshold = nearest_neighbours[[transformation.to_word for transformation in clazz]]
        for i in range(len(clazz)):
            A = numpy.array(PA, copy=True)
            delta = syn0norm[clazz[i].to_word] - syn0norm[clazz[i].from_word]
            A += delta
            A /= numpy.linalg.norm(A, axis=1)[:, numpy.newaxis]
            C = (A * B).sum(1)
            indices, = numpy.where(C >= threshold)
            for index in indices:
                if index != i:
                    fout.write("%d %d %d %d\n" % (clazz[index].from_word, clazz[index].to_word, clazz[i].from_word, clazz[i].to_word))
