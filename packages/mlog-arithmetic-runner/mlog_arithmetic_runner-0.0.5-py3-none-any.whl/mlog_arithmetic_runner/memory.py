import math


class MemoryCell:
    def __init__(self, size: int):
        self.size: int = size
        self.memory: list[float] = [0.0, ] * size

    def read(self, position) -> float:
        pos: int = int(math.floor(position))
        if pos < 0 or pos >= self.size:
            return 0.0
        return self.memory[pos]

    def write(self, position, value) -> None:
        pos: int = int(math.floor(position))
        if pos < 0 or pos >= self.size:
            return
        self.memory[pos] = value

    def reset(self):
        self.memory = [0.0, ] * self.size
