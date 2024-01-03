from display import SnakeDisplay
from game import SnakeGame
from vision import SnakeVision
from snake import Direction, Position
import pygame, neat, pickle, os, sys, copy
from neat.nn import FeedForwardNetwork
import loop_check, math

class Game:
    def __init__(self):
        self.cols = 20
        self.rows = 20
        self.size = (self.rows, self.cols)
        self.game = SnakeGame(self.size)
        self.display = SnakeDisplay(self.game, (500,500))
        self.vision = SnakeVision(self.game)
        self.positions = []

    def move(self, key):
        game = self.game
        if key == pygame.K_d:
            game.set_direction(Direction.RIGHT)
        elif key == pygame.K_a:
            game.set_direction(Direction.LEFT)

    def play(self, fps=60, speed=10):
        clock = pygame.time.Clock()
        counter = 0
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

            if counter == speed:
                print(self.game.loop())
                self.display.draw()
                print(self.vision.get_vision())
                counter = 0
            counter += 1

    def play_ai(self, net:FeedForwardNetwork, draw=False):
        clock = pygame.time.Clock()
        loop, limit = 0, 50
        game = self.game
        while True:
            if draw:
                clock.tick(60)
                self.display.draw()

            #decision
            output = net.activate(self.vision.get_vision())
            decision = output.index(max(output))
            match decision:
                case 1: 
                    game.set_direction(Direction.LEFT)
                case 2: 
                    game.set_direction(Direction.RIGHT)

            loop += 1
            result = game.loop()
            if result == 'fruit':
                loop = 0
            elif result:
                return result
            if loop == limit + game.snake.length() * 10:
                return 'loop'

def test_genomes(genomes, config):
    events = {'body':0, 'wall':0, 'win': 0, 'loop': 0}
    for (_, genome) in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        game = Game()

        result = game.play_ai(net, False)
        genome.fitness += game.game.points * 10
        events[result] += 1
    print(events)

def test_best():
    config = load_config()
    with open('best.genome', 'rb') as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    game = Game()
    print(game.play_ai(winner_net, True))

def train_ai(checkpoint = None):
    config = load_config()
    if checkpoint:
        p = neat.Checkpointer.restore_checkpoint(checkpoint)
    else:
        p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(test_genomes, 50)

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
        case 'manual': Game().play(speed=10) 
        case 'test': test_best()

    pygame.quit()