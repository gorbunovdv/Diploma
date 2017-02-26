//
// Created by dgorbunov on 24.02.17.
//

#ifndef DIPLOMA_TRANSFORMATIONS_ITERATOR_H
#define DIPLOMA_TRANSFORMATIONS_ITERATOR_H

#include <string>
#include <dirent.h>
#include <stdexcept>
#include <vector>
#include <algorithm>
#include <deque>
#include "../structures/transformation.h"

class TransformationsReader {
public:
  TransformationsReader(std::string path, const std::shared_ptr<Word2Vec> &word2vec) : word2vec(word2vec) {
    auto vector = getFiles(path);
    files = std::deque<std::string>(vector.begin(), vector.end());
  }

  static std::vector<std::string> getFiles(std::string path) {
    std::vector<std::string> files;
    DIR *dir;
    struct dirent *ent;
    if ((dir = opendir(path.data())) != NULL) {
      while ((ent = readdir (dir)) != NULL) {
        if (*ent->d_name != '.') {
          files.push_back(path + "/" + std::string(ent->d_name));
        }
      }
      closedir (dir);
    } else {
      perror ("");
      throw std::runtime_error("Failed to open directory " + path);
    }
    std::sort(files.begin(), files.end());
    return files;
  }

  bool next(Transformation &result) {
    while (current_file == nullptr || feof(current_file)) {
      if (current_file != nullptr && feof(current_file)) {
        current_file = nullptr;
        fclose(current_file);
      }
      if (files.empty()) {
        return false;
      }
      std::string next_file = files.front();
      files.pop_front();
      current_file = fopen(next_file.data(), "r");
      if (current_file == nullptr) {
        throw std::runtime_error("Failed to open file " + next_file);
      }
    }
    return word2vec->read(current_file, result);
  }

  template<typename Operator>
  void foreach(Operator anOperator) {
    Transformation currentTransformation;
    while (next(currentTransformation)) {
      anOperator(currentTransformation);
    }
  }

private:
  std::deque<std::string> files;
  FilePointer current_file = nullptr;
  const std::shared_ptr<Word2Vec> word2vec;
};

class TransformationsWriter {
public:
  TransformationsWriter(std::string path, const std::shared_ptr<Word2Vec> &word2vec): path(path), word2vec(word2vec) {
    if (path == "") {
      throw std::runtime_error("Path is empty");
    }
    system(("rm -Rvf " + path + "/*").data());
    max_transformations_count_in_file = config["transformations_iterator"]["max_transformations_count_in_file"].asInt();
  }

  void write(const Transformation &transformation) {
    ++current_transformation_number;
    if (current_file == nullptr || current_transformation_number > max_transformations_count_in_file) {
      createNextFile();
    }
    word2vec->write(current_file, transformation);
  }

  template<typename Iterator>
  void write(Iterator begin, const Iterator &end) {
    while (begin != end) {
      write(*begin);
      begin++;
    }
  }

  template<typename Container>
  void write(const Container &container) {
    for (auto i : container) {
      write(i);
    }
  }

  ~TransformationsWriter() {
    if (current_file != nullptr) {
      LOGGER() << "Closed " << current_file_path << std::endl;
      fclose(current_file);
    }
  }

private:
  std::string convert(int num) {
    std::string result;
    for (int i = 0; i < 10; i++) {
      result += static_cast<char>('0' + num % 10);
      num /= 10;
    }
    std::reverse(result.begin(), result.end());
    return result;
  }

  void createNextFile() {
    current_transformation_number = 1;
    if (current_file != nullptr) {
      LOGGER() << "Closed " << current_file_path << std::endl;
      fclose(current_file);
    }
    current_file_number++;
    std::string next_file_path = path + "/" + convert(current_file_number) + ".bin";
    current_file = fopen(next_file_path.data(), "w");
    if (current_file == nullptr) {
      throw std::runtime_error("Failed to open file " + next_file_path + " for write");
    }
    current_file_path = next_file_path;
  }

  std::string path;
  FilePointer current_file = nullptr;
  int32_t current_file_number = 0, current_transformation_number = 0;
  int32_t max_transformations_count_in_file;
  const std::shared_ptr<Word2Vec> word2vec;
  std::string current_file_path;
};

#endif //DIPLOMA_TRANSFORMATIONS_ITERATOR_H
