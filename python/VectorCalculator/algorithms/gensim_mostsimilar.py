import sys
from gensim.models import Word2Vec

from utils.ticker import Ticker


def gensim_mostsimilar(vectors, index1, index2, min_cos, model):
    assert isinstance(model, Word2Vec)
    result = []
    ticker = Ticker("gensim_mostsimilar", len(vectors))
    for word in range(len(vectors)):
        result.extend(
            filter(lambda x: x[0] >= min_cos, map(lambda x: (x[1], word, model.vocab[x[0]].index), model.most_similar(positive=[model.index2word[index1], model.index2word[word]],
                                                                 negative=[model.index2word[index2]]))))
        if ticker.tick():
            print >> sys.stderr, "Pairs count: ", len(result)
    result.sort(reverse=True)
    return result
