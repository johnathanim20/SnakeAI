import pygame
import time
import random
from enum import Enum

BLOCK_SIZE = 40
#PLAYABLE SNAKE GAME : RUN WITH python snakePlayer.py 
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class Color(Enum):
    RED = pygame.Color(255,0,0)
    GREEN = pygame.Color(0,255,0)
    BLACK = pygame.Color(0,0,0)
    WHITE = pygame.Color(255,255,255)

class Snake():
    def __init__(self, speed, direction, head, color):
        self.speed = speed
        self.direction = direction
        self.head = head
        self.positions = [[head[0] - i, head[1]] for i in range(0,BLOCK_SIZE*4,BLOCK_SIZE)]
        self.color = color 

class Fruit():
    def __init__(self, gridDimensionX, gridDimensionY, color):
        self.x = random.randint(1, gridDimensionX - 1)//BLOCK_SIZE * BLOCK_SIZE
        self.y = random.randint(1, gridDimensionY - 1)//BLOCK_SIZE * BLOCK_SIZE
        self.color = color
    
class SnakePlayer:
    def __init__(self, window):
        pygame.init()
        self.window = window
        self.frame = 0
        self.snake = Snake(15, Direction.RIGHT.value, [BLOCK_SIZE*4,BLOCK_SIZE*4], Color.GREEN)
        self.fruit = Fruit(window[0], window[1], Color.RED)
        self.score = 0
        self.game_window = pygame.display.set_mode((window[0], window[1]))
        self.font = pygame.font.SysFont('times new roman', 25)
        self.fps = pygame.time.Clock()
        self.game_over = False
        pygame.display.set_caption('Snake')
        self.gameStep()

    def show_score(self, color):
        score_surface = self.font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        self.game_window.blit(score_surface, score_rect)    
    def drawGameObjects(self):
        self.game_window.fill(Color.BLACK.value)
        for s in self.snake.positions:
            pygame.draw.rect(self.game_window, self.snake.color.value, pygame.Rect(s[0], s[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.game_window, self.fruit.color.value, pygame.Rect(self.fruit.x, self.fruit.y, BLOCK_SIZE, BLOCK_SIZE))
        self.show_score(Color.WHITE.value)
        pygame.display.update()
        self.fps.tick(self.snake.speed)


    def gameStep(self):
        lastDir = Direction.RIGHT
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.snake.direction != Direction.RIGHT:
                        lastDir = Direction.LEFT
                    elif event.key == pygame.K_RIGHT and self.snake.direction != Direction.LEFT:
                        lastDir = Direction.RIGHT
                    elif event.key == pygame.K_UP and self.snake.direction != Direction.DOWN:
                        lastDir = Direction.UP
                    elif event.key == pygame.K_DOWN and self.snake.direction != Direction.UP:
                        lastDir = Direction.DOWN
            if lastDir == Direction.RIGHT and self.snake.direction != Direction.LEFT:
                self.snake.direction = Direction.RIGHT
                self.snake.head = [self.snake.head[0] + BLOCK_SIZE, self.snake.head[1]]
            elif lastDir == Direction.LEFT and self.snake.direction != Direction.RIGHT:
                self.snake.direction = Direction.LEFT
                self.snake.head = [self.snake.head[0] - BLOCK_SIZE, self.snake.head[1]]
            elif lastDir == Direction.UP and self.snake.direction != Direction.DOWN:
                self.snake.direction = Direction.UP
                self.snake.head = [self.snake.head[0] , self.snake.head[1] - BLOCK_SIZE]
            elif lastDir == Direction.DOWN and self.snake.direction != Direction.UP:
                self.snake.direction = Direction.DOWN
                self.snake.head = [self.snake.head[0], self.snake.head[1] + BLOCK_SIZE]
            self.illegalMove(self.snake.head)
            self.snake.positions.insert(0, self.snake.head)
            self.eatFruit()
            self.drawGameObjects()
    def eatFruit(self):
        if self.snake.head == [self.fruit.x, self.fruit.y]:
            self.score += 1
            self.fruit = Fruit(self.window[0], self.window[1], Color.RED)
        else:
            self.snake.positions.pop()
    def illegalMove(self, head):
        if head in self.snake.positions[1:]:
            pygame.quit()
            quit()
        if head[0] < 0 or head[0] > self.window[0] or head[1] < 0 or head[1] > self.window[1]:
            pygame.quit()
            quit()
s = SnakePlayer([BLOCK_SIZE*40,BLOCK_SIZE*20])