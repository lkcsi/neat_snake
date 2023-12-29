from snake import Snake, Position, Direction
from random import randint

class SnakeGame:
    def __init__(self, matrix:tuple):
        self.cols = matrix[0]
        self.rows = matrix[1]
        self.fruit = None
        self.snake = Snake(Position(self.cols // 2, self.rows // 2))
        self.points = 0
        self.game_over = False
        self.add_fruit()

    def loop(self):
        if not self.game_over:
            self.check_collision()
            self.check_fruit()
            self.snake.move()
            
    def check_collision(self):
        snake = self.snake
        if snake.head.x < 0 or snake.head.x == self.rows or snake.head.y < 0 or snake.head.y == self.cols:
            self.game_over = True

    def check_fruit(self):
        snake = self.snake
        fruit = self.fruit
        if fruit and fruit.x == snake.head.x and fruit.y == snake.head.y:
            fruit = None
            self.points += 1
            self.add_fruit()
            self.add_part()

    def add_part(self):
        self.snake.add_part()

    def set_direction(self, dir:Direction):
        snake = self.snake
        snake.set_direction(dir)

    def add_fruit(self):
        pos_x = randint(0, self.cols-1)
        pos_y = randint(0, self.rows-1)
        self.fruit = Position(pos_x ,pos_y)