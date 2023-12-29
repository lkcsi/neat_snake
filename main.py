from display import SnakeDisplay
from game import SnakeGame
from snake import Direction
import pygame, neat, pickle, os, time, math
from neat.nn import FeedForwardNetwork

class Game:
    def __init__(self):
        self.cols = 20
        self.rows = 20
        self.size = (self.rows, self.cols)
        self.game = SnakeGame(self.size)
        self.display = SnakeDisplay(self.game, (500,500))

    def move(self, key):
        game = self.game
        if key == pygame.K_w:
            game.set_direction(Direction.UP)
        elif key == pygame.K_s:
            game.set_direction(Direction.DOWN)
        elif key == pygame.K_d:
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
                self.game.loop()
                self.display.draw()
                print(self.get_fruit_distances())
                counter = 0
            counter += 1

    def get_wall_distances(self):
        snake = self.game.snake

        left = snake.head.x
        right = self.cols - 1 - snake.head.x
        top = snake.head.y
        bottom = self.rows - 1 - snake.head.y

        return [left,right,top,bottom]

    def get_fruit_distances(self):
        snake = self.game.snake
        fruit = self.game.fruit

        return [fruit.x - snake.head.x, fruit.y - snake.head.y]

    def play_ai(self, net:FeedForwardNetwork, draw=False):
        clock = pygame.time.Clock()
        alive, idle, last_score = 0, 0, 0
        game = self.game
        while True:
            if draw:
                clock.tick(60)
                self.display.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0

            if game.game_over:
                return alive
            #decision
            output = net.activate(self.get_fruit_distances() + self.get_wall_distances())
            decision = output.index(max(output))
            match decision:
                case 0: game.set_direction(Direction.UP)
                case 1: game.set_direction(Direction.DOWN)
                case 2: game.set_direction(Direction.RIGHT)
                case 3: game.set_direction(Direction.LEFT)

            #check loop
            if game.points == last_score:
                idle += 1
            else: 
                last_score = game.points
                idle = 0

            alive += 1
            game.loop()
            if idle > 100:
                return alive

def test_genomes(genomes, config):
    for (_, genome) in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        game = Game()
        alive = game.play_ai(net, False)

        genome.fitness = game.game.points * 10 + alive / 10

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
        winner = p.run(test_genomes, 2)
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
    #Game().play(speed=2)
    #train_ai('neat-checkpoint-184')
    #train_ai()
    test_best()
    pygame.quit()