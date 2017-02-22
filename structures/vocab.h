//
// Created by Dmitry Gorbunov on 11/02/17.
//

#ifndef DIPLOMA_VOCAB_H
#define DIPLOMA_VOCAB_H

#include <algorithm>
#include "../utf/utf_string.h"

struct Vocab {
  int32_t index;
  utf_string word;
  std::shared_ptr<std::vector<float>> syn0;

  std::shared_ptr<Vocab> reverse() {
    auto reversed = std::make_shared<Vocab>();
    reversed->index = index;
    reversed->word = word;
    std::reverse(reversed->word.begin(), reversed->word.end());
    reversed->syn0 = syn0;
    return reversed;
  }
};


#endif //DIPLOMA_VOCAB_H
