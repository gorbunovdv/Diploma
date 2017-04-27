# coding=utf-8

import numpy
from python.utils import utils

from python.config.config import config
from python.logger.logger import Logger

logger = Logger("Word2Vec")


class Vocab:
    pass

"""
    Класс, реализующий хранение модели Word2Vec. Отсекает слова с символами, не встречающимися в данном языке.
    Реализация аналогична классу Word2Vec в C++.
"""

class Word2Vec:
    def __init__(self, fin):
        assert isinstance(fin, file)
        header = fin.readline()
        self.words_count, self.dimensions_count = map(int, header.split())
        letters_set = set(unicode(config["word2vec"]["valid_letters"]))
        self.index2word = []
        self.vocab = {}
        self.word_list = set()
        i = 0
        binary_length = numpy.dtype(numpy.float32).itemsize * self.dimensions_count
        deleted_words = 0
        syn0 = []
        while i < self.words_count:
            add_word = True
            cur = Vocab()
            cur.index = i
            try:
                cur.word = self.read_word(fin)
                if not self.check_if_word_is_valid(cur.word, letters_set):
                    add_word = False
            except Exception, e:
                logger.info("UTF encoding failed: skipping word")
                add_word = False
            cur.syn0 = numpy.fromstring(fin.read(binary_length), dtype=numpy.float32)
            if add_word:
                self.index2word.append(cur)
                syn0.append(numpy.array(cur.syn0, copy=True))
                self.vocab[cur.word] = cur
                self.word_list.add(cur.word)
            else:
                i -= 1
                self.words_count -= 1
                deleted_words += 1
            i += 1
        self.syn0 = numpy.array(syn0)
        logger.info("Deleted {} words".format(deleted_words))
        logger.info("{} words in model".format(self.words_count))

    """
        Проверить, валидно ли слово, т.е. встречаются ли в нем символы не из алфавита
    """
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
