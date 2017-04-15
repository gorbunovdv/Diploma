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
        for line in filter(lambda line: len(line) > 0, map(lambda line: line.split(), codecs.open(config["parameters"]["word_count"]["path"] + "/result.txt", 'r', 'utf-8').read().split("\n"))):
            self.count[line[0]] = int(line[1])

    @staticmethod
    def calculate_word_count():
        count = defaultdict(int)
        tokens = codecs.open(config["parameters"]["raw_model"]["path"], 'r', 'utf-8').read().split()
        ticker = Ticker(logger, len(tokens), "calculate_word_count")
        for token in tokens:
            count[token] += 1
            ticker()
        fout = codecs.open(config["parameters"]["word_count"]["path"] + "/result.txt", "w", 'utf-8')
        for word, cnt in count.iteritems():
            print type(word)
            fout.write(word)
            fout.write(' ')
            fout.write(str(cnt))
        fout.close()

    def check_word_counts(self, word2vec, word1, word2):
        return self.count[word2vec.index2word[word1].word] >= self.count[word2vec.index2word[word2].word]
