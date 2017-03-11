from config.config import config
from python.logger.logger import Logger
from python.managers.royal_manager import RoyalManager
from python.word2vec.Word2Vec import Word2Vec

logger = Logger("Main")

model_name, model_path = config["word2vec"]["model"], config["word2vec"]["path"]
logger.info("Using {} as a Word2Vec model".format(model_name))
with open(model_path, "r") as fin:
    word2vec = Word2Vec(fin)

royal_manager = RoyalManager(word2vec)
royal_manager.run()
