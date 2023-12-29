from game import SnakeGame
from pygame import display, draw


class SnakeDisplay:
    WHITE = (255,255,255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLACK = (0,0,0)
    def __init__(self, game:SnakeGame, size:tuple):
        self.game = game
        self.size = size
        self.window = display.set_mode(size)
        self.rect_x = size[0] // game.cols
        self.rect_y = size[1] // game.rows

    def draw(self):
        self.window.fill(self.WHITE)
        self.draw_fruits()
        self.draw_snake()
        display.update()

    def draw_fruits(self):
        fruit = self.game.fruit
        if fruit:
            draw.rect(self.window, self.RED, (fruit.x * self.rect_x, fruit.y * self.rect_y, self.rect_x, self.rect_y))

    def draw_snake(self):
        snake = self.game.snake
        draw.rect(self.window, self.BLACK, (snake.head.x * self.rect_x, snake.head.y * self.rect_y, self.rect_x, self.rect_y))
        for part in snake.parts:
            draw.rect(self.window, self.BLACK, (part.x * self.rect_x, part.y * self.rect_y, self.rect_x, self.rect_y))

