from MCTS import MCTS
from Coach import Coach
from tictactoe.TicTacToeGame import TicTacToeGame, display
from tictactoe.keras.NNet import NNetWrapper as NNet
import sys
import numpy as np
from utils import *

humanPlayer = -1
computerPlayer = 1
"""
use this script as the backend to the tictactoeaz.py front-end.
"""

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


game = TicTacToeGame()

# nnet players - The Computer Player
n1 = NNet(game)
n1.load_checkpoint('./pretrained_models/tictactoe/keras/','best-25eps-25sim-10epch.pth.tar')
args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
mcts1 = MCTS(game, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))
board = game.getInitBoard()

while True:
    eprint("Enter msg Id:")
    msgId = int(input())

    if msgId == 0:
        board = game.getInitBoard()
        print(0)
    elif msgId == 1:
        # Computer Turn
        action = n1p(game.getCanonicalForm(board, computerPlayer))
        board, curPlayer = game.getNextState(board, computerPlayer, action)
        print(0)
        print(action)

    elif msgId == 2:
        # Human Turn - as long as we know it is a valid move then
        # we don't need to call the human player code. It only
        # checks for a valid move anyway.
        action = int(input()) #hp(game.getCanonicalForm(board, humanPlayer))
        eprint("Human move is:", action)
        print(0)
        board, curPlayer = game.getNextState(board, humanPlayer, action)

    elif msgId == 3:
        # Game Over?
        x = game.getGameEnded(board, 1)
        if x != int(x):
            print(3) # It was a draw - x is returned as 1E-4.
        elif x == 1:
            print(1) # Computer Won
        elif x == -1:
            print(2) # Human Won
        else:
            print(0) # Game Continues
