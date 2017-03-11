import sys
import time


class Ticker:
    def __init__(self, name, max_ticks):
        self.name = name

        self.current_time = time.time()
        self.last_time = time.time()

        self.current_ticks = 0
        self.last_ticks = 0
        self.max_ticks = max_ticks

    def tick(self):
        self.current_time = time.time()
        self.current_ticks += 1
        if self.current_ticks == self.max_ticks or time.time() - self.last_time > 15:
            self.print_statistics()
            self.last_time = self.current_time
            self.last_ticks = self.current_ticks
            return True
        return False

    def print_statistics(self):
        print >> sys.stderr, ("%s >> %s: currently processed %d/%d ticks (%f per second, %f seconds per tick)"
                              "; approximately %f seconds left" % (
              time.strftime('%X %x %Z'), self.name, self.current_ticks, self.max_ticks,
              1.0 * (self.current_ticks - self.last_ticks) / (self.current_time - self.last_time),
              1.0 * (self.current_time - self.last_time) / (self.current_ticks - self.last_ticks),
              (self.max_ticks - self.current_ticks) / ((self.current_ticks - self.last_ticks) / (self.current_time - self.last_time))
        ))