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

class FilterTransformationManager {
public:
  static void filterAllTransformations(const std::shared_ptr<Word2Vec> &word2vec) {
    auto sourcePath = config["parameters"]["transformations_build"]["result_path"].asString();
    auto destPath = config["parameters"]["transformations_filter"]["sorted_each_path"].asString();
    auto files = TransformationsReader::getFiles(sourcePath);
    for (const auto &sourceFile : files) {
      auto destFile = destPath + sourceFile.substr(sourcePath.size());
      sortFile(sourceFile, destFile, word2vec);
    }
    auto destSortedPath = config["parameters"]["transformations_filter"]["sorted_path"].asString();
    sortFiles(files, destSortedPath, word2vec);
  }

private:
  static void sortFiles(auto files, std::string destPath, const std::shared_ptr<Word2Vec> &word2vec) {
    std::vector<FILE*> openedFiles(len(files));
    for (int32_t i = 0; i < len(files); i++) {
      openedFiles[i] = fopen(files[i].data(), "r");
      if (openedFiles[i] == nullptr) {
        throw std::runtime_error("Failed to open file " + files[i]);
      }
    }
    std::vector<std::pair<Transformation, bool>> lastTransformation(len(files), std::make_pair(Transformation(), false));
    std::vector<std::pair<int64_t, int64_t>> hashes(len(files));
    TransformationsWriter writer(destPath);
    LOGGER() << "Sorting files" << std::endl;
    for (;;) {
      int32_t best = -1;
      for (int32_t i = 0; i < len(files); i++) {
        if (!lastTransformation[i].second && !feof(openedFiles[i])) {
          fread(&lastTransformation[i].first, sizeof(Transformation), 1, openedFiles[i]);
          if (!lastTransformation[i].first.validate(word2vec)) {
            throw std::runtime_error("Invalid tranformation");
          }
          hashes[i] = lastTransformation[i].first.hash(word2vec);
          lastTransformation[i].second = true;
        }
        if (lastTransformation[i].second && (best == -1 || hashes[best] > hashes[i])) {
          best = i;
        }
      }
      if (best == -1) {
        break;
      }
      writer.write(lastTransformation[best].first);
      RESULT() << lastTransformation[best].first.getClass(word2vec) << std::endl;
      lastTransformation[best].second = false;
    }
    for (FILE *file : openedFiles) {
      fclose(file);
    }
  }

  static void sortFile(std::string sourceFile, std::string destFile, const std::shared_ptr<Word2Vec> &word2vec) {
    LOGGER() << "Sorting file " << sourceFile << " into " << destFile << std::endl;
    FILE *fin = fopen(sourceFile.data(), "r");
    if (fin == nullptr) {
      throw std::runtime_error("Failed to open file " + sourceFile);
    }
    std::vector<std::pair<std::pair<int64_t, int64_t>, Transformation>> transformations;
    while (!feof(fin)) {
      static Transformation transformation;
      fread(&transformation, sizeof(transformation), 1, fin);
      transformations.push_back(std::make_pair(transformation.hash(word2vec), transformation));
    }
    fclose(fin);
    LOGGER() << "Sorting " << len(transformations) << " transformations" << std::endl;
    std::sort(transformations.begin(), transformations.end(), [] (const auto &a, const auto &b) {
      return a.first < b.first;
    });
    LOGGER() << "Sorted " << len(transformations) << " transformations" << std::endl;
    FILE *fout = fopen(destFile.data(), "w");
    if (fout == nullptr) {
      throw std::runtime_error("Failed to open file " + destFile + " to write");
    }
    for (const auto &transformation : transformations) {
      fwrite(&transformation.second, sizeof(transformation), 1, fout);
    }
    fclose(fout);
  }
};

#endif //DIPLOMA_FILTER_TRANSFORMATION_MANAGER_H
