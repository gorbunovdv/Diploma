//
// Created by dgorbunov on 23.02.17.
//

#ifndef DIPLOMA_FILTER_TRANSFORMATION_MANAGER_H
#define DIPLOMA_FILTER_TRANSFORMATION_MANAGER_H

#include <complex>
#include <dirent.h>
#include "../Word2Vec/word2vec.h"
#include "../structures/transformation.h"

class FilterTransformationManager {
public:
  static void filterAllTransformations(const std::shared_ptr<Word2Vec> &word2vec) {
    std::vector<std::string> filesPath = getFilesPaths();
    LOGGER() << "There are " << len(filesPath) << " paths" << std::endl;
    for (auto str : filesPath) {
      LOGGER() << str << std::endl;
    }
    LOGGER() << "Filtering transformations" << std::endl;
    std::set<std::pair<int64_t, int64_t>> to_delete;
    int32_t transformations_to_delete_count = 0;
    int32_t min_transformations_count = config["parameters"]["transformations_filter"]["min_transformations_count"].asInt();
    for (const auto &i : FilterTransformationManager::getTransformationsCount(word2vec, filesPath)) {
      if (i.second < min_transformations_count) {
        to_delete.insert(i.first);
        transformations_to_delete_count += i.second;
      }
    }
    LOGGER() << "Need to delete " << len(to_delete) << " transformation classes" << std::endl;
    LOGGER() << "Deleting" << transformations_to_delete_count << " transformations in total" << std::endl;
    FilterTransformationManager::filterAllTransformationsInternal(word2vec, filesPath, to_delete);
  }

private:
  static void filterAllTransformationsInternal(const std::shared_ptr<Word2Vec> &word2vec, const std::vector<std::string> &filesPath,
      const std::set<std::pair<int64_t, int64_t>> &to_delete)
  {
#pragma omp parallel for num_threads(PROCESSES_COUNT)
    for (int32_t i = 0; i < len(filesPath); i++) {
      FILE *input = fopen(filesPath[i].data(), "r");
      if (input == nullptr) {
        throw std::runtime_error("Could not open file " + filesPath[i]);
      }
      FILE *output = fopen((filesPath[i] + ".filtered").c_str(), "w");
      if (output == nullptr) {
        throw std::runtime_error("Could not open file for write " + filesPath[i] + ".filtered");
      }
      while (!feof(input)) {
        Transformation transformation;
        fread(&transformation, sizeof(transformation), 1, input);
        if (to_delete.count(transformation.hash(word2vec)) == 0) {
          fwrite(&transformation, sizeof(transformation), 1, input);
        }
      }
      fclose(input);
      fclose(output);
    }
  }

  static std::map<std::pair<int64_t, int64_t>, int32_t> getTransformationsCount(const std::shared_ptr<Word2Vec> &word2vec, const std::vector<std::string> &filesPath) {
    std::vector<std::map<std::pair<int64_t, int64_t>, int32_t>> result(len(filesPath));
#pragma omp parallel for num_threads(PROCESSES_COUNT)
    for (int32_t i = 0; i < len(filesPath); i++) {
      FILE *file = fopen(filesPath[i].data(), "r");
      if (file == nullptr) {
        throw std::runtime_error("Could not open file " + filesPath[i]);
      }
      while (!feof(file)) {
        Transformation transformation;
        fread(&transformation, sizeof(transformation), 1, file);
        result[i][transformation.hash(word2vec)]++;
      }
      fclose(file);
    }
    for (int32_t i = 1; i < len(filesPath); i++) {
      if (len(result[i]) > len(result.front())) {
        swap(result[i], result.front());
      }
      for (const auto &pair : result[i]) {
        result.front()[pair.first] += pair.second;
      }
      result[i].clear();
    }
    LOGGER() << "Different classes: " << len(result.front()) << std::endl;
    return result.front();
  }

  static std::vector<std::string> getFilesPaths() {
    std::string path = config["parameters"]["transformations_build"]["result_path"].asString();
    std::vector<std::string> result;
    DIR *dir;
    struct dirent *ent;
    if ((dir = opendir(path.data())) != NULL) {
      while ((ent = readdir (dir)) != NULL) {
        if (*ent->d_name != '.') {
          result.push_back(path + "/" + std::string(ent->d_name));
        }
      }
      closedir (dir);
    } else {
      perror ("");
      throw std::runtime_error("Failed to open directory " + path);
    }
    return result;
  }
};

#endif //DIPLOMA_FILTER_TRANSFORMATION_MANAGER_H
