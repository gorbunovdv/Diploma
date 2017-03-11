# coding=utf-8
import gc
import sys
import numpy
from pyflann import FLANN

from datastructures.resizeable_list import resizeable_tuple_three
from utils.ticker import Ticker


def get_all_pairs_two_spaces_with_mincos_strict_basic(mat1, mat2, i, j, part_size, min_cos):
    shape = mat2.shape
    mat = numpy.dot(mat1, mat2.T)
    array = numpy.ravel(mat)
    indices, = numpy.where(array >= min_cos)
    pairs = resizeable_tuple_three()
    for (a, num) in zip(array[indices], indices):
        num1, num2 = num // shape[0] + i * part_size, num % shape[0] + j * part_size
        pairs.append((a, num1, num2))
    return pairs


def get_all_pairs_two_spaces_with_mincos_strict(vectors1_, vectors2_, min_cos, part_size=1000, disable_ticker=False):
    """
    Функция ищет все пары векторов из двух векторных пространств таких, что косинусная метрика между ними >= min_cos
    Точное решение
    :param vectors1_: вектора модели первого векторного пространства
    :param vectors2_: вектора модели второго векторного пространства
    :param min_cos: минимальная косинусная метрика
    :param part_size: внутренний размер кусочка, на которые бьются вектора
    :return: список (d, u, v), где u, v - два индекса векторов, а d - расстояние между ними
    """
    vectors1 = numpy.array(vectors1_, copy=True)
    vectors1 /= numpy.linalg.norm(vectors1, axis=1)[:, numpy.newaxis]
    vectors2 = numpy.array(vectors2_, copy=True)
    vectors2 /= numpy.linalg.norm(vectors2, axis=1)[:, numpy.newaxis]
    pairs = resizeable_tuple_three()
    parts_count1 = (len(vectors1) + part_size - 1) // part_size
    parts_count2 = (len(vectors2) + part_size - 1) // part_size
    if not disable_ticker:
        ticker = Ticker("get_all_pairs_two_spaces_with_mincos_strict", parts_count1 * parts_count2)
    for i in range(parts_count1):
        for j in range(parts_count2):
            mat1 = vectors1[i * part_size:min(len(vectors1), (i + 1) * part_size)]
            mat2 = vectors2[j * part_size:min(len(vectors2), (j + 1) * part_size)]
            pairs.extend(get_all_pairs_two_spaces_with_mincos_strict_basic(mat1, mat2, i, j, part_size, min_cos))
            if not disable_ticker:
                if ticker.tick():
                    print >> sys.stderr, "Pairs count: ", len(pairs)
        gc.collect()
    return pairs


def get_all_pairs_two_spaces_with_mincos_notstrict(vectors1_, vectors2_, min_cos, index_filename=None):
    """
    Функция ищет все пары векторов из двух векторных пространств таких, что косинусная метрика между ними >= min_cos
    Неточное решение
    :param vectors1_: вектора модели первого векторного пространства
    :param vectors2_: вектора модели второго векторного пространства
    :param min_cos: минимальная косинусная метрика
    :param index_filename: путь к сохраненному индексу, если есть
    :return: список (d, u, v), где u, v - два индекса векторов, а d - квадрат расстояния между ними
    """
    vectors1 = numpy.array(vectors1_, copy=True)
    vectors1 /= numpy.linalg.norm(vectors1, axis=1)[:, numpy.newaxis]
    vectors2 = numpy.array(vectors2_, copy=True)
    vectors2 /= numpy.linalg.norm(vectors2, axis=1)[:, numpy.newaxis]
    pairs = resizeable_tuple_three()
    pyflann = FLANN(cores=36)
    if index_filename is None:
        pyflann.build_index(vectors1)
    else:
        pyflann.load_index(index_filename, vectors1)
    max_dist = 2 * (1 - min_cos)
    ticker = Ticker("get_all_pairs_with_mincos_notstrict", len(vectors2))
    for i in range(len(vectors2)):
        result, dists = pyflann.nn_radius(vectors2[i], max_dist)
        for j in range(len(result)):
            pairs.append((dists[j] ** 0.5, i, result[j]))
        if ticker.tick():
            gc.collect()
    return pairs
