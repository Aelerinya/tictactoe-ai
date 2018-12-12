#!/usr/bin/env python3

import random

class morpion_game():
    def __init__(self, player1, player2):
        self.turn = 0
        self.players = [player1, player2]
        random.shuffle(self.players)
        self.grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def is_winner(self, player):
        #Verify lines
        for i in range(0, 3):
            if self.grid[i] == [player] * 3:
                return 1

        #Verify columns
        for i in range(0, 3):
            if [row[i] for row in self.grid] == [player] * 3:
                return 1

        #Verify diagonals
        if [self.grid[i][i] for i in range(0, 3)] == [player] * 3:
            return 1
        if [self.grid[i][2 - i] for i in range(0, 3)] == [player] * 3:
            return 1

        return 0

    def log(self):
        for i in self.grid:
            print(i)
