from python.logger.logger import IterableTicker, Logger
from python.managers.vector_builder import VectorBuilder

logger = Logger('Word2VecConstructor')

class Word2VecConstructor:
    @staticmethod
    def construct(word2vec, word_count):
        syn0 = {}
        manager = VectorBuilder(word2vec, word_count)
        for word in IterableTicker(logger, word_count):
            vector = manager.predict_vector(word)
            if vector is not None:
                syn0[word] = vector
        return syn0
