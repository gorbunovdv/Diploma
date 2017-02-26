//
// Created by dgorbunov on 23.02.17.
//

#ifndef DIPLOMA_FILTER_TRANSFORMATION_MANAGER_H
#define DIPLOMA_FILTER_TRANSFORMATION_MANAGER_H

#include <complex>
#include <dirent.h>
#include <fcntl.h>
#include "../Word2Vec/word2vec.h"
#include "../structures/transformation.h"
#include "../data_structures/transformations_iterator.h"

class FilterTransformationManager {
public:
  static void filterAllTransformations(const std::shared_ptr<Word2Vec> &word2vec) {
    auto sourcePath = config["parameters"]["transformations_build"]["result_path"].asString();
    auto destPath = config["parameters"]["transformations_filter"]["sorted_each_path"].asString();
    auto files = TransformationsReader::getFiles(sourcePath);
    for (auto &sourceFile : files) {
      auto destFile = destPath + sourceFile.substr(sourcePath.size());
      sortFile(sourceFile, destFile, word2vec);
      sourceFile = destFile;
    }
    auto destSortedPath = config["parameters"]["transformations_filter"]["sorted_path"].asString();
    sortFiles(files, destSortedPath, word2vec);
    auto destFilteredPath = config["parameters"]["transformations_filter"]["filtered_path"].asString();
    filterTransformations(word2vec, destSortedPath, destFilteredPath);
  }

private:
  static void filterTransformations(const std::shared_ptr<Word2Vec> &word2vec, std::string sourcePath, std::string destPath) {
    LOGGER() << "Filtering transformation classes" << std::endl;
    int32_t min_transformations_in_class = config["parameters"]["transformations_filter"]["min_transformations_in_class"].asInt();
    LOGGER() << "Minimum number of transformations in class: " << min_transformations_in_class << std::endl;
    TransformationsReader reader(sourcePath, word2vec);
    TransformationsWriter writer(destPath, word2vec);
    int32_t transformationClasses = 0, transformations = 0;
    reader.foreachClass(word2vec, [&min_transformations_in_class, &writer, &transformationClasses, &transformations](const std::vector<Transformation> &transformationClass){
      if (FilterTransformationManager::validTransformationClass(transformationClass, min_transformations_in_class)) {
        writer.write(transformationClass);
        transformationClasses++;
        transformations += len(transformationClass);
      }
    });
    LOGGER() << transformationClasses << " transformation classes after filtering" << std::endl;
    LOGGER() << transformations << " transformations after filtering" << std::endl;
  }

  static bool validTransformationClass(const std::vector<Transformation> &transformationClass, int32_t min_transformations_in_class) {
    return len(transformationClass) >= min_transformations_in_class;
  }

  static void sortFiles(std::vector<std::string> files, std::string destPath, const std::shared_ptr<Word2Vec> &word2vec) {
    std::vector<BufferedReader> openedFiles(len(files));
    for (int32_t i = 0; i < len(files); i++) {
      openedFiles[i] = BufferedReader(files[i]);
    }
    std::vector<std::pair<Transformation, bool>> lastTransformation(len(files), std::make_pair(Transformation(), false));
    std::vector<std::pair<int64_t, int64_t>> hashes(len(files));
    TransformationsWriter writer(destPath, word2vec);
    LOGGER() << "Sorting files" << std::endl;
    for (;;) {
      int32_t best = -1;
      for (int32_t i = 0; i < len(files); i++) {
        if (!lastTransformation[i].second && !openedFiles[i].eof()) {
          if (!word2vec->read(openedFiles[i], lastTransformation[i].first)) {
            continue;
          }
          lastTransformation[i].second = true;
          hashes[i] = lastTransformation[i].first.hash(word2vec);
        }
        if (lastTransformation[i].second && (best == -1 || hashes[best] > hashes[i])) {
          best = i;
        }
      }
      if (best == -1) {
        break;
      }
      writer.write(lastTransformation[best].first);
      lastTransformation[best].second = false;
    }
  }

  static void sortFile(std::string sourceFile, std::string destFile, const std::shared_ptr<Word2Vec> &word2vec) {
    LOGGER() << "Sorting file " << sourceFile << " into " << destFile << std::endl;
    BufferedReader fin(sourceFile);
    std::vector<std::pair<std::pair<int64_t, int64_t>, Transformation>> transformations;
    while (!fin.eof()) {
      Transformation transformation;
      if (!word2vec->read(fin, transformation)) {
        continue;
      }
      transformations.push_back(std::make_pair(transformation.hash(word2vec), transformation));
    }
    LOGGER() << "Sorting " << len(transformations) << " transformations" << std::endl;
    std::sort(transformations.begin(), transformations.end(), [] (const auto &a, const auto &b) {
      return a.first < b.first;
    });
    LOGGER() << "Sorted " << len(transformations) << " transformations" << std::endl;
    FilePointer fout = fopen(destFile.data(), "w");
    if (fout == nullptr) {
      throw std::runtime_error("Failed to open file " + destFile + " to write");
    }
    for (const auto &transformation : transformations) {
      word2vec->write(fout, transformation.second);
    }
    fclose(fout);
  }
};

#endif //DIPLOMA_FILTER_TRANSFORMATION_MANAGER_H
