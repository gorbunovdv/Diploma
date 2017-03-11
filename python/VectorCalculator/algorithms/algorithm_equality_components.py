# coding=utf-8
import gc
import numpy
from pyflann import FLANN

from utils.ticker import Ticker


def get_all_equality_components_with_mincos_strict(vectors_, min_cos, part_size=1000):
    """
    Функция ищет классы эквивалентности среди пар векторов модели >= min_cos.
    Точное решение
    :param vectors_: вектора модели
    :param min_cos: минимальная косинусная метрика
    :param part_size: размер кусочка
    :return: словарь классов эквивалентностей
    """
    vectors = numpy.array(vectors_, copy=True)
    for i in range(len(vectors)):
        vectors[i] /= numpy.linalg.norm(vectors[i])

    def find_root(parent, v):
        if parent[v] != v:
            parent[v] = find_root(parent, parent[v])
        return parent[v]

    def unite(rank, parent, a, b):
        a, b = find_root(parent, a), find_root(parent, b)
        if a != b:
            if rank[a] == rank[b]:
                rank[a] += 1
            if rank[a] > rank[b]:
                a, b = b, a
            parent[a] = b

    parent, rank = list(range(len(vectors))), [0] * len(vectors)
    parts_count = (len(vectors) + part_size - 1) // part_size
    ticker = Ticker("get_all_equality_components_with_mincos_strict",
                    parts_count * (parts_count - 1) // 2 + parts_count)
    for i in range(parts_count):
        for j in range(i, parts_count):
            mat1 = vectors[i * part_size:min(len(vectors), (i + 1) * part_size)]
            mat2 = vectors[j * part_size:min(len(vectors), (j + 1) * part_size)]
            shape = mat2.shape
            mat = numpy.dot(mat1, mat2.T)
            array = numpy.ravel(mat)
            indices, = numpy.where(array >= min_cos)
            for (a, num) in zip(array[indices], indices):
                num1, num2 = num // shape[0] + i * part_size, num % shape[0] + j * part_size
                if num1 < num2:
                    unite(rank, parent, num1, num2)
            ticker.tick()
        gc.collect()
    result = {}
    for i in range(len(vectors)):
        if find_root(parent, i) not in result:
            result[find_root(parent, i)] = []
        result[find_root(parent, i)].append(i)
    return result


def get_all_equality_components_with_mincos_notstrict(vectors_, min_cos, index_filename=None):
    """
    Функция ищет классы эквивалентности среди пар векторов модели >= min_cos.
    Точное решение
    :param vectors_: вектора модели
    :param min_cos: минимальная косинусная метрика
    :param index_filename: индекс векторов модели, если есть
    :return: словарь классов эквивалентностей
    """
    vectors = numpy.array(vectors_, copy=True)
    for i in range(len(vectors)):
        vectors[i] /= numpy.linalg.norm(vectors[i])

    def find_root(parent, v):
        if parent[v] != v:
            parent[v] = find_root(parent, parent[v])
        return parent[v]

    def unite(rank, parent, a, b):
        a, b = find_root(parent, a), find_root(parent, b)
        if a != b:
            if rank[a] == rank[b]:
                rank[a] += 1
            if rank[a] > rank[b]:
                a, b = b, a
            parent[a] = b

    max_dist = 2 * (1 - min_cos)
    pyflann = FLANN(cores=36)
    if index_filename is None:
        pyflann.build_index(vectors)
    else:
        pyflann.load_index(index_filename, vectors)
    parent, rank = list(range(len(vectors))), [0] * len(vectors)
    ticker = Ticker("get_all_equality_components_with_mincos_notstrict", len(vectors))
    for i in range(len(vectors)):
        result, dists = pyflann.nn_radius(vectors[i], max_dist)
        for j in range(len(result)):
            unite(rank, parent, i, result[j])
        if ticker.tick():
            gc.collect()
    result = {}
    for i in range(len(vectors)):
        if find_root(parent, i) not in result:
            result[find_root(parent, i)] = []
        result[find_root(parent, i)].append(i)
    return result
