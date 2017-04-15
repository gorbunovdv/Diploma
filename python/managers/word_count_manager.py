import os
from collections import defaultdict
from itertools import imap
import codecs

from python.config.config import config
from python.logger.logger import Ticker, Logger

logger = Logger("WordCountManager")

class WordCountManager:
    def __init__(self):
        if not os.path.exists(config["parameters"]["word_count"]["path"] + "/result.txt"):
            self.calculate_word_count()
        self.count = {}
        for line in filter(lambda line: len(line) > 0, map(lambda line: line.split(), open(config["parameters"]["word_count"]["path"] + "/result.txt", 'r').read().split("\n"))):
            self.count[line[0]] = int(line[1])

    @staticmethod
    def calculate_word_count():
        count = defaultdict(int)
        tokens = open(config["parameters"]["raw_model"]["path"], 'r').read().split()
        ticker = Ticker(logger, len(tokens), "calculate_word_count")
        for token in tokens:
            count[token] += 1
            ticker()
        fout = open(config["parameters"]["word_count"]["path"] + "/result.txt", "w")
        for word, cnt in count.iteritems():
            fout.write(word.encode('utf-8'))
            fout.write(' ')
            fout.write(str(cnt))
            fout.write("\n")
        fout.close()

    def check_word_counts(self, word2vec, word1, word2):
        return self.count[word2vec.index2word[word1].word] >= self.count[word2vec.index2word[word2].word]
