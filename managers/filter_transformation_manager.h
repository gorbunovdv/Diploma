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

// Менеджер для фильтрации преобразований: сначала сортирует преобразования по хешу от класса,
class FilterTransformationManager {
public:
  // Функция, осуществующая всю фильтрацию
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
  // Функция, осуществующая только фильтрацию отсортированных классов
  static void filterTransformations(const std::shared_ptr<Word2Vec> &word2vec, std::string sourcePath, std::string destPath) {
    LOGGER() << "Filtering transformation classes" << std::endl;
    int32_t minTransformationsInClass = config["parameters"]["transformations_filter"]["min_transformations_in_class"].asInt();
    LOGGER() << "Minimum number of transformations in class: " << minTransformationsInClass << std::endl;
    TransformationsReader reader(sourcePath, word2vec);
    TransformationsWriter writer(destPath, word2vec);
    int32_t transformationClasses = 0, transformations = 0;
    int32_t largestTransformationClass = 0;
    reader.foreachClass(word2vec, [&largestTransformationClass, &minTransformationsInClass, &writer, &transformationClasses, &transformations](const std::vector<Transformation> &transformationClass){
      if (FilterTransformationManager::validTransformationClass(transformationClass, minTransformationsInClass)) {
        writer.write(transformationClass);
        transformationClasses++;
        transformations += len(transformationClass);
        largestTransformationClass = std::max(largestTransformationClass, len(transformationClass));
      }
    });
    LOGGER() << transformationClasses << " transformation classes after filtering" << std::endl;
    LOGGER() << transformations << " transformations after filtering" << std::endl;
    LOGGER() << "Largest class contains: " << largestTransformationClass << std::endl;
  }

  static bool validTransformationClass(const std::vector<Transformation> &transformationClass, int32_t min_transformations_in_class) {
    return len(transformationClass) >= min_transformations_in_class;
  }

  // Функция, осуществляющая вторую часть внешней сортировки: слияние отсортированных преобразований в разных файлах
  static void sortFiles(std::vector<std::string> files, std::string destPath, const std::shared_ptr<Word2Vec> &word2vec) {
    std::vector<std::unique_ptr<BufferedReader>> openedFiles;
    for (int32_t i = 0; i < len(files); i++) {
      openedFiles.push_back(std::make_unique<BufferedReader>(files[i]));
    }
    std::vector<std::pair<Transformation, bool>> lastTransformation(len(files), std::make_pair(Transformation(), false));
    std::vector<std::pair<int64_t, int64_t>> hashes(len(files));
    TransformationsWriter writer(destPath, word2vec);
    LOGGER() << "Sorting files" << std::endl;
    for (;;) {
      int32_t best = -1;
      for (int32_t i = 0; i < len(files); i++) {
        if (!lastTransformation[i].second && !openedFiles[i]->eof()) {
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

  // Функция, осуществляющая сортировку одного файла
  static void sortFile(std::string sourceFile, std::string destFile, const std::shared_ptr<Word2Vec> &word2vec) {
    LOGGER() << "Sorting file " << sourceFile << " into " << destFile << std::endl;
    auto fin = std::make_unique<BufferedReader>(sourceFile);
    std::vector<std::pair<std::pair<int64_t, int64_t>, Transformation>> transformations;
    while (!fin->eof()) {
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
