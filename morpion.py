#!/usr/bin/env python3

import random

class morpion_game():
    def __init__(self, player1, player2):
        self.turn = 0
        self.players = [player1, player2]
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

    def run(self):
        while self.turn < 9:
            player = self.players[self.turn % 2]
            previous_state = [1 if item not in [0, player.icon] else item for item in self.flatten_grid()]

            reward = 0
            #Player do a move
            move = player.play(previous_state, player.icon)
            if self.grid[move[0]][move[1]] == 0:
                self.grid[move[0]][move[1]] = player.icon
            else:
                reward = -1
            #Add new state to player dataset
            state = self.flatten_grid()
            player.add_data((previous_state, state, move, reward))
            #Does the player win ?
            if self.is_winner(player.icon):
                return player.name
            self.turn += 1
        return "Tie"

    def log(self):
        for i in self.grid:
            print(i)

    def flatten_grid(self):
        return tuple([item for sublist in self.grid for item in sublist])

class morpion_player():
    def __init__(self, name, icon, human=False):
        self.dataset = []
        self.states = {}
        self.name = name
        self.icon = icon
        self.human = human

    def play(self, state, player):
        if self.human:
            for i in [0, 3, 6]:
                print(state[i : i + 3])
            line = int(input("line:"))
            column = int(input("column:"))
            return (line, column)
        else:
            return (random.randint(0, 2), random.randint(0, 2))

    def add_data(self, move):
        self.dataset.append(move)

def main():
    p1 = morpion_player("IA", "X")
    p2 = morpion_player("IA 2", "O")
    game = morpion_game(p1, p2)
    winner = game.run()
    if p1.name == winner:
        p1.add_data((game.flatten_grid(), 10))
        p2.add_data((game.flatten_grid(), -10))
    elif p2.name == winner:
        p1.add_data((game.flatten_grid(), -10))
        p2.add_data((game.flatten_grid(), 10))
    else:
        p1.add_data((game.flatten_grid(), 0))
        p2.add_data((game.flatten_grid(), 0))
    print(f"Winner : {winner}")
    print(p1.dataset)
    print(p2.dataset)

if __name__ == "__main__":
    main()
