# coding=utf-8
from collections import defaultdict

from python.config.config import config
from python.logger.logger import Ticker, Logger
from python.utils import utils
from python.utils.utils import to_unicode

logger = Logger("WordCountManager")


def tokenizer(file):
    current_token = []
    while True:
        symbol = file.read(1)
        if symbol == b'':
            break
        if symbol == b' ' or symbol == b'\n' or symbol == b'\t':
            if current_token != b"":
                yield utils.to_unicode(b''.join(current_token))
            current_token = []
        else:
            current_token.append(symbol)
    if current_token != []:
        yield utils.to_unicode(b''.join(current_token))

"""
    Менеджер, осуществующий подсчет частот слов в исходном корпусе текстов
"""
class WordCountManager:
    def __init__(self):
        self.calculate_word_count()

    def calculate_word_count(self):
        self.count = {}
        for [word, count] in map(lambda line: line.split(), open(config["word2vec"]["vocab"]).readlines()):
            try:
                word = to_unicode(word)
            except UnicodeDecodeError:
                logger.info("Could not parse word " + str([word, count]))
            self.count[word] = int(count)

    def check_word_counts(self, word2vec, word1, word2):
        return self.count[word2vec.index2word[word1].word] < self.count[word2vec.index2word[word2].word]
