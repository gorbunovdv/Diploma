//
// Created by Dmitry Gorbunov on 08/02/17.
//

#ifndef DIPLOMA_WORD2VEC_H
#define DIPLOMA_WORD2VEC_H

#include <iostream>
#include <string>
#include <vector>
#include <map>
#include "../config/config.h"
#include "../types/types.h"
#include "../logging/logging.h"
#include "../utf/utf_string.h"
#include "../structures/vocab.h"

struct Word2Vec {
  Word2Vec(FILE *file) {
    LOGGER() << "Loading word2vec model" << std::endl;
    int64_t wordsCount_, dimensionsCount_;
    fscanf(file, "%lld", &wordsCount_);
    fscanf(file, "%lld", &dimensionsCount_);
    std::tie(wordsCount, dimensionsCount) = std::tie(wordsCount_, dimensionsCount_);
    std::set<int32_t> letters_list = utf_string(config["word2vec"]["valid_letters"].asString()).set();
    for (int32_t i = 0; i < wordsCount; i++) {
      bool addWord = true;
      auto cur = std::make_shared<Vocab>();
      cur->index = i;
      try {
        cur->word = read_word(file);
        if (!check_if_word_is_valid(cur->word, letters_list)) {
          addWord = false;
        }
      } catch (std::exception e) {
        LOGGER() << "UTF8 decoding failed: skipping word" << std::endl;
        addWord = false;
      }
      cur->syn0 = std::make_shared<std::vector<float>>(static_cast<size_t>(dimensionsCount));
      fread(&cur->syn0->front(), sizeof(float), static_cast<size_t>(dimensionsCount), file);
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

  int32_t getWordsCount() const {
    return wordsCount;
  }

  int32_t getDimensionsCount() const {
    return dimensionsCount;
  }

  int32_t wordsCount;
  int32_t dimensionsCount;
  std::vector<std::shared_ptr<Vocab>> index2word;
  std::map<utf_string, std::shared_ptr<Vocab>> vocab;

private:
  static utf_string read_word(FILE *file) {
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
