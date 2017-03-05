//
// Created by Dmitry Gorbunov on 10/02/17.
//

#ifndef DIPLOMA_UTF_STRING_H
#define DIPLOMA_UTF_STRING_H

#include "../utf8/utf8.h"
#include <set>
#include <vector>
#include <ostream>
#include <string>
#include <algorithm>

class utf_string {
public:
  utf_string(const std::string &string = "") {
    utf8::utf8to32(string.begin(), string.end(), std::back_inserter(utf32line));
  }

  auto begin() {
    return utf32line.begin();
  }

  auto end() {
    return utf32line.end();
  }

  auto cbegin() const {
    return utf32line.cbegin();
  }

  auto cend() const {
    return utf32line.cend();
  }

  std::string to_string() const {
    std::string string;
    utf8::utf32to8(utf32line.begin(), utf32line.end(), back_inserter(string));
    return string;
  }

  friend std::ostream& operator << (std::ostream &stream, const utf_string &utf_string) {
    return stream << utf_string.to_string();
  }

  friend std::ofstream& operator << (std::ofstream &stream, const utf_string &utf_string) {
    return stream << utf_string.to_string();
  }

  friend bool operator < (const utf_string &a, const utf_string &b) {
    return a.utf32line < b.utf32line;
  }

  friend bool operator == (const utf_string &a, const utf_string &b) {
    return a.utf32line == b.utf32line;
  }

  friend utf_string operator + (const utf_string &a, const utf_string &b) {
    auto vector1 = a.utf32line;
    const auto &vector2 = b.utf32line;
    vector1.insert(vector1.end(), vector2.begin(), vector2.end());
    return utf_string(vector1);
  }

  int32_t& operator[] (size_t index) {
    return utf32line[index];
  }

  int32_t size() const {
    return len(utf32line);
  }

  utf_string substr(int32_t begin, int32_t N) const {
    N = std::min(N, size() - begin);
    return utf_string(std::vector<int32_t>(utf32line.begin() + begin, utf32line.begin() + begin + N));
  }

  size_t getHash() const {
    size_t hash = 0;
    for (auto c : utf32line) {
      hash = hash * 3333333 + c + 1;
    }
    return hash;
  }

  auto set() {
    return std::set<int32_t>(utf32line.begin(), utf32line.end());
  }

private:
  utf_string(const std::vector<int32_t> utf32line) : utf32line(utf32line) {}
  std::vector<int32_t> utf32line;
};

namespace std {
template <> struct hash<utf_string>
{
  size_t operator()(const utf_string &x) const {
    return x.getHash();
  }
};
}


#endif //DIPLOMA_UTF_STRING_H
