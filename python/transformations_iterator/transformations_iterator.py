import struct
from os import listdir
from os.path import isfile, join

from python.logger.logger import Logger
from python.structures.transformation import Transformation

logger = Logger("TransformationReader")


class TransformationsReader:
    def __init__(self, path):
        self.files = sorted([join(path, file) for file in listdir(path) if isfile(join(path, file))])

    @staticmethod
    def readInt(file):
        bytes = file.read(4)
        if bytes == b'':
            raise EOFError()
        return struct.unpack("<L", bytes)[0]

    def generate(self):
        for file in self.files:
            logger.info("Reading file {}".format(file))
            with open(file) as fin:
                while True:
                    try:
                        from_word, to_delete, to_word, to_add, typ = [TransformationsReader.readInt(fin) for _ in
                                                                      range(5)]
                        yield Transformation(typ, from_word, to_delete, to_word, to_add)
                    except EOFError:
                        break

    def foreachClass(self, word2vec):
        current_class = []
        current_class_type = u""
        for transformation in self.generate():
            next_class_type = transformation.getClass(word2vec)
            if len(current_class) == 0 or next_class_type == current_class_type:
                current_class.append(transformation)
            else:
                yield current_class
                current_class = [transformation]
            current_class_type = next_class_type
        if len(current_class) > 0:
            yield current_class
