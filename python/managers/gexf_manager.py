from gexf import Gexf

from python.config.config import config
from python.logger.logger import IterableTicker, Logger

logger = Logger("GexfManager")


class GexfManager:
    @staticmethod
    def add_gexf_format(path1, path2, word2vec):
        gexf = Gexf("Creator", "Acyclic Graph")
        graph = gexf.addGraph("directed", "statis", "Acyclic Graph")
        for index, vocab in enumerate(word2vec.index2word):
            graph.addNode(index, vocab.word)
        for index, (i1, i2, i3, i4) in enumerate(map(int, line.split()) for line in IterableTicker(logger, open(path1), 10 ** 6)):
            graph.addEdge(index, i1, i2)
        fout = open(path2, "w")
        gexf.write(fout)
