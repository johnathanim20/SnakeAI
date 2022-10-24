import random
import numpy as np
from collections import deque
from snakeAI import SnakeGame, Direction
from helper import plot
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pygame
import time
MAX_MEMORY = 1000
BATCH_SIZE = 10
LR = 0.001

class NN:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 
        self.gamma = 0.9 
        self.memory = deque(maxlen=MAX_MEMORY) 
        self.model = self.createModel() 

    def createModel(self):
        model = keras.Sequential()
        model.add(layers.Dense(units=11, input_dim=11))
        model.add(layers.Dense(units=16, activation='relu'))
        model.add(layers.Dense(units=3,  activation = 'linear'))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
        return model

    def get_state(self, game):
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN
        state = [(dir_u and game.obstacleUp()) or
                (dir_r and game.obstacleRight()) or
                (dir_d and game.obstacleDown()) or
                (dir_l and game.obstacleLeft()),

                (dir_u and game.obstacleRight()) or
                (dir_l and game.obstacleUp()) or
                (dir_d and game.obstacleLeft()) or
                (dir_r and game.obstacleDown()),

                (dir_u and game.obstacleLeft()) or
                (dir_l and game.obstacleDown()) or
                (dir_r and game.obstacleUp()) or
                (dir_d and game.obstacleRight()),

                # Move direction
                dir_l,
                dir_r,
                dir_u,
                dir_d,
                # Fruit location 
                game.fruit[0] < game.snake_body[0][0],  
                game.fruit[0] > game.snake_body[0][0],  
                game.fruit[1] < game.snake_body[0][1], 
                game.fruit[1] > game.snake_body[0][1]  
                ]
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            batch = random.sample(self.memory, BATCH_SIZE)
        else:
            batch = self.memory
        for state, action, reward, next_state, done in batch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state.reshape((1, 11)), verbose=0)[0])
            target_f = self.model.predict(state.reshape((1, 11)), verbose=0)
            target_f[0][np.argmax(action)] = target
            self.model.fit(state.reshape((1, 11)), target_f, batch_size = BATCH_SIZE, epochs=1, verbose=0)

    def train_short_memory(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = reward + self.gamma * np.amax(self.model.predict(next_state.reshape((1, 11)), verbose=0)[0])
        
        target_f = self.model.predict(state.reshape((1, 11)), verbose=0)
        target_f[0][np.argmax(action)] = target
        start = time.time()
        self.model.fit(state.reshape((1, 11)), target_f, batch_size = BATCH_SIZE, epochs=1, verbose=0)
    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            prediction = self.model.predict(state.reshape((1,11)), verbose=0)
            move = np.argmax(prediction[0])
            final_move[move] = 1
        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    nn = NN()
    game = SnakeGame()
    game.start()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        state_old = nn.get_state(game)
        final_move = nn.get_action(state_old)
        reward, done, score = game.play_step(final_move)
        state_new = nn.get_state(game)
        nn.train_short_memory(state_old, final_move, reward, state_new, done)
        nn.remember(state_old, final_move, reward, state_new, done)
        if done:
            game = SnakeGame()
            game.start()
            nn.n_games += 1
            nn.train_long_memory()
            if score > record:
                record = score
            print('Game', nn.n_games, 'Score', score, 'Record:', record)
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / nn.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
if __name__ == '__main__':
    train()