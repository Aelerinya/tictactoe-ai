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
            ennemy = self.players[(self.turn + 1) % 2]
            previous_state = self.flatten_grid(player)

            reward = 0
            #Player do a move
            move = player.play(previous_state, player.icon)
            while self.grid[move[0]][move[1]] != 0:
                move = player.play(previous_state, player.icon)
            self.grid[move[0]][move[1]] = player.icon
            #Add new state to player dataset
            player.add_data((previous_state, move, reward))
            #Does the player win ?
            if self.is_winner(player.icon):
                #Add win states
                win_state = self.flatten_grid(player)
                player.states[win_state] = 1
                lose_state = self.flatten_grid(ennemy)
                ennemy.states[lose_state] = -1
                return player.name
            self.turn += 1
        return "Tie"

    def log(self):
        for i in self.grid:
            print(i)

    def flatten_grid(self, player):
        return tuple([1 if item not in [0, player.icon] else item for sublist in self.grid for item in sublist])

class morpion_player():
    def __init__(self, name, icon, trainable = True, human=False):
        self.dataset = []
        self.states = {}
        self.name = name
        self.icon = icon
        self.human = human
        self.epsilon = 1
        self.trainable = trainable

    def play(self, state, player):
        if self.human:
            for i in [0, 3, 6]:
                print(state[i : i + 3])
            line = int(input("line:"))
            column = int(input("column:"))
            return (line, column)
        else:
            if random.random() > self.epsilon:
                return self.greedy_play(state)
            else:
                return (random.randint(0, 2), random.randint(0, 2))

    def greedy_play(self, state):
        moves = ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2))
        best_move = (random.randint(0, 2), random.randint(0, 2))
        best_value = 0
        #print("State:")
        #print(state)
        for m in moves:
            if self.is_valid(state, m):
                next_state = self.get_next_state(state, m)
                #print(f"Move : {m} Value : {self.states[next_state] if next_state in self.states else 0}")
                next_value = self.states[next_state] if (next_state in self.states) else 0
                if next_value > best_value:
                    best_value = next_value
                    best_move = m
        #print(f"State : {state} Best move : {best_move} = {best_value}")
        #print(f"Choosen : {best_move}")
        return best_move

    def get_next_state(self, state, move):
            next_state = list(state)
            next_state[move[0] * 3 + move[1]] = self.icon
            next_state = tuple(next_state)
            return next_state

    def is_valid(self, state, move):
        if state[move[0] * 3 + move[1]] == 0:
            return True
        else:
            return False

    def add_data(self, move):
        self.dataset.append(move)

    def train(self, learning_rate):
        if self.trainable == False:
            return
        for data in reversed(self.dataset):
            state = data[0]
            if not state in self.states:
                self.states[state] = 0
            next_state = self.get_next_state(state, data[1])
            increment = self.states[next_state] if (next_state in self.states) else 0
            self.states[state] += learning_rate * (increment - self.states[state])
        self.dataset = []
        self.epsilon = self.epsilon * 0.9995 if (self.epsilon > 0.005) else 0.005

def main():
    stats = {}
    p1 = morpion_player("IA", "X")
    p2 = morpion_player("IA 2", "O")
    for i in range(0, 10000):
        players = [p1, p2]
        random.shuffle(players)
        game = morpion_game(players[0], players[1])
        winner = game.run()
        #print(f"Winner : {winner}")
        p1.train(0.01)
        p2.train(0.01)
        if not winner in stats:
            stats[winner] = 1
        else:
            stats[winner] += 1
    # for i in p1.states:
    #     if not p1.states[i] in [-100, 0, 100]:
    #         print(f"{i} : {p1.states[i]}")
    best_move = max(p1.states, key=p1.states.get)
    print(f"{best_move} = {p1.states[best_move]}")
    print(f"number of states : {len(p1.states)}")
    print(stats)
    random_player = morpion_player("random", "R", False)
    stats = {p1.name : 0, random_player.name : 0, "Tie" : 0}
    plays = 1000
    for i in range(0, plays):
        players = [p1, random_player]
        random.shuffle(players)
        game = morpion_game(players[0], players[1])
        winner = game.run()
        stats[winner] += 1
    #print(p1.states)
    print(f"Win rates :")
    for i in stats:
        print(f"{i} : {stats[i] / plays:.2f}")
    human = morpion_player("human", "H", False, True)
    while False:
        game = morpion_game(p1, human)
        winner = game.run()
        print(f"Winner : {winner}")

if __name__ == "__main__":
    main()
