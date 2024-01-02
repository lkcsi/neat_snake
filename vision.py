from snake import Position
from game import SnakeGame
from math import atan2, degrees

class SnakeVision:

    def __init__(self, game:SnakeGame):
        self.game = game

    #check food distance at direction
    def check_food(self, dx, dy):
        snake = self.game.snake
        fruit = self.game.fruit
        pos = Position(snake.head.x + dx, snake.head.y + dy)
        while 0 <= pos.x < self.game.cols and 0 <= pos.y < self.game.rows:
            if pos == fruit:
                if dx!=0: return dx*fruit.x - dx*snake.head.x
                if dy!=0: return dy*fruit.y - dy*snake.head.y
            pos = Position(pos.x + dx, pos.y + dy)

        return -1

    def check_obstacle(self, dx, dy):
        snake = self.game.snake
        pos = Position(snake.head.x + dx, snake.head.y + dy)
        result = 1
        while not snake.is_part(pos) and 0 <= pos.x < self.game.cols and 0 <= pos.y < self.game.rows:
            pos = Position(pos.x + dx, pos.y + dy)
            result += 1
        return result

    def get_wall_distances(self):
        snake = self.game.snake
        ahead = self.check_obstacle(snake.dx, snake.dy)
        left = self.check_obstacle(snake.dy, snake.dx * -1)
        right = self.check_obstacle(snake.dy * -1, snake.dx)

        return [left, ahead, right]

    def get_vision(self):
        snake = self.game.snake
        ahead = self.check_obstacle(snake.dx, snake.dy)
        left = self.check_obstacle(snake.dy, snake.dx * -1)
        right = self.check_obstacle(snake.dy * -1, snake.dx)
        angle = self.get_fruit_angle()
        return [left, ahead, right, angle]

    def get_fruit_angle(self):
        snake = self.game.snake
        fruit = self.game.fruit

        deltaX = snake.head.x - fruit.x
        deltaY = snake.head.y - fruit.y

        #if snake.dx == -1: deltaX, deltaY = deltaY, deltaX
        if snake.dy == -1: deltaX, deltaY = deltaX, deltaY
        elif snake.dy == 1: deltaX, deltaY = deltaX*-1, deltaY*-1
        elif snake.dx == -1: deltaX, deltaY = deltaY*-1, deltaX
        elif snake.dx == 1: deltaX, deltaY = deltaY,-1*deltaX

        angle = atan2(deltaX, deltaY)
        return angle
        #ahead = self.check_food(snake.dx, snake.dy)
        #left = self.check_food(snake.dy, snake.dx * -1)
        #right = self.check_food(snake.dy * -1, snake.dx)

        #return [left, ahead, right]