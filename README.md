#Tic Tac Toe AI in Python3

This project implements an epsilon-greedy reinforcement learning algorithm to train an AI to play tic tac toe.

It it composed of two main classes:
* _morpion\_game_ : a game of tic tac toe composed of two players
* _morpion\_player_ : a player in a game of Tic Tac Toe, with its own memory, name and identifier

The program creates two competing AIs who play 100.000 games against each other.
Then the first AI play games against a fully random player to estimate its skills.
Finally the user can play games against the AI.

Using this reinforcement algorithm, the AI can achieve around **91%** of win rate against a random AI.
