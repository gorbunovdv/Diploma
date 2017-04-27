//
// Created by Dmitry Gorbunov on 11/02/17.
//

#ifndef DIPLOMA_TRIE_H
#define DIPLOMA_TRIE_H

#include <cstdint>
#include <vector>
#include <map>
#include <memory>
#include <algorithm>
#include "../Word2Vec/word2vec.h"
#include "../structures/vocab.h"

// Класс для хранения префиксного дерева
class Trie {
public:
  Trie() = default;

  // Структура одной вершины  префиксного дерева
  struct TrieNode {
    std::vector<int32_t> ends;
    std::map<int32_t, std::shared_ptr<TrieNode>> go;
    int32_t in, out;
    int height;
  };

  // Добавление строки в префиксное дерево
  void addString(std::shared_ptr<Vocab> entity) {
    auto currentNode = root;
    for (auto currentSymbol : entity->word) {
      if (currentNode->go.find(currentSymbol) == currentNode->go.end()) {
        auto newNode = std::make_shared<TrieNode>();
        nodes.push_back(newNode);
        currentNode->go[currentSymbol] = newNode;
        verticesCount++;
      }
      currentNode = currentNode->go[currentSymbol];
    }
    currentNode->ends.push_back(entity->index);
  }

  // Насчитать эйлеров обход префиксного дерева
  void buildInOut() {
    buildInOut(root);
    std::sort(euler.begin(), euler.end());
  }

  // Возвращает количество вершин
  int32_t vecticesCount() const {
    return verticesCount;
  }

  std::vector<std::tuple<int32_t, int, int32_t>> euler; // euler in, height, index
  std::vector<std::shared_ptr<TrieNode>> nodes;

private:
  // Обход в глубину, насчитывающий времена входа, времена выхода вершин, а также эйлеров обход
  void buildInOut(std::shared_ptr<TrieNode> vertex, int height = 0) {
    vertex->in = timer++;
    vertex->height = height;
    for (auto index : vertex->ends) {
      euler.emplace_back(vertex->in, height, index);
    }
    for (auto edge : vertex->go) {
      buildInOut(edge.second, height + 1);
    }
    vertex->out = timer++;
  }

  std::shared_ptr<TrieNode> root = std::make_shared<TrieNode>();
  int32_t verticesCount = 1;
  int32_t timer = 0;
};

#endif //DIPLOMA_TRIE_H
