import sys

import numpy
from gensim.models.word2vec import Word2Vec

import config_utils
from algorithms import gensim_mostsimilar
from algorithms.algorithm_3cosadd import get_all_pairs_with_fixed_relationship_3cosadd_strict, \
    get_all_pairs_with_fixed_relationship_3cosadd_notstrict
from algorithms.algorithm_allpairs import get_all_pairs_with_mincos_strict, get_all_pairs_with_mincos_notstrict
from algorithms.algorithm_equality_components import get_all_equality_components_with_mincos_strict, \
    get_all_equality_components_with_mincos_notstrict
from printer.printers import pairs_with_mincos_printer, relationship_printer, equivalence_class_printer
from tester.evaluators import relationship_evaluator, equivalence_class_evaluator, closest_pairs_evaluator
from tester.tester import test_two_functions

config_utils.init_config(sys.argv)

path_to_model = config_utils.config["model"]

model = Word2Vec.load_word2vec_format(path_to_model, binary=True, unicode_errors='ignore')
if not hasattr(model, 'syn0norm'):
    model.syn0norm = numpy.array(model.syn0)
    model.syn0norm /= numpy.linalg.norm(model.syn0norm, axis=1)[:, numpy.newaxis]

print model.syn0norm.shape


try:
    result = test_two_functions(
        model,
        get_all_pairs_with_fixed_relationship_3cosadd_strict,
        get_all_pairs_with_fixed_relationship_3cosadd_notstrict,
        relationship_evaluator,
        relationship_printer,
        model.syn0norm,
        model.vocab['man'].index,
        model.vocab['woman'].index,
        0.5
    )
except Exception, e:
    print str(e)

try:
    result1, result2 = test_two_functions(
        model,
        get_all_equality_components_with_mincos_strict,
        get_all_equality_components_with_mincos_notstrict,
        equivalence_class_evaluator,
        equivalence_class_printer,
        model.syn0norm,
        0.98
    )
except Exception, e:
    print str(e)

try:
    result = test_two_functions(
        model,
        get_all_pairs_with_fixed_relationship_3cosadd_strict,
        gensim_mostsimilar.gensim_mostsimilar,
        relationship_evaluator,
        relationship_printer,
        model.syn0norm,
        model.vocab['man'].index,
        model.vocab['woman'].index,
        0.7,
        model=model)
except Exception, e:
    print str(e)

