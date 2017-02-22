//
// Created by Dmitry Gorbunov on 11/02/17.
//

#ifndef DIPLOMA_ITERABLE_H
#define DIPLOMA_ITERABLE_H

template<typename Collection>
class Iterable {
  Iterable(const Collection &collection) : collection(collection) { }

  class Iterator {

  };

private:
  const Collection &collection;
};

#endif //DIPLOMA_ITERABLE_H
