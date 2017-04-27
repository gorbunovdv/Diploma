from itertools import imap

import numpy

from python.utils import utils


class EvaluateManager:
    @staticmethod
    def evaluate(fin, fout, vocab):
        for word1, word2, sim in imap(lambda line: line.strip().split(","), fin):
            if word1 == 'word1' and word2 == 'word2' and sim == 'sim':
                fout.write("{},{},{},{}\n".format(word1, word2, sim, 'usim'))
            else:
                word1 = utils.to_unicode(word1)
                word2 = utils.to_unicode(word2)
                cos = numpy.dot(vocab[word1] / numpy.linalg.norm(vocab[word1]), vocab[word2]  / numpy.linalg.norm(vocab[word2]))
                fout.write("{},{},{},{}\n".format(word1, word2, sim, cos))
        fout.close()
