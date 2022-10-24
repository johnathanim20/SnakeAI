import pygame
import time
import random
from enum import Enum
import numpy as np

#snake game environment for NN to train and test with
pygame.init()
BLOCK_SIZE = 40
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

class SnakeGame:
    def __init__(self, width=720, height=480):
        self.frame = 0
        self.score = 0
        self.game_over = False
        self.width = width
        self.height = height
    def start(self):
        self.init_snake()
        self.init_food()
        self.init_render()
    def init_snake(self):
        x = random.randint(0, self.width - BLOCK_SIZE)//BLOCK_SIZE*BLOCK_SIZE
        y = random.randint(0, self.height - BLOCK_SIZE)//BLOCK_SIZE*BLOCK_SIZE
        self.snake_body = [[x,y]]
        self.direction = Direction.RIGHT
        self.speed = 50
    def init_food(self):
        x = random.randint(0, self.width - BLOCK_SIZE)//BLOCK_SIZE*BLOCK_SIZE
        y = random.randint(0, self.height - BLOCK_SIZE)//BLOCK_SIZE*BLOCK_SIZE
        while [x,y] in self.snake_body:
            x = random.randint(0, self.width - BLOCK_SIZE)//BLOCK_SIZE*BLOCK_SIZE
            y = random.randint(0, self.height - BLOCK_SIZE)//BLOCK_SIZE*BLOCK_SIZE
        self.fruit = [x,y]
    def eat_fruit(self):
        return self.fruit == self.snake_body[0]
    def collision(self):
        head = self.snake_body[0]
        if self.frame > 100 * len(self.snake_body):
            return True
        if head in self.snake_body[1:] or head[0] < 0 or head[0] > self.width - BLOCK_SIZE or head[1] < 0 or head[1] > self.height - BLOCK_SIZE:
            return True
        return False
    def init_render(self):
        self.fps = pygame.time.Clock()
        self.game_window = pygame.display.set_mode((self.width, self.height))
        self.game_window.fill(Color.BLACK.value)
        pygame.display.set_caption('Snake')
        self.render()
    def render(self):
        self.game_window.fill(Color.BLACK.value)
        for s in self.snake_body:
            pygame.draw.rect(self.game_window, Color.GREEN.value, pygame.Rect(s[0], s[1],BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.game_window, Color.RED.value, pygame.Rect(self.fruit[0], self.fruit[1],BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.update()
        self.fps.tick(self.speed)
    def play_step(self, action):
        #[1,0,0] - keep current direction
        #[0,1,0] - turn right
        #[0,0,1] - turn left
        #can't go backwards - invalid move in this implementation
        self.frame += 1
        if not self.game_over:
            dir_l = self.direction == Direction.LEFT
            dir_r = self.direction == Direction.RIGHT
            dir_u = self.direction == Direction.UP
            dir_d = self.direction == Direction.DOWN
            if np.array_equal(action,[0,1,0]):
                if dir_l:
                    self.direction = Direction.UP
                elif dir_u:
                    self.direction = Direction.RIGHT
                elif dir_r:
                    self.direction = Direction.DOWN
                else:
                    self.direction = Direction.LEFT
            elif np.array_equal(action,[0,0,1]):
                if dir_l:
                    self.direction = Direction.DOWN
                elif dir_u:
                    self.direction = Direction.LEFT
                elif dir_r:
                    self.direction = Direction.UP
                else:
                    self.direction = Direction.RIGHT
            if self.direction == Direction.LEFT:
                head = [self.snake_body[0][0] - BLOCK_SIZE, self.snake_body[0][1]]
            elif self.direction == Direction.RIGHT:
                head = [self.snake_body[0][0] + BLOCK_SIZE, self.snake_body[0][1]]
            elif self.direction == Direction.DOWN:
                head = [self.snake_body[0][0], self.snake_body[0][1] + BLOCK_SIZE]
            elif self.direction == Direction.UP:
                head = [self.snake_body[0][0], self.snake_body[0][1] - BLOCK_SIZE]
            self.snake_body.insert(0, head)
            reward = 0
            if self.eat_fruit():
                self.score += 1
                reward = 10
                self.init_food()
            else:
                self.snake_body.pop()
            if self.collision():
                reward = -10
                self.game_over = True
            else:
                self.render()
            return reward, self.game_over, self.score
    def obstacleRight(self):
        head = self.snake_body[0]
        if head[0] + BLOCK_SIZE > self.width:
            return True
        tmp = [head[0] + BLOCK_SIZE, head[1]]
        if tmp in self.snake_body[1:]:
            return True
        return False
    def obstacleDown(self):
        head = self.snake_body[0]
        if head[1] + BLOCK_SIZE > self.height:
            return True
        tmp = [head[0], head[1] + BLOCK_SIZE]
        if tmp in self.snake_body[1:]:
            return True
        return False
    def obstacleLeft(self):
        head = self.snake_body[0]
        if head[0] - BLOCK_SIZE < 0:
            return True
        tmp = [head[0] - BLOCK_SIZE, head[1]]
        if tmp in self.snake_body[1:]:
            return True
        return False
    def obstacleUp(self):
        head = self.snake_body[0]
        if head[1] - BLOCK_SIZE < 0:
            return True
        tmp = [head[0], head[1] - BLOCK_SIZE]
        if tmp in self.snake_body[1:]:
            return True
        return False
