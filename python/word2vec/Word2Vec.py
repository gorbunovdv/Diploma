import traceback

import numpy
import sys
from gensim.models.word2vec_inner import REAL
from gensim import utils

from python.config.config import config


class Vocab:
    pass


class Word2Vec:
    def __init__(self, fin):
        assert isinstance(fin, file)
        header = fin.readline()
        self.words_count, self.dimensions_count = map(int, header.split())
        letters_set = set(unicode(config["word2vec"]["valid_letters"]))
        self.index2word = []
        i = 0
        binary_length = numpy.dtype(REAL).itemsize * self.dimensions_count
        deleted_words = 0
        while i < self.words_count:
            add_word = True
            cur = Vocab()
            cur.index = i
            try:
                cur.word = self.read_word(fin)
                if not self.check_if_word_is_valid(cur.word, letters_set):
                    add_word = False
            except Exception, e:
                print "UTF encoding failed: skipping word"
                add_word = False
            cur.syn0 = numpy.fromstring(fin.read(binary_length), dtype=REAL)
            if add_word:
                self.index2word.append(cur)
            else:
                i -= 1
                self.words_count -= 1
                deleted_words += 1
            i += 1
        print "Deleted {} words".format(deleted_words)
        print "{} words in model".format(self.words_count)

    @staticmethod
    def check_if_word_is_valid(word, letters_set):
        for letter in word:
            if letter not in letters_set:
                return False
        return True

    @staticmethod
    def read_word(fin):
        word = []
        while True:
            ch = fin.read(1)
            if ch == b' ':
                break
            if ch == b'':
                raise EOFError("unexpected end of input; is count incorrect or file otherwise damaged?")
            if ch != b'\n':  # ignore newlines in front of words (some binary files have)
                word.append(ch)
        return utils.to_unicode(b''.join(word))
