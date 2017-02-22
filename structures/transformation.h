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

  bool validate(const std::shared_ptr<Word2Vec> &word2vec) const {
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

  static utf_string hash(const std::shared_ptr<Word2Vec> &word2vec,
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

  utf_string hash(const std::shared_ptr<Word2Vec> &word2vec) const {
    return Transformation::hash(word2vec, from_word, to_delete, to_word, to_add, type);
  }

private:
  int32_t from_word, to_delete;
  int32_t to_word, to_add;
  Type type;
};


#endif //DIPLOMA_TRANSFORMATION_H
