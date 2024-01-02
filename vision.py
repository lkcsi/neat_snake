from snake import Position
from game import SnakeGame
from math import atan2, degrees, dist

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

    def check_obstacle(self, dx, dy, distance):
        snake = self.game.snake
        pos = Position(snake.head.x, snake.head.y)
        for i in range(1, distance+1):
            pos = Position(pos.x + dx, pos.y + dy)
            if (snake.is_part(pos) or
                0 > pos.x or pos.x >= self.game.cols or 
                0 > pos.y or pos.y >= self.game.rows):
                    return i
        return distance + 1

    def check_danger(self, dx, dy, max):
        snake = self.game.snake
        pos = Position(snake.head.x, snake.head.y)
        for i in range(1, max+1):
            pos = Position(pos.x + dx, pos.y + dy)
            if (snake.is_part(pos) or
                0 > pos.x or pos.x >= self.game.cols or 
                0 > pos.y or pos.y >= self.game.rows):
                    return max+1 - i
        return 0

    def check_obstacles(self, distance):
        snake = self.game.snake
        ahead = self.check_obstacle(snake.dx, snake.dy, distance)
        left = self.check_obstacle(snake.dy, snake.dx * -1, distance)
        right = self.check_obstacle(snake.dy * -1, snake.dx, distance)

        return [left, ahead, right]

    def get_vision(self):
        #obstacles = self.check_obstacles(self.game.rows)
        food = self.get_fruit_orientation_2()
        danger = self.get_danger()
        #delta = self.delta()
        #angle = self.get_fruit_angle()
        #return [wall[0], wall[1], wall[2], angle]
        return danger + food

    def get_fruit_distance(self):
        snake = self.game.snake

        ahead = self.check_food(snake.dx, snake.dy)
        left = self.check_food(snake.dy, snake.dx * -1)
        right = self.check_food(snake.dy * -1, snake.dx)

        return [left, ahead, right]
    
    def get_danger(self):
        snake = self.game.snake
        ahead = self.check_danger(snake.dx, snake.dy, 3)
        left = self.check_danger(snake.dy, snake.dx*-1, 3)
        right = self.check_danger(snake.dy*-1, snake.dx, 3)

        return [ahead, left, right]

    def get_fruit_orientation_2(self):
        fruit = self.game.fruit
        snake = self.game.snake

        ahead, left, right = 0, 0, 0
        if snake.dx != 0:
            if snake.dx * fruit.x > snake.dx * snake.head.x:
                ahead = 1
            if snake.dx * fruit.y < snake.dx * snake.head.y: left = 1
            elif snake.dx * fruit.y > snake.dx * snake.head.y: right = 1
        if snake.dy != 0:
            if snake.dy * fruit.y > snake.dy * snake.head.y:
                ahead = 1
            if snake.dy * fruit.x < snake.dy * snake.head.x: right = 1
            elif snake.dy * fruit.x > snake.dy * snake.head.x: left = 1

        return [ahead ,left, right]
        

    def get_fruit_orientation(self):
        snake = self.game.snake
        fruit = self.game.fruit
        if snake.dy != 0:
            ahead, right, left = self.game.rows, self.game.cols, self.game.cols
            delta = snake.dy * fruit.y - snake.dy * snake.head.y
            if delta >= 0:
                ahead = delta
                left = snake.dy * fruit.x - snake.dy * snake.head.x
                if left < 0: right, left = abs(left), right
        if snake.dx != 0:
            ahead, right, left = self.game.cols, self.game.rows, self.game.rows
            delta = snake.dx * fruit.x - snake.dx * snake.head.x
            if delta >= 0:
                ahead = delta
                right = snake.dx * fruit.y - snake.dx * snake.head.y
                if right < 0: left, right = abs(right), left
        return [left, ahead, right]

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
        distance = dist([fruit.x, fruit.y], [snake.head.x, snake.head.y])
        return [angle, distance]