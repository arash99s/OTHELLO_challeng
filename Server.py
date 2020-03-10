### color = 1 : white
### color = 2 : black
import os
import json
import sys

class Cell:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
    def __eq__(self, other):
        return (
                self.__class__ == other.__class__ and
                self.row == other.row and
                self.col == other.col
        )
    def __hash__(self):
        return self.row + 17 * self.col
    def __str__(self):
        return '('+str(self.row)+',' + str(self.col) + ')'


dirname = os.path.dirname(sys.argv[0])

def run_client(client_path : str , first_time : bool = False):
    os.chdir(client_path)
    if first_time:
        executable = 'g++ ' + 'main.cpp' + ' -o output -std=c++11'
        os.system(executable)
    executable = 'output.exe'
    os.system(executable)
    os.chdir(dirname)

def write_now_json(board : [] , c1 : str , c2 : str):
    board_dict = {}
    board_dict['color'] = 1
    board_dict['turn'] = board
    with open(c1 +'now_board.json', 'w') as outfile1:
        json.dump(board_dict, outfile1)
    board_dict['color'] = 2
    with open(c2 + 'now_board.json', 'w') as outfile2:
        json.dump(board_dict, outfile2)
    print('done writing')

def write_log_json(board_dict: {}):
    with open('log.json' , 'w') as outfile:
        json.dump(board_dict, outfile)

def initialize(board : []):
    white_dir = input('enter white directory: ')
    # white_dir = "Client1"
    c1_path = dirname + '/' + white_dir + '/'

    black_dir = input('enter black directory: ')
    # black_dir = "Client2"
    c2_path = dirname + '/' + black_dir + '/'

    write_now_json(board, c1_path, c2_path)
    return c1_path , c2_path

def find_coordinate(c1: str, c2:str):
    client1 = open(c1 + 'out.txt', 'r')
    coordinate1 = client1.read().split()
    client2 = open(c2 + 'out.txt', 'r')
    coordinate2 = client2.read().split()
    return coordinate1 , coordinate2

def find_mycells(board: [], color: int):
    mycells = []
    for i in range(8):
        for j in range(8):
            if board[i][j] == color:
               mycells.append(Cell(i, j))
    return mycells

def fill_color(cell1: Cell, cell2: Cell , color: int , board: []):
    if cell1.row == cell2.row:
        min_col = min(cell1.col, cell2.col)
        max_col = max(cell1.col, cell2.col)
        for col in range(min_col, max_col+1):
            board[cell1.row][col] = color
    elif cell1.col == cell2.col:
        min_row = min(cell1.row, cell2.row)
        max_row = max(cell1.row, cell2.row)
        for row in range(min_row, max_row+1):
            board[row][cell1.col] = color
    else:
        min_col = min(cell1.col, cell2.col)
        max_col = max(cell1.col, cell2.col)
        min_row = min(cell1.row, cell2.row)
        max_row = max(cell1.row, cell2.row)
        if (cell1.col == min_col and cell1.row == min_row) or (cell1.col == max_col and cell1.row == max_row):
            row = min_row
            for col in range(min_col, max_col+1):
                board[row][col] = color
                row += 1
        else:
            row = max_row
            for col in range(min_col, max_col + 1):
                board[row][col] = color
                row -= 1

