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
#include "../data_structures/transformations_iterator.h"

class TransformationManager {
public:
  static void getAllTransformations(const std::shared_ptr<Word2Vec> &word2vec) {
    TransformationsWriter writer(config["parameters"]["transformations_build"]["result_path"].asString(), word2vec);
    LOGGER() << "Building SUFFIX tranformations" << std::endl;
    TransformationManager::getAllTransformationsInternal(word2vec, Transformation::SUFFIX, writer);
    LOGGER() << "Building PREFIX tranformations" << std::endl;
    TransformationManager::getAllTransformationsInternal(word2vec, Transformation::PREFIX, writer);
  }

  static void getAllTransformationsInternal(
    const std::shared_ptr<Word2Vec> &word2vec,
    Transformation::Type type,
    TransformationsWriter &writer)
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
    std::random_shuffle(trie->nodes.begin(), trie->nodes.end());
    auto trieRMQ = std::make_shared<TrieRMQ>(trie);
    std::vector<Transformation> transformations;
    bool useShortestTransformations = config["parameters"]["transformations_build"]["use_shortest_transformations"].asBool();
    int32_t count = 0;
    int32_t files_count = config["parameters"]["transformations_build"]["files_count"].asInt();
    for (auto node : trie->nodes) {
      std::vector<std::tuple<int, int32_t>> rootTuples;
      for (auto end : node->ends) {
        rootTuples.push_back(std::make_tuple(node->height, end));
      }
      std::vector<std::vector<std::tuple<int, int32_t>>> separatedTuples = {rootTuples};
      for (auto edge : node->go) {
        int32_t in = edge.second->in;
        int32_t out = edge.second->out;
        std::vector<std::tuple<int, int32_t>> tuples;
        trieRMQ->request(in, out, node->height + remove_add_symbols_count, tuples);
        separatedTuples.push_back(tuples);
      }
      for (int32_t i = 0; i < len(separatedTuples); i++) {
        for (const auto& tuple1 : separatedTuples[i]) {
          int height1;
          int32_t index1;
          std::tie(height1, index1) = tuple1;
          for (int32_t j = 0; j < len(separatedTuples); j++) {
            if (useShortestTransformations && i == j) {
              continue;
            }
            for (const auto& tuple2 : separatedTuples[j]) {
              int height2;
              int32_t index2;
              std::tie(height2, index2) = tuple2;
              if (height1 - node->height + height2 - node->height > total_changes_count) {
                continue;
              }
              Transformation transformation(
                  index1, height1 - node->height, index2, height2 - node->height, type);
              if (!transformation.validate(word2vec)) {
                throw std::runtime_error("Invalid transformation!");
              }
              writer.write(transformation);
              count++;
            }
          }
        }
      }
    }
    LOGGER() << "Found " << count << " transformations" << std::endl;
  }
};
#endif //DIPLOMA_TRANSFORMATION_MANAGER_H
