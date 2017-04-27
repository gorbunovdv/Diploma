# coding=utf-8
from collections import defaultdict

from python.config.config import config
from python.logger.logger import Ticker, Logger
from python.utils import utils

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
        tokens = tokenizer(open(config["parameters"]["raw_model"]["path"], 'r'))
        ticker = Ticker(logger, 0, "calculate_word_count", step=10 ** 6)
        for token in tokens:
            if not token in self.count:
                self.count[token] = 0
            self.count[token] += 1
            ticker()

    def check_word_counts(self, word2vec, word1, word2):
        return self.count[word2vec.index2word[word1].word] < self.count[word2vec.index2word[word2].word]
