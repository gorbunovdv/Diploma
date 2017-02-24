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
  TransformationsReader(std::string path) {
    files = getFiles(path);
  }

  static std::deque<std::string> getFiles(std::string path) {
    std::deque<std::string> files;
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
    fread(&result, sizeof(Transformation), 1, current_file);
    return true;
  }

private:
  std::deque<std::string> files;
  FILE* current_file = nullptr;
};

class TransformationsWriter {
public:
  TransformationsWriter(std::string path): path(path) {
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
    fwrite(&transformation, sizeof(Transformation), 1, current_file);
  }

  ~TransformationsWriter() {
    if (current_file != nullptr) {
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
      fclose(current_file);
    }
    current_file_number++;
    std::string next_file_path = path + "/" + convert(current_file_number) + ".bin";
    current_file = fopen(next_file_path.data(), "w");
    if (current_file == nullptr) {
      throw std::runtime_error("Failed to open file " + next_file_path + " for write");
    }
  }

  std::string path;
  FILE *current_file = nullptr;
  int32_t current_file_number = 0, current_transformation_number = 0;
  int32_t max_transformations_count_in_file;
};

#endif //DIPLOMA_TRANSFORMATIONS_ITERATOR_H
