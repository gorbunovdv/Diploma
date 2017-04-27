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
#include "../utils.h"

// Класс для удобного считывания преобразований из файла
class TransformationsReader {
public:
  TransformationsReader(std::string path, const std::shared_ptr<Word2Vec> &word2vec) : word2vec(word2vec) {
    auto vector = getFiles(path);
    files = std::deque<std::string>(vector.begin(), vector.end());
  }

  // Находит список всех файлов в указанной директории
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

  // Считывает следующее преобразование в списке
  bool next(Transformation &result) {
    while (!current_file->isDefined() || current_file->eof()) {
      if (current_file->isDefined() && current_file->eof()) {
        current_file = std::make_unique<BufferedReader>();
      }
      if (files.empty()) {
        return false;
      }
      std::string next_file = files.front();
      files.pop_front();
      current_file = std::make_unique<BufferedReader>(next_file);
    }
    if (word2vec->read(current_file, result)) {
      return true;
    }
    if (current_file->eof() && !files.empty()) {
      return next(result);
    }
    return false;
  }

  // Применяет оператор ко всем преобразованиям в файлах
  template<typename Operator>
  void foreach(Operator anOperator) {
    Transformation currentTransformation;
    while (next(currentTransformation)) {
      anOperator(currentTransformation);
    }
  }

  // Применяет оператор ко всем преобразованиям в классе (они должны быть отсортированы)
  template<typename Operator>
  void foreachClass(const std::shared_ptr<Word2Vec> &word2vec, Operator anOperator) {
    std::pair<int64_t, int64_t> currentHash;
    std::vector<Transformation> current;
    Transformation currentTransformation;
    int32_t iteration = 0;
    while (next(currentTransformation)) {
      const std::pair<int64_t, int64_t> currentTransformationHash = currentTransformation.hash(word2vec);
      if (len(current) == 0 || currentHash == currentTransformationHash) {
        current.push_back(currentTransformation);
        currentHash = currentTransformationHash;
      } else {
        if ((++iteration & ((1 << 20) - 1)) == 0) {
          LOGGER() << "Read " << iteration << " classes" << std::endl;
        }
        anOperator(current);
        current = { currentTransformation };
        currentHash = currentTransformationHash;
      }
    }
    if (len(current) > 0) {
      anOperator(current);
    }
  }

private:
  std::deque<std::string> files;
  std::unique_ptr<BufferedReader> current_file = std::make_unique<BufferedReader>();
  const std::shared_ptr<Word2Vec> word2vec;
};

// Класс для удобной записи преобразований в директорию
class TransformationsWriter {
public:
  TransformationsWriter(std::string path, const std::shared_ptr<Word2Vec> &word2vec): path(path), word2vec(word2vec) {
    if (path == "") {
      throw std::runtime_error("Path is empty");
    }
    system(("rm -Rvf " + path + "/*").data());
    max_transformations_count_in_file = config["transformations_iterator"]["max_transformations_count_in_file"].asInt();
  }

  // Записать преобразование transformation в файл
  void write(const Transformation &transformation) {
    ++current_transformation_number;
    if (current_file == nullptr || current_transformation_number > max_transformations_count_in_file) {
      createNextFile();
    }
    word2vec->write(current_file, transformation);
  }

  // Записать все преобразования в полуинтервале итераторов
  template<typename Iterator>
  void write(Iterator begin, const Iterator &end) {
    while (begin != end) {
      write(*begin);
      begin++;
    }
  }

  // Записать все преобразования в контейнере
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
    current_file_path = path + "/" + convert(current_file_number) + ".bin";
    current_file = fopen(current_file_path.data(), "w");
    if (current_file == nullptr) {
      throw std::runtime_error("Could not open file " + current_file_path + " for write");
    }
  }

  std::string path;
  FilePointer current_file = nullptr;
  int32_t current_file_number = 0, current_transformation_number = 0;
  int32_t max_transformations_count_in_file;
  const std::shared_ptr<Word2Vec> word2vec;
  std::string current_file_path;
};

#endif //DIPLOMA_TRANSFORMATIONS_ITERATOR_H
