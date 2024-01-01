from display import SnakeDisplay
from game import SnakeGame
from snake import Direction, Position
import pygame, neat, pickle, os, sys, copy
from neat.nn import FeedForwardNetwork
import loop_check

class Game:
    def __init__(self):
        self.cols = 20
        self.rows = 20
        self.size = (self.rows, self.cols)
        self.game = SnakeGame(self.size)
        self.display = SnakeDisplay(self.game, (500,500))
        self.positions = []

    def move(self, key):
        game = self.game
        if key == pygame.K_d:
            game.set_direction(Direction.RIGHT)
        elif key == pygame.K_a:
            game.set_direction(Direction.LEFT)

    def play(self, fps=60, speed=1):
        clock = pygame.time.Clock()
        counter = 0
        limit = 10 - speed
        run = True
        while run:
            clock.tick(fps)
            run = not self.game.game_over
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                if event.type == pygame.KEYDOWN:
                    self.move(event.key)

            if counter == limit:
                event = self.game.loop()['event']
                if event: 
                    print(event)
                self.display.draw()
                print(self.game.snake.head, self.get_wall_distances())
                counter = 0
            counter += 1


    def get_wall_distances(self):
        snake = self.game.snake
        left, ahead, right = 0, 0, 0
        if snake.dx == -1:
            ahead = snake.head.x + 1
            left = self.rows - snake.head.y
            right = snake.head.y + 1
        elif snake.dx == 1:
            ahead = self.cols - snake.head.x
            left = snake.head.y + 1
            right = self.rows - snake.head.y
        elif snake.dy == -1:
            ahead = snake.head.y + 1
            left = snake.head.x + 1
            right = self.cols - snake.head.x
        elif snake.dy == 1:
            ahead = self.rows - snake.head.y
            left = self.cols - snake.head.x
            right = snake.head.x + 1

        return [left, ahead, right]

    def get_fruit_distances(self):
        snake = self.game.snake
        fruit = self.game.fruit

        left, ahead, right = 0, 0, 0
        if snake.dx != 0:
            if snake.head.y == fruit.y and snake.dx * fruit.x > snake.dx * snake.head.x:
                ahead = 1
            elif snake.head.x == fruit.x:
                if fruit.y * snake.dx < snake.head.y * snake.dx:
                    left = 1
                if fruit.y * snake.dx > snake.head.y * snake.dx:
                    right = 1

        elif snake.dy != 0:
            if snake.head.x == fruit.x and snake.dy * fruit.y > snake.dy * snake.head.y:
                ahead = 1
            elif snake.head.y == fruit.y:
                if fruit.x * snake.dy < snake.head.x * snake.dy:
                    right = 1
                if fruit.x * snake.dy > snake.head.x * snake.dy:
                    left = 1

        return [left, ahead, right]

    def play_ai(self, net:FeedForwardNetwork, draw=False):
        clock = pygame.time.Clock()
        alive = 0
        loop, limit = 0, 200
        game = self.game
        while True:
            if draw:
                clock.tick(60)
                self.display.draw()

            #decision
            output = net.activate(self.get_fruit_distances() + self.get_wall_distances())
            decision = output.index(max(output))
            match decision:
                case 1: game.set_direction(Direction.RIGHT)
                case 2: game.set_direction(Direction.LEFT)

            alive += 1
            loop += 1
            event = game.loop()['event']
            if event == 'fruit':
                loop = 0
            elif event == 'collision':
                return {'reason':'collision', 'alive':alive}
            if loop == limit:
                return {'reason': 'loop', 'alive': alive}
            if game.points == 100:
                return {'reason': 'win', 'alive': alive}


def test_genomes(genomes, config):
    for (_, genome) in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        game = Game()

        result = game.play_ai(net, False)
        #if result['reason'] != 'loop':
        #    genome.fitness += min(100, result['alive'])
        genome.fitness += game.game.points * 10
        if result['reason'] == 'win':
            genome.fitness += 100

def test_best():
    config = load_config()
    with open('best.genome', 'rb') as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    game = Game()
    game.play_ai(winner_net, True)

def train_ai(checkpoint = None):
    config = load_config()
    if checkpoint:
        p = neat.Checkpointer.restore_checkpoint(checkpoint)
    else:
        p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())
    p.add_reporter(neat.Checkpointer(1))

    try:
        winner = p.run(test_genomes, 100)
    except KeyboardInterrupt:
        print('interrupted')

    with open('best.genome', 'wb') as f:
        pickle.dump(winner, f)

def load_config():
    local_dir = os.path.dirname(__file__)
    config_dir = os.path.join(local_dir, 'config.txt')

    return neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                       neat.DefaultSpeciesSet, neat.DefaultStagnation, config_dir)

if __name__ == '__main__':
    print('args', sys.argv)
    match sys.argv[1]:
        case 'train': 
            checkpoint = None
            if len(sys.argv) > 2:
                checkpoint = sys.argv[2]
            train_ai(checkpoint)
        case 'manual': Game().play() 
        case 'test': test_best()

    pygame.quit()