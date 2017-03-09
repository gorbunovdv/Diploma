from config.config import config
from python.logger.logger import Logger
from python.transformations_iterator.transformations_iterator import TransformationsReader
from python.word2vec.Word2Vec import Word2Vec

logger = Logger("Main")

model_name, model_path = config["word2vec"]["model"], config["word2vec"]["path"]
logger.info("Using {} as a Word2Vec model".format(model_name))
with open(model_path, "r") as fin:
    word2vec = Word2Vec(fin)
reader = TransformationsReader(config["parameters"]["transformations_filter"]["filtered_path"])
for clazz in reader.foreachClass(word2vec):
    pass #print len(clazz)
