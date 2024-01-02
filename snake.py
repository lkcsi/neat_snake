from enum import Enum
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set(self, pos):
        self.x = pos.x
        self.y = pos.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'{self.x}, {self.y}'

    def __repr__(self):
        return f'[{self.x}, {self.y}]'

class Direction(Enum):
    LEFT = 0
    RIGHT = 1

class Snake:
    def __init__(self, pos:Position):
        self.head = pos
        self.dx = 1
        self.dy = 0
        self.increase = False
        self.parts = []
    
    def set_direction(self, dir: Direction):
        if dir == Direction.RIGHT:
            dx = self.dx
            self.dx = self.dy * -1
            self.dy = dx
        if dir == Direction.LEFT:
            dy = self.dy
            self.dy = self.dx * -1
            self.dx = dy

    def length(self):
        return 1 + len(self.parts)

    def is_part(self, pos:Position):
        for part in self.parts:
            if part == pos:
                return True
        return False

    def move(self):
        last_pos = Position(self.head.x, self.head.y)
        self.move_head(self.head)
        for part in self.parts:
            temp = Position(part.x, part.y)
            part.x = last_pos.x
            part.y = last_pos.y
            last_pos = temp
        if self.increase:
            self.parts.append(Position(last_pos.x, last_pos.y))
            self.increase = False

    def move_head(self, pos:Position):
        self.head.x += self.dx
        self.head.y += self.dy

    def add_part(self):
        self.increase = True