def available_cells(board: [], color: int, current_cell: Cell):
    if color == 1:
        opp_color = 2
    else :
        opp_color = 1
    mycells = find_mycells(board, color)
    available = []
    for cell in mycells:
        ### down
        flag = False
        row = cell.row + 1
        col = cell.col
        while row < 8 and board[row][col] == opp_color:
            row += 1
            flag = True
        if row < 8 and board[row][col] == 0 and flag:
            available.append(Cell(row, col))
            if Cell(row, col) == current_cell:
                fill_color(cell, current_cell, color, board)
        ### up
        flag = False
        row = cell.row - 1
        col = cell.col
        while row >= 0 and board[row][col] == opp_color:
            row -= 1
            flag = True
        if row >= 0 and board[row][col] == 0 and flag:
            available.append(Cell(row, col))
            if Cell(row, col) == current_cell:
                fill_color(cell, current_cell, color, board)
        ### right
        flag = False
        row = cell.row
        col = cell.col + 1
        while col < 8 and board[row][col] == opp_color:
            col += 1
            flag = True
        if col < 8 and board[row][col] == 0 and flag:
            available.append(Cell(row, col))
            if Cell(row, col) == current_cell:
                fill_color(cell, current_cell, color, board)
        ### left
        flag = False
        row = cell.row
        col = cell.col - 1
        while col >= 0 and board[row][col] == opp_color:
            col -= 1
            flag = True
        if col >= 0 and board[row][col] == 0 and flag:
            available.append(Cell(row, col))
            if Cell(row, col) == current_cell:
                fill_color(cell, current_cell, color, board)
        ### up_right
        flag = False
        row = cell.row - 1
        col = cell.col + 1
        while row >= 0 and col < 8 and board[row][col] == opp_color:
            row -= 1
            col += 1
            flag = True
        if row >= 0 and col < 8 and board[row][col] == 0 and flag:
            available.append(Cell(row, col))
            if Cell(row, col) == current_cell:
                fill_color(cell, current_cell, color, board)
        ### down_right
        flag = False
        row = cell.row + 1
        col = cell.col + 1
        while row < 8 and col < 8 and board[row][col] == opp_color:
            row += 1
            col += 1
            flag = True
        if row < 8 and col < 8 and board[row][col] == 0 and flag:
            available.append(Cell(row, col))
            if Cell(row, col) == current_cell:
                fill_color(cell, current_cell, color, board)
        ### up_left
        flag = False
        row = cell.row - 1
        col = cell.col - 1
        while row >= 0 and col >= 0 and board[row][col] == opp_color:
            row -= 1
            col -= 1
            flag = True
        if row >= 0 and col >= 0 and board[row][col] == 0 and flag:
            available.append(Cell(row, col))
            if Cell(row, col) == current_cell:
                fill_color(cell, current_cell, color, board)
        ### down_left
        flag = False
        row = cell.row + 1
        col = cell.col - 1
        while row < 8 and col >= 0 and board[row][col] == opp_color:
            row += 1
            col -= 1
            flag = True
        if row < 8 and col >= 0 and board[row][col] == 0 and flag:
            available.append(Cell(row, col))
            if Cell(row, col) == current_cell:
                fill_color(cell, current_cell, color, board)

    return available

def is_finished(board: [], available: []):
    white_cells = find_mycells(board, 1)
    black_cells = find_mycells(board, 2)
    if len(white_cells) + len(black_cells) == 64:
        return True
    if len(available) == 0:
        return True
    return False

def copy_board(board: []):
    new_board = []
    for b in board:
        new_board.append(b.copy())
    return new_board

def run():
    now_board = [[0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 1, 2, 0, 0, 0],
                 [0, 0, 0, 2, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0]]
    ###
    client1_path , client2_path = initialize(now_board)
    ###
    data_dict = {}
    data_dict['turn0'] = copy_board(now_board)
    for turn in range(1, 1000):
        print('server: '+'turn : ' , turn)
        if turn%2 == 1:
            color = 1
            cp = client1_path
        else:
            color = 2
            cp = client2_path
        ### run
        if turn == 1 or turn == 2: # build and run
            run_client(cp, True)
        else :
            run_client(cp)
        ###
        coordinate1, coordinate2 = find_coordinate(client1_path, client2_path)
        if color == 1:
            print('server: '+'white choose: ' , coordinate1)
            row = int(coordinate1[0])
            col = int(coordinate1[1])
        else :
            print('server: '+'black choose: ', coordinate2)
            row = int(coordinate2[0])
            col = int(coordinate2[1])
        available = available_cells(now_board, color, Cell(row,col))
        if available.__contains__(Cell(row, col)):
            print('server: '+'correct choice')
            # for b in now_board:
            #     print(b)
        else:
            print('server: '+'error in choice')
        write_now_json(now_board, client1_path, client2_path)
        json_turn = 'turn'+str(turn)
        data_dict[json_turn] = copy_board(now_board)
        if is_finished(now_board, available):
            break

    write_log_json(data_dict)
    for b in now_board:
        print(b)



if __name__ == '__main__':
    print(dirname)
    run()
    e = input('enter any key to exit')