# coding=utf-8
import gc
import numpy
from sklearn.cluster import MiniBatchKMeans

from algorithms.algorithm_3cosadd import get_all_pairs_with_fixed_relationship_3cosadd_strict
from datastructures.resizeable_list import resizeable_tuple_five
from savers.savers import load_clustering
from utils.ticker import Ticker


def get_all_fours_with_relationship_3cosadd_strict_without_clustering(vectors, clustering, min_cos):
    """
    Функция ищет все четверки слов, которые образуют одинаковые отношения с помощью 3cosadd и готовой кластеризации.
    Ищутся исключительно четверки слов такие, что все четыре слова лежат в одном кластере.
    Точное решение.
    :param vectors: вектора модели
    :param clustering: кластеризация
    :param min_cos: минимальная косинусная метрика
    :return: cписок (d, a1, b1, a2, b2), где a1, b1 образуют то же отношение, что и a2, b2, d - расстояние между парами
    """
    clusters = {}
    for index in range(len(clustering)):
        if clustering[index] not in clusters:
            clusters[clustering[index]] = []
        clusters[clustering[index]].append(index)
    for cluster in clusters:
        clusters[cluster] = numpy.array(clusters[cluster])
    result = resizeable_tuple_five()
    ticker = Ticker("get_all_fours_with_relationship_3cosadd_strict_without_clustering", len(clusters))
    for cluster_index in clusters:
        cluster = clusters[cluster_index]
        for index1 in range(len(cluster)):
            for index2 in range(len(cluster)):
                cluster_result = get_all_pairs_with_fixed_relationship_3cosadd_strict(vectors[cluster], index1,
                                                                                      index2, min_cos, disable_ticker=True)
                for distance, word1, word2 in cluster_result:
                    result.append((distance, cluster[index1], cluster[index2], cluster[word1], cluster[word2]))
        if ticker.tick():
            print "Fours count: ", len(result)
            gc.collect()
    return result


def get_clustering(vectors, n_clusters, max_iter=None, n_init=None):
    """
    Функция ищет кластеризацию данных векторов
    :param vectors: вектора модели
    :param n_clusters: количество кластеров
    :param max_iter: максимальное количество итераций
    :param n_init: количество инициализаций
    :return: список номеров кластеров для каждого вектора
    """
    if max_iter is None:
        max_iter = 100
    if n_init is None:
        n_init = 3
    clustering_sklearn = MiniBatchKMeans(n_clusters, max_iter=max_iter, n_init=n_init)
    return clustering_sklearn.fit_predict(vectors)


def get_all_fours_with_relationship_3cosadd_strict(vectors, n_clusters, min_cos, index_filename=None, max_iter=None,
                                                   n_init=None):
    """
    Функция ищет все четверки слов, которые образуют одинаковые отношения с помощью 3cosadd.
    Ищутся исключительно четверки слов такие, что все четыре слова лежат в одном кластере.
    Точное решение.
    :param vectors: вектора модели
    :param n_clusters: количество кластеров
    :param min_cos: минимальная косинусная метрика
    :param index_filename: путь к сохраненной кластеризации, если есть
    :param max_iter: максимальное количество итераций
    :param n_init: количество инициализаций
    :return: cписок (d, a1, b1, a2, b2), где a1, b1 образуют то же отношение, что и a2, b2, d - расстояние между парами
    """
    clustering = get_clustering(vectors, n_clusters, max_iter, n_init) if index_filename is None else load_clustering(
        index_filename)
    return get_all_fours_with_relationship_3cosadd_strict_without_clustering(vectors, clustering, min_cos)
