//
// Created by Dmitry Gorbunov on 08/02/17.
//

#ifndef DIPLOMA_LOGGING_H
#define DIPLOMA_LOGGING_H

#include <fstream>

std::ofstream ____result("result.txt");

#define LOGGER() std::cerr << "[" << 1.0 * clock() / CLOCKS_PER_SEC << "]: "
#define RESULT() ____result

#endif //DIPLOMA_LOGGING_H
