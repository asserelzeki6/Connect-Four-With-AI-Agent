import sys
import os

# Add the project's root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.Node import Node

def board_score(board, player1, player2):
    score = 0
    row = len(board)
    col = len(board[0])
    for i in range(row-1,-1,-1):
        for j in range(col):
            if(board[i][j]==player1):
                score+=calc_stream(board, i, j, player1,1)     
            elif(board[i][j]==player2):
                score+=calc_stream(board, i, j, player2, -1)
    return score
    
def move_score(board, score, i, j, player, cost):
    score+=specific_calc_stream(board,i,j,player,cost)
    return score

def calc_stream(board, i, j, player, cost):
    col = len(board[0])
    h=1
    v=1
    dl=1
    dr=1
    score=0
    for k in range(1,4):
        if j+k<col: # horizontal right
            if board[i][j+k]==player:
                h+=1
            else:
                h=0
            if i-k>=0: # diagonal right
                if board[i-k][j+k]==player:
                    dr+=1
                else:
                    dr=0
        if i-k >= 0: # vertical up
            if board[i-k][j]==player:
                v+=1
            else:
                v=0
            if j-k >=0: # diagonal left
                if board[i-k][j-k]==player:
                    dl+=1
                else:
                    dl=0
    if h==4 : score+=cost
    if v==4 : score+=cost
    if dr==4 : score+=cost
    if dl==4 : score+=cost
    return score

def specific_calc_stream(board, i, j, player, cost):
    row = len(board)
    col = len(board[0])
    hr=1
    hl=1
    vu=1
    vd=1
    dlu=1
    dru=1
    score=0
    for k in range(1,4):
        if j+k<col: # horizontal right
            if board[i][j+k]==player:
                hr+=1
            else:
                hr=0
            if i-k>=0: # diagonal right up
                if board[i-k][j+k]==player:
                    dru+=1
                else:
                    dru=0
        if i-k >= 0: # vertical up
            if board[i-k][j]==player:
                vu+=1
            else:
                vu=0
            if j-k >=0: # diagonal left up
                if board[i-k][j-k]==player:
                    dlu+=1
                else:
                    dlu=0

        ############################################
        if j-k>=0: # horizontal left
            if board[i][j-k]==player:
                hl+=1
            else:
                hl=0
            if i-k>=0: # diagonal right down
                if board[i-k][j-k]==player:
                    drd+=1
                else:
                    drd=0
        if i+k < row: # vertical down
            if board[i+k][j]==player:
                vd+=1
            else:
                vd=0
            if j-k >=0: # diagonal left down
                if board[i+k][j-k]==player:
                    dld+=1
                else:
                    dld=0
        
    if hr==4 : score+=cost
    if vu==4 : score+=cost
    if dru==4 : score+=cost
    if dlu==4 : score+=cost
    if hl==4 : score+=cost
    if vd==4 : score+=cost
    if drd==4 : score+=cost
    if dld==4 : score+=cost
    return score

def print_board(board):
    for i in range(len(board)):
        print(board[i])

def driver():
    row = 6
    col = 7
    player1 = 'r'
    player2 = 'y'
    board = [['.' for _ in range(col)] for _ in range(row)]
    board[4][0]=player2
    board[4][1]=player2
    board[4][2]=player2
    board[4][3]=player2
    print_board(board, row)
    score = board_score(board,player1,player2)
    print(score)
    board[4][4]=player2
    print_board(board)
    score = move_score(board, score, 4, 4, player2, -1)
    print(score)

# driver()