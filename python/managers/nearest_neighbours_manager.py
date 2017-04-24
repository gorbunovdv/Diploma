import numpy

from python.config.config import config
from python.logger.logger import Ticker, Logger

logger = Logger("NearestNeighboursManager")


def func(tup):
    vectors, vectors_t, topk, tick, i = tup
    current = numpy.dot(vectors[i][numpy.newaxis, :], vectors_t)[0]
    current = current[numpy.argpartition(current, len(current) - topk)]
    current = current[len(current) - topk:]
    current = current[numpy.argsort(current)][::-1]
    tick()
    return current


class NearestNeighboursManager:
    @classmethod
    def calculate_nearest_neighbours(cls, word2vec):
        fout = open(config["parameters"]["nearest_neighbours"]["path"], "w")
        cls.get_nearest_neighbours(word2vec.syn0, topk=config["parameters"]["nearest_neighbours"]["topk"],
                                   operator=lambda floats: cls.write_floats_to_file(fout, floats))
        fout.close()

    @staticmethod
    def write_floats_to_file(fout, floats):
        for f in floats:
            fout.write("%.4f " % f)
        fout.write("\n")
        fout.flush()

    @staticmethod
    def read_floats_from_file(fin):
        return numpy.array(map(float, fin.readline().split()))

    @staticmethod
    def get_nearest_neighbours(vectors_, topk, operator):
        vectors = numpy.array(vectors_, copy=True)
        vectors /= numpy.linalg.norm(vectors, axis=1)[:, numpy.newaxis]
        vectors_t = vectors.transpose()
        tick = Ticker(logger, len(vectors), "get_nearest_neighbours")
        for current in pool.imap(func, [(vectors, vectors_t, topk, tick, i) for i in range(len(vectors))]):
            operator(current)

    @classmethod
    def load_nearest_neighbours(cls, word2vec):
        fin = open(config["parameters"]["nearest_neighbours"]["path"], "r")
        return numpy.array([
                               cls.read_floats_from_file(fin)
                               for _ in range(word2vec.words_count)
                               ])


from python.pool.pool import pool
