//
// Created by Dmitry Gorbunov on 11/02/17.
//

#ifndef DIPLOMA_CONFIG_H
#define DIPLOMA_CONFIG_H

#include <string>
#include <vector>
#include <map>
#include <json/json.h>

Json::Value config;

void init_config(std::istream &stream) {
  Json::Reader reader;
  if (!reader.parse(stream, config)) {
    throw std::runtime_error(reader.getFormattedErrorMessages());
  }
}

#endif //DIPLOMA_CONFIG_H
