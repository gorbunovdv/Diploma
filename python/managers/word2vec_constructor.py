from python.managers.vector_builder import VectorBuilder


class Word2VecConstructor:
    @staticmethod
    def construct(word2vec, word_count):
        syn0 = {}
        manager = VectorBuilder(word2vec, word_count)
        for word in word_count:
            vector = manager.predict_vector(word)
            if vector is not None:
                syn0[word] = vector
        return syn0
