from config.config import config
from python.logger.logger import Logger
from python.managers.nearest_neighbours_manager import NearestNeighboursManager
from python.managers.royal_manager import RoyalManager
from python.transformations_iterator.transformations_iterator import TransformationsReader
from python.word2vec.Word2Vec import Word2Vec

logger = Logger("Main")

model_name, model_path = config["word2vec"]["model"], config["word2vec"]["path"]
logger.info("Using {} as a Word2Vec model".format(model_name))
with open(model_path, "r") as fin:
    word2vec = Word2Vec(fin)

# NearestNeighboursManager.calculate_nearest_neighbours(word2vec)

#reader = TransformationsReader("/home/dgorbunov/Documents/Diploma/results_config_ru_big_3/filtered")
#for clazz in reader.foreachClass(word2vec):
#    for element in clazz:
#        print element.getClass(word2vec), " : ", word2vec.index2word[element.from_word].word, word2vec.index2word[element.to_word].word

royal_manager = RoyalManager(word2vec)
royal_manager.run()
