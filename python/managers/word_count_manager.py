class WordCountManager:
    def check_word_counts(self, word2vec, word1, word2):
        return len(word2vec.index2word[word1].word) >= len(word2vec.index2word[word2].word)
