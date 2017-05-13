import numpy

from python.config.config import config
from python.logger.logger import Logger
from python.managers.vector_builder import VectorBuilder
from python.managers.word2vec_constructor import Word2VecConstructor
from python.managers.word_count_manager import WordCountManager
from python.word2vec.Word2Vec import Word2Vec
from python.utils.utils import to_unicode

logger = Logger("Demonstrator")


model_name, model_path = config["word2vec"]["model"], config["word2vec"]["path"]
logger.info("Using {} as a Word2Vec model".format(model_name))
with open(model_path, "r") as fin:
    word2vec = Word2Vec(fin)

word_count_manager = WordCountManager()
manager = VectorBuilder(word2vec, word_count_manager.count)
initial_vocab = word2vec.generate_vocab()

while True:
    word = raw_input("Enter single word: ")
    word = to_unicode(word)
    if not word2vec.check_if_word_is_valid(word, word2vec.letters_set):
        print "Word contains inadequate symbols"
        continue
    print "Initial Vocab:", word
    if word not in initial_vocab:
        print "Word is not in Initial Vocab"
    else:
        vector = initial_vocab[word]
        print "Frequency is {}".format(word_count_manager.count[word])
        distances = sorted([(numpy.dot(vector / numpy.linalg.norm(vector), vector2 / numpy.linalg.norm(vector2)), word2) for word2, vector2 in initial_vocab.iteritems()], reverse=True)[:10]
        for distance2, word2 in distances:
            print word2, "\t" * 3, distance2, "\t" * 3, word_count_manager.count[word2]
    vector = manager.predict_vector(word, print_transformation=True)
    if vector is None:
        print "Could not predict vector"
        continue
    distances = sorted([(numpy.dot(vector / numpy.linalg.norm(vector), vector2 / numpy.linalg.norm(vector2)), word2) for word2, vector2 in initial_vocab.iteritems()], reverse=True)[:10]
    for distance2, word2 in distances:
        print word2, "\t" * 3, distance2, "\t" * 3, word_count_manager.count[word2]
