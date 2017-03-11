# coding=utf-8
import numpy

from algorithms.algorithm_allpairs_two_spaces import get_all_pairs_two_spaces_with_mincos_strict, \
    get_all_pairs_two_spaces_with_mincos_notstrict


def get_all_pairs_with_fixed_relationship_3cosadd_strict(vectors_, index1, index2, min_cos, model=None):
    """
    Функция ищет все пары слов, которые образуют фиксированное отношение с помощью 3cosadd.
    Точное решение.
    :param vectors_: вектора модели
    :param index1: индекс первого слова в отношении
    :param index2: индекс второго слова в отношении
    :param min_cos: минимальная косинусная метрика
    :return: список (d, u, v), где u, v образуют то же отношение, что и index1, index2, d - расстояние между парами
    """
    modified_vectors = numpy.array(vectors_, copy=True)
    for i in range(len(modified_vectors)):
        modified_vectors[i] += vectors_[index2] - vectors_[index1]
    return filter(lambda x: x[1] != x[2],
                  get_all_pairs_two_spaces_with_mincos_strict(vectors_, modified_vectors, min_cos))


def get_all_pairs_with_fixed_relationship_3cosadd_notstrict(vectors_, index1, index2, min_cos, index_filename=None):
    """
    Функция ищет все пары слов, которые образуют фиксированное отношение с помощью 3cosadd.
    Неточное решение.
    :param vectors_: вектора модели
    :param index1: индекс первого слова в отношении
    :param index2: индекс второго слова в отношении
    :param min_cos: минимальная косинусная метрика
    :param index_filename: путь к насчитанному индексу модели, если она есть
    :return: список (d, u, v), где u, v образуют то же отношение, что и index1, index2, d - квадрат расстояния между парами
    """
    modified_vectors = numpy.array(vectors_, copy=True)
    for i in range(len(modified_vectors)):
        modified_vectors[i] += vectors_[index2] - vectors_[index1]
    return filter(lambda x: x[1] != x[2],
                  get_all_pairs_two_spaces_with_mincos_notstrict(vectors_, modified_vectors, min_cos, index_filename))
