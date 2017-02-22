//
// Created by Dmitry Gorbunov on 08/02/17.
//

#ifndef DIPLOMA_ROYAL_MANAGER_H
#define DIPLOMA_ROYAL_MANAGER_H

#include <iostream>
#include "../Word2Vec/word2vec.h"
#include "transformation_manager.h"

class RoyalManager {
public:
  RoyalManager(std::shared_ptr<Word2Vec> word2vec) : word2vec(word2vec) { }

  void run() {
    auto transformationMap = TransformationManager::getAllTransformations(word2vec);
    for (const auto &vector : transformationMap) {
      RESULT() << vector.first << ":" << len(vector.second) << std::endl;
      for (const auto &transformation : vector.second) {
        transformation.print(word2vec);
      }
    }
  }

private:
  std::shared_ptr<Word2Vec> word2vec;
};

#endif //DIPLOMA_ROYAL_MANAGER_H
