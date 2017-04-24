from collections import defaultdict

from python.config.config import config
from python.logger.logger import Ticker, Logger

logger = Logger("WordCountManager")


def tokenizer(file):
    current_token = ""
    while True:
        symbol = file.read(1)
        if symbol == "":
            break
        if symbol == ' ' or symbol == '\n':
            if current_token != "":
                yield current_token
            current_token = ""
        else:
            current_token += symbol
    if current_token != "":
        yield current_token


class WordCountManager:
    def __init__(self):
        self.calculate_word_count()

    def calculate_word_count(self):
        self.count = defaultdict(int)
        tokens = tokenizer(open(config["parameters"]["raw_model"]["path"], 'r'))
        ticker = Ticker(logger, 0, "calculate_word_count")
        for token in tokens:
            self.count[token] += 1
            ticker()

    def check_word_counts(self, word2vec, word1, word2):
        return self.count[word2vec.index2word[word1].word] >= self.count[word2vec.index2word[word2].word]
