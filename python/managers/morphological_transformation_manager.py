import numpy

from python.config.config import config
from python.logger.logger import Ticker, Logger
from python.transformations_iterator.transformations_iterator import TransformationsReader

logger = Logger("MorphologicalTransformationManager")

class MorphologicalTransformationManager:
    @classmethod
    def calculate_morphological_transformations(cls, word2vec):
        fout = open(config["parameters"]["morphological_transformations_build"]["path"])
        reader = TransformationsReader(config["parameters"]["transformations_filter"]["path"])
        classTicker = Ticker(logger, 0, "classTicker")
        syn0norm = numpy.array(word2vec.syn0, copy=True)
        syn0norm /= numpy.linalg.norm(syn0norm, axis=1)[:, numpy.newaxis]
        min_cos = float(config["parameters"]["morphological_transformations_build"]["min_cos"])
        for clazz in reader.foreachClass(word2vec):
            cls.process_class(clazz, word2vec, syn0norm, fout, min_cos)
            classTicker()
        fout.close()

    @classmethod
    def process_class(cls, clazz, word2vec, syn0norm, fout, min_cos):
        A, B = numpy.array(syn0norm[[transformation.from_word for transformation in clazz]], copy=True), syn0norm[[transformation.to_word for transformation in clazz]]
        for i in range(len(clazz)):
            delta = syn0norm[clazz[i].to_word] - syn0norm[clazz[i].from_word]
            A += delta
            C = (A*B).sum(1)
            indices = numpy.where(C >= min_cos)
            for index in indices:
                print("%s -> %s (%s -> %s)" % (word2vec.index2word[clazz[index].from_word].word, word2vec.index2word[clazz[index].to_word].word,
                                               word2vec.index2word[clazz[i].from_word].word, word2vec.index2word[clazz[i].to_word].word))
