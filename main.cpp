#include <iostream>
#include "Word2Vec/word2vec.h"
#include "managers/royal_manager.h"

using namespace std;

int main(int argc, char **argv) {
  setlocale(LC_ALL, "Russian");
  srand(-1);
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
  FilePointer model = fopen(word2vecModelPath.data(), "r");
  if (model == nullptr) {
    throw std::runtime_error("Word2Vec model " + word2vecModelPath + " could not be opened");
  }
  auto word2vec = std::make_shared<Word2Vec>(model);
  RoyalManager royal_manager(word2vec);
  royal_manager.run();
  fclose(model);
  LOGGER() << "END!";
  return 0;
}
