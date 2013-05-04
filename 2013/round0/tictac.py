#!/usr/bin/python
import sys

def winner(board, player):
    def ok(row,col):
        return (board[row][col] == player) or (board[row][col] == "T")

    # check the rows
    for row in range(0, 4):
        for col in range(0, 4):
            if not ok(row, col):
                break
        else:
            return True

    # check the columns
    for col in range(0, 4):
        for row in range(0, 4):
            if not ok(row, col):
                break
        else:
            return True

    # check downgoing diagonal
    for col in range(0, 4):
        if not ok(col, col):
            break
    else:
        return True

    # check upgoing diagonal
    for col in range(0, 4):
        if not ok(3 - col, col):
            break
    else:
        return True

    return False


def game_not_over(board):
    for line in board:
        if "." in line:
            return True
    return False

T = int(raw_input())
for t in range(1, T+1):
    sys.stdout.write("Case #%d: " % t)

    # Read in the blank line separating test cases:
    if t > 1:
        junk = raw_input()
        
    # Read in the 4x4 board:
    board = ["","","",""]
    for i in range(0,4):
        board[i] = raw_input()

    if winner(board, "X"):
        print "X won"
    elif winner(board, "O"):
        print "O won"
    elif game_not_over(board):
        print "Game has not completed"
    else:
        print "Draw"

