import sys

import numpy
from gensim.models.word2vec import Word2Vec

import config_utils
from algorithms.algorithm_3cosadd_not_fixed_relationship import get_all_fours_with_relationship_3cosadd_strict
from printer.printers import fours_with_not_fixed_relationship_printer
from tester.tester import test_single_function

config_utils.init_config(sys.argv)

path_to_model = config_utils.config["model"]

model = Word2Vec.load_word2vec_format(path_to_model, binary=True, unicode_errors='ignore')
if not hasattr(model, 'syn0norm'):
    model.syn0norm = numpy.array(model.syn0)
    model.syn0norm /= numpy.linalg.norm(model.syn0norm, axis=1)[:, numpy.newaxis]
try:
    result = test_single_function(
        model,
        get_all_fours_with_relationship_3cosadd_strict,
        fours_with_not_fixed_relationship_printer,
        model.syn0norm,
        1000,
        0.9
    )
except Exception, e:
    print str(e)



