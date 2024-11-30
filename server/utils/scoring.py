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


def heuristic(board, player, opponent):
    weights = [
        [3, 4, 5, 7, 5, 4, 3],
        [4, 6, 8, 10, 8, 6, 4],
        [5, 8, 11, 13, 11, 8, 5],
        [5, 8, 11, 13, 11, 8, 5],
        [4, 6, 8, 10, 8, 6, 4],
        [3, 4, 5, 7, 5, 4, 3]
    ]

    score = 0

    # 1. Weighted Position Scoring
    for row in range(6):
        for col in range(7):
            if board[row][col] == player:
                score += weights[row][col]
            elif board[row][col] == opponent:
                score -= weights[row][col]
    # 2. Line Potential Scoring
    player_2_in_row = count_sequences(board, 2, player)
    player_3_in_row = count_sequences(board, 3, player)
    player_4_in_row = count_sequences(board, 4, player)
    opponent_2_in_row = count_sequences(board, 2, opponent)
    opponent_3_in_row = count_sequences(board, 3, opponent)
    opponent_4_in_row = count_sequences(board, 4, opponent)
    # Scoring: prioritize longer sequences
    score += 10 * player_2_in_row + 50 * player_3_in_row + 1000 * player_4_in_row
    score -= 10 * opponent_2_in_row + 50 * opponent_3_in_row + 1000 * opponent_4_in_row

    # 3. Blocking Opponent Moves
    # If the opponent has a winning move (3 in a row with a potential 4th), penalize heavily
    if opponent_3_in_row > 0:
        score -= 1000  # Significant penalty for allowing the opponent to win next turn

    return score


def count_sequences(board, length, piece):
    count = 0

    def is_open(row, col, dr, dc):
        count_ = 0
        start_row = row
        start_col = col
        end_row = row + (length - 1) * dr
        end_col = col + (length - 1) * dc

        # Check bounds for the sequence itself
        if not (0 <= start_row < 6 and 0 <= start_col < 7 and
                0 <= end_row < 6 and 0 <= end_col < 7):
            return False
        if dr == 0 and dc ==1:
            count_ = 0
            for i in range(1, 4 - length + 1):
                if col - i < 0:
                    break
                if board[row][col-i] == '.' or board[row][col-i] == piece:
                    count_ += 1
                else:
                    break
            for i in range(length, 4):  # 2,3 #3
                # print('here')                #range 2 to 4 , range 3 to 4
                # print(row+i)
                if col + i > 6:
                    break
                if board[row][col+i] == '.' or board[row][col+i] == piece:
                    count_ += 1
                else:
                    break

        #row=1,col=1,dr=1,dc=0
        # Check the cells before and after the sequence
        if dr == 1 and dc==0:
            count_ = 0
            for i in range(1,4-length+1):
                if row-i<0:
                    break
                if board[row-i][col]=='.' or board[row-i][col]==piece:
                    count_+=1
                else:
                    break
            for i in range(length,4): #2,3 #3
                # print('here')                #range 2 to 4 , range 3 to 4
                # print(row+i)
                if row+i>5:
                    break
                if board[row + i][col] == '.' or board[row + i][col] == piece:
                    count_ += 1
                else:
                    break
        if dr == 1 and dc == 1:
            count_ = 0
            for i in range(1, 4 - length + 1):
                if row - i < 0 or col - i < 0:
                    break
                if board[row - i][col-i] == '.' or board[row - i][col-i] == piece:
                    count_ += 1
                else:
                    break
            for i in range(length, 4):  # 2,3 #3
                # print('here')                #range 2 to 4 , range 3 to 4
                # print(row+i)
                if row + i > 5 or col + i > 6:
                    break
                if board[row + i][col+i] == '.' or board[row + i][col+i] == piece:
                    count_ += 1
                else:
                    break

        if dr == -1 and dc == 1:
            count_ = 0
            for i in range(1, 4 - length + 1):
                if row + i >5 or col - i < 0:
                    break
                if board[row + i][col-i] == '.' or board[row + i][col-i] == piece:
                    count_ += 1
                else:
                    break
            for i in range(length, 4):  # 2,3 #3
                # print('here')                #range 2 to 4 , range 3 to 4
                # print(row+i)
                if row - i < 0 or col + i > 6:
                    break
                if board[row - i][col+i] == '.' or board[row - i][col+i] == piece:
                    count_ += 1
                else:
                    break
        return count_>=4-length


    # Horizontal
    for row in range(6):
        for col in range(7 - length + 1):
            if all(board[row][col + i] == piece for i in range(length)):
                if is_open(row, col, 0, 1):
                    count += 1

    # Vertical
    for row in range(6 - length + 1):
        for col in range(7):
            if all(board[row + i][col] == piece for i in range(length)):
                if is_open(row, col, 1, 0):
                    count += 1

    # Diagonal (positive slope)
    for row in range(6 - length + 1):
        for col in range(7 - length + 1):
            if all(board[row + i][col + i] == piece for i in range(length)):
                if is_open(row, col, 1, 1):
                    count += 1

    # Diagonal (negative slope)
    for row in range(length - 1, 6):
        for col in range(7 - length + 1):
            if all(board[row - i][col + i] == piece for i in range(length)):
                if is_open(row, col, -1, 1):
                    count += 1

    return count
