# coding=utf-8
from collections import defaultdict
from itertools import imap

import numpy

from python.config.config import config
from python.word2vec.Word2Vec import Word2Vec

"""
    Менеджер, осуществляющий подсчет векторов для редких слов
"""
class VectorBuilder:
    def __init__(self, word2vec, word_count):
        assert isinstance(word2vec, Word2Vec)
        self.word2vec = word2vec
        graph_filename = config["parameters"]["acyclic_graph"]["path"] + "/result.txt"
        self.mapping = defaultdict(lambda: -1)
        for word1, word2, word3, word4 in imap(lambda line: map(int, line.split()), open(graph_filename)):
            self.mapping[word1] = word2
        self.transformation, self.length, self.s_transformations = self.calculate_rs(word2vec, self.mapping)
        self.word_count = word_count

    def __getitem__(self, item):
        vector = self.predict_vector(item)
        if vector is None:
            raise KeyError()
        return vector

    def __contains__(self, item):
        vector = self.predict_vector(item)
        return vector is not None

    """
        Насчитать множество RS по ациклическому графу
    """
    @classmethod
    def calculate_rs(cls, word2vec, mapping):
        used = defaultdict(bool)
        topological_sorting = []

        def dfs(word_index, mapping, topological_sorting, used):
            if used[word_index]:
                return
            used[word_index] = True
            if word_index in mapping and mapping[word_index] != -1:
                dfs(mapping[word_index], mapping, topological_sorting, used)
            topological_sorting.append(word_index)

        for word_index in range(len(word2vec.index2word)):
            dfs(word_index, mapping, topological_sorting, used)

        transformation = {}
        length = {}

        for word in topological_sorting:
            if mapping[word] == -1:
                transformation[word], length[word] = ('', '', '', ''), 0
            else:
                transformation[word], length[word] = cls.composite(word2vec.index2word[word].word,
                                                                   word2vec.index2word[mapping[word]].word,
                                                                   transformation[mapping[word]]), \
                                                     length[mapping[word]] + 1

        transformations = defaultdict(lambda: defaultdict(list))
        s_transformations = defaultdict(lambda: defaultdict(list))

        print "Max length: ", max(length)

        for i in range(len(transformation)):
            if transformation[i] == ('', '', '', ''):
                continue
            p_delete, p_add, s_delete, s_add = transformation[i]
            transformations[p_delete][s_delete].append((p_add, s_add, length[i]))

        for vertex, to_vertex in mapping.iteritems():
            if to_vertex == -1:
                continue
            p_delete, p_add, s_delete, s_add = cls.composite(word2vec.index2word[vertex].word,
                                                   word2vec.index2word[to_vertex].word,
                                                   ('', '', '', ''))
            if (p_delete, p_add, s_delete, s_add) == ('', '', '', ''):
                continue
            s_transformations[p_delete][s_delete].append((p_add, s_add))

        return transformations, length, s_transformations

    """
        Применить преобразование, образованное словами word1, word2 к преобразованию transformation
    """
    @classmethod
    def composite(cls, word1, word2, transformation):
        p_delete, p_add, s_delete, s_add = transformation
        lca1, lca2 = 0, 1
        while lca1 < len(word1) and lca1 < len(word2) and word1[lca1] == word2[lca1]:
            lca1 += 1
        while lca2 < len(word1) and lca2 < len(word2) and word1[-lca2] == word2[-lca2]:
            lca2 += 1
        lca2 -= 1
        if lca1 > lca2:
            c1, c2 = word1[lca1:], word2[lca1:]
            s_delete, s_add = cls.update_suffix(c1, c2, s_delete, s_add)
        else:
            c1, c2 = word1[:-lca2], word2[:-lca2]
            p_delete, p_add = cls.update_prefix(c1, c2, p_delete, p_add)
        return p_delete, p_add, s_delete, s_add

    @classmethod
    def update_prefix(cls, w1, w2, w3, w4):
        if len(w2) > len(w3):
            w4 = w2[:len(w2) - len(w3)] + w4
        else:
            w1 = w3[:len(w3) - len(w2)] + w1
        return w1, w4

    @classmethod
    def update_suffix(cls, w1, w2, w3, w4):
        w1, w2, w3, w4 = ("".join(reversed(w)) for w in (w1, w2, w3, w4))
        w1, w4 = cls.update_prefix(w1, w2, w3, w4)
        w1, w4 = ("".join(reversed(w)) for w in (w1, w4))
        return "".join(reversed(w1)), "".join(reversed(w4))

    """
        Предсказать вектор для слова word
    """
    def predict_vector(self, word, print_transformation=False, demonstration=False):
        if not demonstration and word in self.word2vec.word_list and self.word_count[word] >= 100:
            return self.word2vec.syn0[self.word2vec.vocab[word].index]
        best = ""
        for prefix in range(-1, len(word)):
            for suffix in range(prefix + 1, len(word) + 1):
                s1, s2 = word[:prefix + 1], word[suffix:]
                for (add_left, add_right, length) in self.transformation[s1][s2]:
                    result = add_left + word[prefix + 1:suffix] + add_right
                    if result in self.word2vec.vocab and self.word_count[result] >= 100 and (best == "" or self.word_count[result] > self.word_count[best]):
                        best = result
        if best != "":
            if print_transformation:
                print word, ' -> ', best
            return self.word2vec.vocab[best].syn0

        for prefix in range(-1, len(word)):
            for suffix in range(prefix + 1, len(word) + 1):
                s1, s2 = word[:prefix + 1], word[suffix:]
                for (add_left, add_right) in self.s_transformations[s1][s2]:
                    result = add_left + word[prefix + 1:suffix] + add_right
                    if result in self.word2vec.vocab and self.word_count[result] >= 100:
                        if print_transformation:
                            print word, ' -> ', result
                        return self.word2vec.syn0[self.word2vec.vocab[result].index]

        if word in self.word2vec.vocab:
            if print_transformation:
                print "Could not find transformation: using Word2Vec vector"
            return self.word2vec.vocab[word].syn0

        return None

