from snake import Position
from game import SnakeGame
from math import atan2, degrees, dist

class SnakeVision:

    def __init__(self, game:SnakeGame):
        self.game = game

    #check food distance at direction
    def check_fruit(self, dx, dy):
        snake = self.game.snake
        fruit = self.game.fruit
        pos = Position(snake.head.x + dx, snake.head.y + dy)
        while 0 <= pos.x < self.game.cols and 0 <= pos.y < self.game.rows:
            if pos in snake.parts:
                return 0
            if pos == fruit:
                return 1
            pos = Position(pos.x + dx, pos.y + dy)
        return 0

    def check_snake(self, dx, dy):
        snake = self.game.snake
        pos = Position(snake.head.x + dx, snake.head.y + dy)
        while 0 <= pos.x < self.game.cols and 0 <= pos.y < self.game.rows:
            if pos in snake.parts:
                return 1
            pos = Position(pos.x + dx, pos.y + dy)
        return 0

    def check_wall(self, dx, dy):
        snake = self.game.snake
        pos = Position(snake.head.x + dx, snake.head.y + dy)
        if 0 > pos.x or pos.x >= self.game.cols or 0 > pos.y or pos.y >= self.game.rows:
            return 1
        return 0

    def get_fruit(self):
        snake = self.game.snake
        ahead = self.check_fruit(snake.dx, snake.dy)
        left = self.check_fruit(snake.dy, snake.dx * -1)
        right = self.check_fruit(snake.dy * -1, snake.dx)

        return [left, ahead, right]

    def get_snake(self):
        snake = self.game.snake
        ahead = self.check_snake(snake.dx, snake.dy)
        left = self.check_snake(snake.dy, snake.dx * -1)
        right = self.check_snake(snake.dy * -1, snake.dx)

        return [left, ahead, right]

    def get_wall(self):
        snake = self.game.snake
        ahead = self.check_wall(snake.dx, snake.dy)
        left = self.check_wall(snake.dy, snake.dx * -1)
        right = self.check_wall(snake.dy * -1, snake.dx)

        return [left, ahead, right]


    def get_vision(self):
        food = self.get_fruit()
        danger = self.get_wall()
        snake = self.get_snake()
        return danger + food + snake