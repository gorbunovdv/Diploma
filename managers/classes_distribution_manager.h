//
// Created by dgorbunov on 05.03.17.
//

#ifndef DIPLOMA_CLASSES_DISTRIBUTION_MANAGER_H
#define DIPLOMA_CLASSES_DISTRIBUTION_MANAGER_H

#include <vector>
#include <cstdint>
#include <unordered_map>
#include "../data_structures/transformations_iterator.h"

// Менеджер, отвечающий за подсчет статистики по классам преобразований, в зависимости от размера класса
class ClassesDistributionManager {
public:
  ClassesDistributionManager(std::string path, const std::shared_ptr<Word2Vec> &word2vec) {
    TransformationsReader reader(path, word2vec);
    reader.foreachClass(word2vec, [this, &word2vec](const std::vector<Transformation> &transformations){
      RESULT() << transformations.back().getClass(word2vec) << " : " << len(transformations) << std::endl;
      this->classesDistribution[len(transformations)]++;
    });
    for (auto i : classesDistribution) {
      RESULT2() << i.first << " : " << i.second << std::endl;
    }
    RESULT2() << "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n";
    int32_t cur = 0;
    for (auto i : classesDistribution) {
      cur += i.second;
      RESULT2() << i.first << " : " << cur << std::endl;
    }
  }

private:
  std::map<int32_t, int32_t> classesDistribution;
};

#endif //DIPLOMA_CLASSES_DISTRIBUTION_MANAGER_H