"""
    Менеджер, осуществляющий подсчет векторов для редких слов
"""
class OffsetVectorBuilder:
    def __init__(self, word2vec, word_count):
        assert isinstance(word2vec, Word2Vec)
        self.word2vec = word2vec
        graph_filename = config["parameters"]["acyclic_graph"]["path"] + "/result.txt"
        self.mapping = defaultdict(lambda: -1)
        for word1, word2, word3, word4 in imap(lambda line: map(int, line.split()), open(graph_filename)):
            self.mapping[word1] = word2
        self.transformation, self.length, self.s_transformations = self.calculate_rs(word2vec, self.mapping)
        self.word_count = word_count

    def __getitem__(self, item):
        vector = self.predict_vector(item)
        if vector is None:
            raise KeyError()
        return vector

    def __contains__(self, item):
        vector = self.predict_vector(item)
        return vector is not None

    """
        Насчитать множество RS по ациклическому графу
    """
    @classmethod
    def calculate_rs(cls, word2vec, mapping):
        used = defaultdict(bool)
        topological_sorting = []

        def dfs(word_index, mapping, topological_sorting, used):
            if used[word_index]:
                return
            used[word_index] = True
            if word_index in mapping and mapping[word_index] != -1:
                dfs(mapping[word_index], mapping, topological_sorting, used)
            topological_sorting.append(word_index)

        for word_index in range(len(word2vec.index2word)):
            dfs(word_index, mapping, topological_sorting, used)

        transformation = {}
        length = {}

        for word in topological_sorting:
            if mapping[word] == -1:
                transformation[word], length[word] = ('', '', '', '', numpy.zeros(word2vec.dimensions_count)), 0
            else:
                transformation[word], length[word] = cls.composite(word2vec.index2word[word].word,
                                                                   word2vec.index2word[mapping[word]].word,
                                                                   transformation[mapping[word]],
                                                                   word2vec.index2word[word].syn0 - word2vec.index2word[mapping[word]].syn0), \
                                                     length[mapping[word]] + 1

        transformations = defaultdict(lambda: defaultdict(list))
        s_transformations = defaultdict(lambda: defaultdict(list))

        print "Max length: ", max(length)

        for i in range(len(transformation)):
            p_delete, p_add, s_delete, s_add, offset = transformation[i]
            if (p_delete, p_add, s_delete, s_add) == ('', '', '', ''):
                continue
            transformations[p_delete][s_delete].append((p_add, s_add, length[i], offset))

        for vertex, to_vertex in mapping.iteritems():
            if to_vertex == -1:
                continue
            p_delete, p_add, s_delete, s_add, offset = cls.composite(word2vec.index2word[vertex].word,
                                                   word2vec.index2word[to_vertex].word,
                                                   ('', '', '', '', numpy.zeros(word2vec.dimensions_count)), word2vec.index2word[vertex].syn0 - word2vec.index2word[to_vertex].syn0)
            if (p_delete, p_add, s_delete, s_add) == ('', '', '', ''):
                continue
            s_transformations[p_delete][s_delete].append((p_add, s_add, offset))

        return transformations, length, s_transformations

    """
        Применить преобразование, образованное словами word1, word2 к преобразованию transformation
    """
    @classmethod
    def composite(cls, word1, word2, transformation, offset):
        p_delete, p_add, s_delete, s_add, vector = transformation
        lca1, lca2 = 0, 1
        while lca1 < len(word1) and lca1 < len(word2) and word1[lca1] == word2[lca1]:
            lca1 += 1
        while lca2 < len(word1) and lca2 < len(word2) and word1[-lca2] == word2[-lca2]:
            lca2 += 1
        lca2 -= 1
        if lca1 > lca2:
            c1, c2 = word1[lca1:], word2[lca1:]
            s_delete, s_add = cls.update_suffix(c1, c2, s_delete, s_add)
        else:
            c1, c2 = word1[:-lca2], word2[:-lca2]
            p_delete, p_add = cls.update_prefix(c1, c2, p_delete, p_add)
        return p_delete, p_add, s_delete, s_add, vector + offset

    @classmethod
    def update_prefix(cls, w1, w2, w3, w4):
        if len(w2) > len(w3):
            w4 = w2[:len(w2) - len(w3)] + w4
        else:
            w1 = w3[:len(w3) - len(w2)] + w1
        return w1, w4

    @classmethod
    def update_suffix(cls, w1, w2, w3, w4):
        w1, w2, w3, w4 = ("".join(reversed(w)) for w in (w1, w2, w3, w4))
        w1, w4 = cls.update_prefix(w1, w2, w3, w4)
        w1, w4 = ("".join(reversed(w)) for w in (w1, w4))
        return "".join(reversed(w1)), "".join(reversed(w4))

    """
        Предсказать вектор для слова word
    """
    def predict_vector(self, word, print_transformation=False, demonstration=False):
        if not demonstration and word in self.word2vec.word_list and self.word_count[word] >= 100:
            return self.word2vec.syn0[self.word2vec.vocab[word].index]
        best = ""
        best_offset = None
        for prefix in range(-1, len(word)):
            for suffix in range(prefix + 1, len(word) + 1):
                s1, s2 = word[:prefix + 1], word[suffix:]
                for (add_left, add_right, length, offset) in self.transformation[s1][s2]:
                    result = add_left + word[prefix + 1:suffix] + add_right
                    if result in self.word2vec.vocab and self.word_count[result] >= 100 and (best == "" or self.word_count[result] > self.word_count[best]):
                        best = result
                        best_offset = offset
        if best != "":
            if print_transformation:
                print word, ' -> ', best
            return self.word2vec.vocab[best].syn0 + best_offset

        for prefix in range(-1, len(word)):
            for suffix in range(prefix + 1, len(word) + 1):
                s1, s2 = word[:prefix + 1], word[suffix:]
                for (add_left, add_right, offset) in self.s_transformations[s1][s2]:
                    result = add_left + word[prefix + 1:suffix] + add_right
                    if result in self.word2vec.vocab and self.word_count[result] >= 100:
                        if print_transformation:
                            print word, ' -> ', result
                        return self.word2vec.syn0[self.word2vec.vocab[result].index] + offset

        if word in self.word2vec.vocab:
            if print_transformation:
                print "Could not find transformation: using Word2Vec vector"
            return self.word2vec.vocab[word].syn0

        return None
