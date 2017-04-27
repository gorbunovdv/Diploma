//
// Created by Dmitry Gorbunov on 08/02/17.
//

#ifndef DIPLOMA_WORD2VEC_H
#define DIPLOMA_WORD2VEC_H

#include <iostream>
#include <string>
#include <cstring>
#include <vector>
#include <map>
#include "../config/config.h"
#include "../types/types.h"
#include "../logging/logging.h"
#include "../utf/utf_string.h"
#include "../structures/vocab.h"
#include "../structures/transformation.h"
#include "../utils.h"
// Реализация хранения модели Word2Vec в C++
struct Word2Vec {
  // Загрузка Word2Vec из файла: считывает модель, удаляя слова, в которых встречаются другие символы, кроме как из языка
  Word2Vec(const std::unique_ptr<BufferedReader> &file) {
    LOGGER() << "Loading word2vec model" << std::endl;
    int64_t wordsCount_, dimensionsCount_;
    fscanf(file->asFilePointer(), "%lld", &wordsCount_);
    fscanf(file->asFilePointer(), "%lld", &dimensionsCount_);
    std::tie(wordsCount, dimensionsCount) = std::tie(wordsCount_, dimensionsCount_);
    std::set<int32_t> letters_list = utf_string(config["word2vec"]["valid_letters"].asString()).set();
    for (int32_t i = 0; i < wordsCount; i++) {
      bool addWord = true;
      auto cur = std::make_shared<Vocab>();
      cur->index = i;
      try {
        cur->word = read_word(file->asFilePointer());
        if (!check_if_word_is_valid(cur->word, letters_list)) {
          addWord = false;
        }
      } catch (std::exception e) {
        LOGGER() << "UTF8 decoding failed: skipping word" << std::endl;
        addWord = false;
      }
      cur->syn0 = std::make_shared<std::vector<float>>(static_cast<size_t>(dimensionsCount));
      fread(&cur->syn0->front(), sizeof(float), static_cast<size_t>(dimensionsCount), file->asFilePointer());
      if (addWord) {
        index2word.push_back(cur);
      } else {
        i--;
        wordsCount--;
      }
    }
    for (auto entity : index2word) {
      vocab[entity->word] = entity;
    }
    LOGGER() << "Successfully loaded word2vec model" << std::endl;
    LOGGER() << "There are " << len(index2word) << " words in model" << std::endl;
    LOGGER() << "Last one is \"" << index2word.back()->word << "\"" << std::endl;
  }

  // Возвращает количество слов в модели Word2Vec
  int32_t getWordsCount() const {
    return wordsCount;
  }

  // Возвращает размерность векторного пространства Word2Vec
  int32_t getDimensionsCount() const {
    return dimensionsCount;
  }

  // Считывает преобразование из файла file в result, а также опционально валидирует преобразование
  bool read(const std::unique_ptr<BufferedReader> &file, Transformation &result) {
    memset(&result, -1, sizeof(Transformation));
    int32_t read = file->read(&result, sizeof(Transformation), 1);
    if (read != 1 && file->eof()) {
      return false;
    }
    if (read != 1) {
      LOGGER() << "EOF: " << file->eof() << std::endl;
      LOGGER() << "Read " << read << std::endl;
      perror("");
      throw std::runtime_error("IO exception");
    }
#ifdef DEBUG_TRANSFORMATIONS
    if (!result.validate(this)) {
      throw std::runtime_error("Validation failed");
    }
#endif
    return true;
  }

  // Записывает преобразование transformation в файл file, а также опционально валидирует преобразование
  void write(FilePointer &file, Transformation transformation) {
#ifdef DEBUG_TRANSFORMATIONS
    if (!transformation.validate(this)) {
      throw std::runtime_error("Validation failed");
    }
#endif
    int32_t written = fwrite(&transformation, sizeof(Transformation), 1, file);
    if (written != 1) {
      LOGGER() << "Written " << written << std::endl;
      perror("");
      throw std::runtime_error("IO exception");
    }
  }

  int32_t wordsCount;
  int32_t dimensionsCount;
  std::vector<std::shared_ptr<Vocab>> index2word;
  std::map<utf_string, std::shared_ptr<Vocab>> vocab;

private:
  // Считывает слово из модели Word2Vec
  static utf_string read_word(FilePointer &file) {
    std::string result;
    while (1) {
      int c = fgetc(file);
      if (feof(file) || c == ' ') {
        break;
      }
      if (c != '\n') {
        result += c;
      }
    }
    return utf_string(result);
  }

  // Проверяет, что в слове не содержатся символы, которые не встречаются в letters_list
  static bool check_if_word_is_valid(utf_string &word, const std::set<int32_t> &letters_list) {
    for (auto c : word) {
      if (letters_list.count(c) == 0) {
        return false;
      }
    }
    return true;
  }
};

#endif //DIPLOMA_WORD2VEC_H
