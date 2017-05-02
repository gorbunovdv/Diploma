from itertools import imap

import numpy

from python.logger.logger import Logger
from python.utils import utils

logger = Logger("EvaluateManager")


class EvaluateManager:
    @staticmethod
    def evaluate(fin, fout, vocab):
        for word1, word2, sim in imap(lambda line: line.strip().split(","), fin):
            if word1 == 'word1' and word2 == 'word2' and sim == 'sim':
                fout.write("{},{},{},{}\n".format(word1, word2, sim, 'usim'))
            else:
                word1 = utils.to_unicode(word1)
                word2 = utils.to_unicode(word2)
                if word1 not in vocab or word2 not in vocab:
                    cos = 0
                    if word1 not in vocab:
                        logger.info((word1 + u": not found!").encode('utf-8'))
                    if word2 not in vocab:
                        logger.info((word2 + u": not found!").encode('utf-8'))
                    logger.info((u"Pair was " + word1 + " -> " + word2).encode('utf-8'))
                else:
                    cos = numpy.dot(vocab[word1] / numpy.linalg.norm(vocab[word1]),
                                    vocab[word2] / numpy.linalg.norm(vocab[word2]))
                fout.write(word1.encode('utf-8'))
                fout.write(',')
                fout.write(word2.encode('utf-8'))
                fout.write(',')
                fout.write(sim)
                fout.write(',')
                fout.write(str(abs(cos)))
                fout.write("\n")
        fout.close()
