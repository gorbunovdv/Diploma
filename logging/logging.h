//
// Created by Dmitry Gorbunov on 08/02/17.
//

#ifndef DIPLOMA_LOGGING_H
#define DIPLOMA_LOGGING_H

#include <fstream>
#include <chrono>

std::ofstream ____result("result.txt");
std::ofstream ____result2("result2.txt");

auto start = std::chrono::high_resolution_clock::now();

// Макрос для удобного логирования
#define LOGGER() std::cerr << std::fixed << "[" << \
std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start).count() \
 / 1000.0 << "] -> " \
<< "(" << __FUNCTION__ << "): "
// Макрос для удобного вывода результатов
#define RESULT() ____result
#define RESULT2() ____result2

// Класс для удобного вывода текущего прогресса по операциям
class Ticker {
public:
  Ticker(std::string ticker, int32_t max_ticks) : ticker(ticker), max_ticks(max_ticks) {}

  template<typename Operator>
  void tick(Operator anOperator) {
    current_ticks++;
    if (current_ticks % (max_ticks / 100) == 0 || current_ticks == max_ticks) {
      anOperator(LOGGER() << "[" << ticker << "]: currently processed " << current_ticks << " / " << max_ticks << "; ");
    }
  }

private:
  std::string ticker;
  int32_t max_ticks;
  int32_t current_ticks = 0;
};

#endif //DIPLOMA_LOGGING_H
