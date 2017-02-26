//
// Created by Dmitry Gorbunov on 11/02/17.
//

#ifndef DIPLOMA_TRANSFORMATION_H
#define DIPLOMA_TRANSFORMATION_H

#include <algorithm>
#include "../Word2Vec/word2vec.h"

class Transformation {
public:
  enum Type {
    PREFIX,
    SUFFIX,
  };

  Transformation(int32_t from_word, int32_t to_delete, int32_t to_word, int32_t to_add, Type type) : from_word(
    from_word), to_delete(to_delete), to_word(to_word), to_add(to_add), type(type) {}

  Transformation() = default;

  template<typename Word2Vec>
  bool validate(const Word2Vec &word2vec) const {
    if (type != PREFIX && type != SUFFIX) {
      LOGGER() << "Error during validation: not PREFIX, not SUFFIX" << std::endl;
      return false;
    }
    if (from_word < 0 || from_word > len(word2vec->index2word)) {
      LOGGER() << "Error during validation: " << from_word << " is not a valid index of word" << std::endl;
      return false;
    }
    if (to_word < 0 || to_word > len(word2vec->index2word)) {
      LOGGER() << "Error during validation: " << from_word << " is not a valid index of word" << std::endl;
      return false;
    }
    auto from_vocab = word2vec->index2word[from_word]->word;
    auto to_vocab = word2vec->index2word[to_word]->word;
    if (type == PREFIX) {
      std::reverse(from_vocab.begin(), from_vocab.end());
      std::reverse(to_vocab.begin(), to_vocab.end());
    }
    int32_t lcp = 0;
    while (lcp < len(from_vocab) && lcp < len(to_vocab) && from_vocab[lcp] == to_vocab[lcp]) {
      lcp++;
    }
    return len(from_vocab) - lcp <= to_delete && len(to_vocab) - lcp <= to_add;
  }

  template<typename Word2Vec>
  void print(const std::shared_ptr<Word2Vec> &word2vec) const {
    const auto &from_vocab = word2vec->index2word[from_word]->word;
    const auto &to_vocab = word2vec->index2word[to_word]->word;
    if (type == PREFIX) {
      RESULT() << "PREFIX " << from_vocab << " -> " << to_delete << " -> " << from_vocab.substr(to_delete, len(from_vocab) - to_delete)
               << " -> " << to_add << " -> " << to_vocab << std::endl;
    } else {
      RESULT() << "SUFFIX " << from_vocab << " -> " << to_delete << " -> " << from_vocab.substr(0, len(from_vocab) - to_delete)
               << " -> " << to_add << " -> " << to_vocab << std::endl;
    }
  }

  template<typename Word2Vec>
  static utf_string getClass(const std::shared_ptr<Word2Vec>& word2vec,
      int32_t from_word,
      int32_t to_delete,
      int32_t to_word,
      int32_t to_add,
      Transformation::Type type)
  {
    const auto &from_vocab = word2vec->index2word[from_word]->word;
    const auto &to_vocab = word2vec->index2word[to_word]->word;
    if (type == PREFIX) {
      return utf_string("PREFIX:") + from_vocab.substr(0, to_delete) + utf_string(":") + to_vocab.substr(0, to_add);
    } else {
      return utf_string("SUFFIX:") + from_vocab.substr(len(from_vocab) - to_delete, to_delete) + utf_string(":") +
        to_vocab.substr(len(to_vocab) - to_add, to_add);
    }
  }

  template<typename Word2Vec>
  utf_string getClass(const std::shared_ptr<Word2Vec>& word2vec) const {
    return Transformation::getClass(word2vec, from_word, to_delete, to_word, to_add, type);
  }

  template<typename Word2Vec>
  std::pair<int64_t, int64_t> hash(const std::shared_ptr<Word2Vec> &word2vec) const {
    utf_string clazz = getClass(word2vec);
    std::pair<int64_t, int64_t> hashResult(0, 0);
    for (auto c : clazz) {
      hashResult.first = hashResult.first * 3333333 + c + 1;
      hashResult.second = hashResult.second * 5555555 + c + 1;
    }
    return hashResult;
  };

private:
  int32_t from_word, to_delete;
  int32_t to_word, to_add;
  Type type;
};


#endif //DIPLOMA_TRANSFORMATION_H
