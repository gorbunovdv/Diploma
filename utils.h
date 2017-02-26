//
// Created by Dmitry Gorbunov on 26/02/17.
//

#ifndef DIPLOMA_UTILS_H
#define DIPLOMA_UTILS_H

#include <string>
#include "types/types.h"

class BufferedReader {
public:
  BufferedReader(std::string file) {
    this->file = fopen(file.data(), "r");
    if (this->file == nullptr) {
      throw std::runtime_error("Could not open file " + file);
    }
    buffer = new char[buffer_size];
    defined = true;
    LOGGER() << "Opened file " << file << std::endl;
  }

  BufferedReader() = default;

  ~BufferedReader() {
    if (!defined) {
      return ;
    }
    delete[] buffer;
    fclose(file);
    LOGGER() << "Closed file " << file << std::endl;
  }

  bool grow_capacity() {
    position = real_size = 0;
    real_size = fread(buffer, sizeof(char), buffer_size, file);
    return real_size > 0;
  }

  FilePointer& asFilePointer() {
    return file;
  }

  bool read(void *pointer_, int32_t structure_size, int32_t structure_count) {
    char* pointer = static_cast<char*>(pointer_);
    int32_t total_size = structure_count * structure_size;
    while (total_size > 0) {
      if (position == real_size && !grow_capacity()) {
        return false;
      }
      int32_t to_copy = std::min(real_size - position, total_size);
      memcpy(pointer, buffer + position, to_copy);
      position += to_copy;
      total_size -= to_copy;
      pointer += to_copy;
    }
    return true;
  }

  bool isDefined() {
    return defined;
  }

  bool eof() {
    return position == real_size && feof(file);
  }

private:
  FilePointer file = nullptr;
  char *buffer;
  int32_t position = 0, real_size = 0;
  bool defined = false;
  static constexpr int32_t buffer_size = 4194304;
};

#endif //DIPLOMA_UTILS_H
