//
// Created by Dmitry Gorbunov on 08/02/17.
//

#ifndef DIPLOMA_ROYAL_MANAGER_H
#define DIPLOMA_ROYAL_MANAGER_H

#include <iostream>
#include "../Word2Vec/word2vec.h"
#include "transformation_manager.h"
#include "filter_transformation_manager.h"
#include "classes_distribution_manager.h"
#include "nearest_points_calculator.h"

class RoyalManager {
public:
  RoyalManager(std::shared_ptr<Word2Vec> word2vec) : word2vec(word2vec) { }

  void run() {
    /*TransformationManager::getAllTransformations(word2vec);
    FilterTransformationManager::filterAllTransformations(word2vec);*/
    ClassesDistributionManager(config["parameters"]["transformations_filter"]["filtered_path"].asString(), word2vec);
    NearestPointsCalculator::testArmadillo();
  }

private:
  std::shared_ptr<Word2Vec> word2vec;
};

#endif //DIPLOMA_ROYAL_MANAGER_H
