from typing import Optional


class MovingAvg():
    def __init__(self, size: int):
        self.data = []
        self.size = size
        self.cur_index = 0
        self.avg = 0
        # for _ in range(size):
        #     self.data.append(0)

    def insert(self, value: float):
        if len(self.data) < self.size:
            self.data.append(value)
        else:
            self.data[self.cur_index] = value
        len_of_data = len(self.data)
        total_data = sum(self.data)
        self.avg = round(total_data / len_of_data, 2)
        self.cur_index = (self.cur_index + 1) % len(self.data)

    def __repr__(self):
        return f"{len(self.data)} - {self.avg}"

    def __str__(self):
        return self.__repr__()
