//
// Created by Dmitry Gorbunov on 08/02/17.
//

#ifndef DIPLOMA_TRANSFORMATION_MANAGER_H
#define DIPLOMA_TRANSFORMATION_MANAGER_H

#include <vector>
#include <iostream>
#include <cassert>
#include <unordered_map>
#include "../types/types.h"
#include "../Word2Vec/word2vec.h"
#include "../logging/logging.h"
#include "../data_structures/trie_rmq.h"
#include "../structures/transformation.h"
#include "../config/config.h"

class TransformationManager {
public:
  static auto getAllTransformations(const std::shared_ptr<Word2Vec> &word2vec) {
    std::unordered_map<utf_string, std::vector<Transformation>> result;
    LOGGER() << "Building SUFFIX tranformations" << std::endl;
    TransformationManager::getAllTransformationsInternal(word2vec, Transformation::SUFFIX, result);
    LOGGER() << "Building PREFIX tranformations" << std::endl;
    TransformationManager::getAllTransformationsInternal(word2vec, Transformation::PREFIX, result);
    LOGGER() << "Validating transformations" << std::endl;
    int32_t totalTransformationsCount = 0;
    for (const auto &transformationClass : result) {
      for (const auto &transformation : transformationClass.second) {
        if (!transformation.validate(word2vec)) {
          LOGGER() << "Failed to validate transformation" << std::endl;
          transformation.print(word2vec);
          throw std::runtime_error("Failed to validate transformation");
        }
      }
    }
    std::vector<utf_string> classesToRemove;
    for (const auto &transformationClass : result) {
      if (len(transformationClass.second) < 10) {
        classesToRemove.push_back(transformationClass.first);
      }
    }
    LOGGER() << len(classesToRemove) << " classes contain less than 10 elements, removing them" << std::endl;
    for (const auto &transformationClass : classesToRemove) {
      result.erase(result.find(transformationClass));
    }
    for (const auto &transformationClass : result) {
      totalTransformationsCount += len(transformationClass.second);
    }
    LOGGER() << "There are " << totalTransformationsCount << " transformations totally" << std::endl;
    LOGGER() << "There are " << len(result) << " different classes of transformations" << std::endl;
    return result;
  }

  static void getAllTransformationsInternal(
    const std::shared_ptr<Word2Vec> &word2vec,
    Transformation::Type type,
    std::unordered_map<utf_string, std::vector<Transformation>> &result)
  {
    int32_t remove_add_symbols_count = config["parameters"]["transformations_build"]["remove_add_symbols_count"].asInt();
    int32_t total_changes_count = config["parameters"]["transformations_build"]["total_changes_count"].asInt();
    auto trie = std::make_shared<Trie>();
    if (type == Transformation::SUFFIX) {
      for (auto entity : word2vec->index2word) {
        trie->addString(entity);
      }
    } else {
      for (auto entity : word2vec->index2word) {
        trie->addString(entity->reverse());
      }
    }
    trie->buildInOut();
    auto trieRMQ = std::make_shared<TrieRMQ>(trie);
    std::vector<Transformation> transformations;
    bool useShortestTransformations = config["parameters"]["transformations_build"]["use_shortest_transformations"].asBool();
#pragma omp for shared(result)
    for (auto node : trie->nodes) {
      std::vector<std::tuple<int, int32_t>> rootTuples;
      for (auto end : node->ends) {
        rootTuples.push_back(std::make_tuple(node->height, end));
      }
      std::vector<std::vector<std::tuple<int, int32_t>>> separatedTuples = { rootTuples };
      for (auto edge : node->go) {
        int32_t in = edge.second->in;
        int32_t out = edge.second->out;
        std::vector<std::tuple<int, int32_t>> tuples;
        trieRMQ->request(in, out, node->height + remove_add_symbols_count, tuples);
        separatedTuples.push_back(tuples);
      }
      for (int32_t i = 0; i < len(separatedTuples); i++) {
        for (const auto &tuple1 : separatedTuples[i]) {
          int height1;
          int32_t index1;
          std::tie(height1, index1) = tuple1;
          for (int32_t j = 0; j < len(separatedTuples); j++) {
            if (useShortestTransformations && i == j) {
              continue;
            }
            for (const auto &tuple2 : separatedTuples[j]) {
              int height2;
              int32_t index2;
              std::tie(height2, index2) = tuple2;
              if (height1 - node->height + height2 - node->height > total_changes_count) {
                continue;
              }
              result[Transformation::hash(word2vec, index1, height1 - node->height, index2, height2 - node->height, type)]
                .emplace_back(index1, height1 - node->height, index2, height2 - node->height, type);
            }
          }
        }
      }
    }
  }
};
#endif //DIPLOMA_TRANSFORMATION_MANAGER_H
