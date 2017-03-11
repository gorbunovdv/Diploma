import numpy


class resizeable_list:
    def __init__(self, type):
        self.type = type
        self.current_size = 0
        self.total_size = 1
        self.array = numpy.ndarray(1, type)

    def append(self, object):
        if self.current_size + 1 > self.total_size:
            self.resize_array(self.total_size * 2)
        self.array[self.current_size] = object
        self.current_size += 1

    def extend(self, objects):
        new_size = self.total_size
        while self.current_size + len(objects) > new_size:
            new_size *= 2
        if new_size != self.total_size:
            self.resize_array(new_size)
        for object in objects:
            self.append(object)

    def resize_array(self, new_size):
        new_array = numpy.ndarray(new_size, self.type)
        new_array[:self.total_size] = self.array
        self.array = new_array
        self.total_size = new_size

    def __iter__(self):
        for index in range(self.current_size):
            yield self.array[index]

    def __getitem__(self, item):
        return self.array[item]

    def __len__(self):
        return self.current_size


class resizeable_tuple_three:
    def __init__(self):
        self.array1 = resizeable_list(numpy.float32)
        self.array2 = resizeable_list(numpy.int32)
        self.array3 = resizeable_list(numpy.int32)
        self.size = 0

    def append(self, object):
        self.array1.append(object[0])
        self.array2.append(object[1])
        self.array3.append(object[2])
        self.size += 1

    def extend(self, objects):
        for object in objects:
            self.append(object)

    def __iter__(self):
        for index in range(self.size):
            yield (self.array1[index], self.array2[index], self.array3[index])

    def __getitem__(self, item):
        return self.array1[item], self.array2[item], self.array3[item]

    def __len__(self):
        return self.array1.current_size


class resizeable_tuple_five:
    def __init__(self):
        self.array1 = resizeable_list(numpy.float32)
        self.array2 = resizeable_list(numpy.int32)
        self.array3 = resizeable_list(numpy.int32)
        self.array4 = resizeable_list(numpy.int32)
        self.array5 = resizeable_list(numpy.int32)
        self.size = 0

    def append(self, object):
        self.array1.append(object[0])
        self.array2.append(object[1])
        self.array3.append(object[2])
        self.array4.append(object[3])
        self.array5.append(object[4])
        self.size += 1

    def extend(self, objects):
        for object in objects:
            self.append(object)

    def __iter__(self):
        for index in range(self.size):
            yield (self.array1[index], self.array2[index], self.array3[index], self.array4[index], self.array5[index])

    def __getitem__(self, item):
        return self.array1[item], self.array2[item], self.array3[item], self.array4[item], self.array5[item]

    def __len__(self):
        return self.array1.current_size
