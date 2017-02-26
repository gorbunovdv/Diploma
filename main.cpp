#include <iostream>
#include "Word2Vec/word2vec.h"
#include "managers/royal_manager.h"

using namespace std;

void check_modes() {
  LOGGER() << "Using " << PROCESSES_COUNT << " jobs" << std::endl;
#ifdef DEBUG_TRANSFORMATIONS
  LOGGER() << "Validate transformations mode on" << std::endl;
#endif
}

int main(int argc, char **argv) {
  setlocale(LC_ALL, "Russian");
  srand(-1);
  check_modes();
  if (argc != 2) {
    std::cerr << "Usage " << argv[0] << ": <path_to_config>" << std::endl;
    return 1;
  }
  std::ifstream configFile(argv[1]);
  if (!configFile.good()) {
    throw std::runtime_error("Config file " + std::string(argv[1]) + " could not be opened");
  }
  init_config(configFile);
  auto word2vecModelPath = config["word2vec"]["path"].asString();
  LOGGER() << "Using " << config["word2vec"]["model"].asString() << " as Word2Vec model" << std::endl;
  auto model = std::make_unique<BufferedReader>(word2vecModelPath);
  auto word2vec = std::make_shared<Word2Vec>(model);
  RoyalManager royal_manager(word2vec);
  royal_manager.run();
  LOGGER() << "END!" << std::endl;
  return 0;
}
