import os
from collections import defaultdict
from itertools import imap

from python.config.config import config
from python.logger.logger import Ticker, Logger

logger = Logger("WordCountManager")

class WordCountManager:
    def __init__(self):
        if not os.path.exists(config["parameters"]["word_count"]["path"] + "/result.txt"):
            self.calculate_word_count()
        self.count = {word: int(count) for [word, count] in open(config["parameters"]["word_count"]["path"] + "/result.txt").read().split()}

    @staticmethod
    def calculate_word_count():
        count = defaultdict(int)
        tokens = open(config["parameters"]["raw_model"]["path"]).read().split()
        ticker = Ticker(logger, len(tokens), "calculate_word_count")
        for token in tokens:
            count[token] += 1
            ticker()
        fout = open(config["parameters"]["word_count"]["path"] + "/result.txt")
        for entity in count.iteritems():
            fout.write("%s %d\n" % entity)
        fout.close()

    def check_word_counts(self, word2vec, word1, word2):
        return self.count[word2vec.index2word[word1].word] >= self.count[word2vec.index2word[word2].word]
