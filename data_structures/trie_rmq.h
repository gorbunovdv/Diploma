//
// Created by Dmitry Gorbunov on 11/02/17.
//

#ifndef DIPLOMA_TRIERMQ_H
#define DIPLOMA_TRIERMQ_H

#include "../data_structures/trie.h"

class TrieRMQ {
public:
  TrieRMQ(std::shared_ptr<Trie> trie) : trie(trie) {
    rmq.resize(4 * len(trie->euler) + 100);
    make_rmq(1, 0, len(trie->euler) - 1);
  }

  int32_t getTotalVectorsSize() const {
    return totalVectorsSize;
  }

  void request(int32_t l, int32_t r, int h, std::vector<std::tuple<int, int32_t>> &result) {
    auto linf = std::numeric_limits<int32_t>::max();
    auto inf = std::numeric_limits<int32_t>::max();
    int32_t ll = std::lower_bound(trie->euler.begin(), trie->euler.end(), std::make_tuple(l, -inf, -linf)) - trie->euler.begin();
    int32_t rr = std::upper_bound(trie->euler.begin(), trie->euler.end(), std::make_tuple(r, inf, linf)) - trie->euler.begin() - 1;
    request(1, 0, len(trie->euler) - 1, ll, rr, h, result);
  }

private:
  void request(int32_t i, int32_t ll, int32_t rr, int32_t l, int32_t r, int h, std::vector<std::tuple<int, int32_t>> &result) {
    if (ll > r || rr < l) {
      return ;
    }
    if (l <= ll && rr <= r) {
      for (int32_t j = 0; j < len(rmq[i]) && std::get<0>(rmq[i][j]) <= h; j++) {
        result.push_back(rmq[i][j]);
      }
      return ;
    }
    request(i * 2, ll, (ll + rr) / 2, l, r, h, result);
    request(i * 2 + 1, (ll + rr) / 2 + 1, rr, l, r, h, result);
  }

  void make_rmq(int32_t i, int32_t l, int32_t r) {
    if (l == r) {
      int height;
      int32_t index;
      std::tie(std::ignore, height, index) = trie->euler[l];
      rmq[i] = { std::make_tuple(height, index) };
    } else {
      make_rmq(i * 2, l, (l + r) / 2);
      make_rmq(i * 2 + 1, (l + r) / 2 + 1, r);
      rmq[i].resize(len(rmq[i * 2]) + len(rmq[i * 2 + 1]));
      std::merge(rmq[i * 2].begin(), rmq[i * 2].end(),
                 rmq[i * 2 + 1].begin(), rmq[i * 2 + 1].end(),
                 rmq[i].begin()
      );
    }
    totalVectorsSize += len(rmq[i]);
  }

  std::shared_ptr<Trie> trie;
  std::vector<std::vector<std::tuple<int, int32_t>>> rmq;
  int32_t totalVectorsSize = 0;
};


#endif //DIPLOMA_TRIERMQ_H
