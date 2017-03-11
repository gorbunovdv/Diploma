# coding=utf-8
import numpy
import sys

from algorithms.algorithm_allpairs_two_spaces import get_all_pairs_two_spaces_with_mincos_notstrict
from utils.ticker import Ticker
from datastructures.resizeable_list import resizeable_tuple_three, resizeable_tuple_five


def get_all_pairs_with_mincos_strict_basic(mat1, mat2, i, j, part_size, min_cos):
    mat1 = numpy.array(mat1, copy=True)
    mat1 /= numpy.linalg.norm(mat1, axis=1)[:, numpy.newaxis]
    mat2 = numpy.array(mat2, copy=True)
    mat2 /= numpy.linalg.norm(mat2, axis=1)[:, numpy.newaxis]
    shape = mat2.shape
    mat = numpy.dot(mat1, mat2.T)
    array = numpy.ravel(mat)
    indices, = numpy.where(array >= min_cos)
    pairs = resizeable_tuple_three()
    for (a, num) in zip(array[indices], indices):
        num1, num2 = num // shape[0] + i * part_size, num % shape[0] + j * part_size
        if num1 < num2:
            pairs.append((a, num1, num2))
    return pairs


def get_all_pairs_with_mincos_strict(vectors_, min_cos, part_size=1000):
    """
    Функция ищет все пары векторов таких, что косинусная метрика между ними >= min_cos
    Точное решение
    :param vectors_: вектора модели
    :param min_cos: минимальная косинусная метрика
    :param part_size: внутренний размер кусочка, на которые бьются вектора
    :return: список (d, u, v), где u, v - два индекса векторов, а d - расстояние между ними
    """
    vectors = numpy.array(vectors_, copy=True)
    vectors /= numpy.linalg.norm(vectors, axis=1)[:, numpy.newaxis]
    pairs = resizeable_tuple_three()
    parts_count = (len(vectors) + part_size - 1) // part_size
    ticker = Ticker("get_all_pairs_with_mincos_strict", parts_count * (parts_count - 1) // 2 + parts_count)
    for i in range(parts_count):
        for j in range(i, parts_count):
            mat1 = vectors[i * part_size:min(len(vectors), (i + 1) * part_size)]
            mat2 = vectors[j * part_size:min(len(vectors), (j + 1) * part_size)]
            new_pairs = get_all_pairs_with_mincos_strict_basic(mat1, mat2, i, j, part_size, min_cos)
            pairs.extend(new_pairs)
            if ticker.tick():
                print >> sys.stderr, "Pairs count: ", len(pairs)
    return pairs


def get_all_pairs_with_mincos_notstrict(vectors_, min_cos, index_filename=None):
    """
    Функция ищет все пары векторов таких, что косинусная метрика между ними >= min_cos
    Неточное решение
    :param vectors_: вектора модели
    :param min_cos: минимальная косинусная метрика
    :param index_filename: путь к сохраненному индексу, если есть
    :return: список (d, u, v), где u, v - два индекса векторов, а d - квадрат расстояния между ними
    """
    return filter(lambda x: x[1] < x[2],
                  get_all_pairs_two_spaces_with_mincos_notstrict(vectors_, vectors_, min_cos, index_filename))
