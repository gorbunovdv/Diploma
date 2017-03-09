class Transformation:
    PREFIX = 0
    SUFFIX = 1

    def __init__(self, type, from_word, to_delete, to_word, to_add):
        self.type = type
        self.from_word = from_word
        self.to_delete = to_delete
        self.to_word = to_word
        self.to_add = to_add

    def getClass(self, word2vec):
        from_vocab, to_vocab = word2vec.index2word[self.from_word].word, word2vec.index2word[self.to_word].word
        if self.type == Transformation.PREFIX:
            return u"PREFIX:" + from_vocab[:self.to_delete] + u":" + to_vocab[:self.to_add]
        else:
            return u"SUFFIX:" + from_vocab[len(from_vocab) - self.to_delete:] + u":" + to_vocab[len(to_vocab) - self.to_add:]