from pyflann import FLANN

from algorithms.algorithm_allpairs import get_all_pairs_with_mincos_strict
from config_utils import config


def save_flann_indices(vectors, filename):
    flann = FLANN(cores=36)
    flann.build_index(vectors)
    flann.save_index(filename=filename)


def save_usual_indices(vectors, filename, min_cos):
    pairs = get_all_pairs_with_mincos_strict(vectors, min_cos)
    fout = open(filename, "w")
    for d, u, v in pairs:
        fout.write("%.20f %d %d\n" % (d, u, v))
    fout.close()


def load_usual_indices(filename):
    lines = open(filename).readlines()
    separated = [line.split() for line in lines]
    return [(float(split[0]), int(split[1]), int(split[2])) for split in separated]


def save_clustering(clustering, filename):
    fout = open(filename, "w")
    fout.write(" ".join(map(str, clustering)))
    fout.close()


def load_clustering(filename):
    return map(int, open(filename).read().strip().split())
