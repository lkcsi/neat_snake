from enum import Enum
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set(self, pos):
        self.x = pos.x
        self.y = pos.y

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Snake:
    def __init__(self, pos:Position):
        self.head = pos
        self.dir = Direction.RIGHT
        self.parts = []
    
    def set_direction(self, dir: Direction):
        if dir == Direction.DOWN and self.dir == Direction.UP:
            return
        if dir == Direction.UP and self.dir == Direction.DOWN:
            return
        if dir == Direction.RIGHT and self.dir == Direction.LEFT:
            return
        if dir == Direction.LEFT and self.dir == Direction.RIGHT:
            return

        self.dir = dir

    def move(self):
        last_pos = Position(self.head.x, self.head.y)
        self.move_head(self.head)
        for part in self.parts:
            temp = Position(part.x, part.y)
            part.x = last_pos.x
            part.y = last_pos.y
            last_pos = temp

    def move_head(self, pos:Position):
        match self.dir:
            case Direction.UP: pos.y -= 1
            case Direction.DOWN: pos.y += 1
            case Direction.LEFT: pos.x -= 1
            case Direction.RIGHT: pos.x += 1

    def add_part(self):
        if len(self.parts) == 0:
            last_pos = self.head
        else: last_pos = self.parts[len(self.parts)-1]
        
        match self.dir:
            case Direction.UP: self.parts.append(Position(last_pos.x, last_pos.y + 1))
            case Direction.DOWN: self.parts.append(Position(last_pos.x, last_pos.y - 1))
            case Direction.LEFT: self.parts.append(Position(last_pos.x + 1, last_pos.y))
            case Direction.RIGHT: self.parts.append(Position(last_pos.x - 1, last_pos.y))


