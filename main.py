import copy
import time
import random
import numpy as np

#functions for solving the Sudoku puzzles. The grid parameter being passes 
# to the function is a 2d array with zero's indicating empty spaces and integers [1-9] in
# the filled in spaces. 

def solve_sudoku(grid):
    def is_valid(num, pos):
        for i in range(9):
            if grid[pos[0]][i] == num and pos[1] != i:
                return False
        for i in range(9):
            if grid[i][pos[1]] == num and pos[0] != i:
                return False
        box_x, box_y = pos[1] // 3, pos[0] // 3
        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x*3, box_x*3 + 3):
                if grid[i][j] == num and (i, j) != pos:
                    return False
        return True
    
    #Returns a list of all empty spaces in the board
    def find_empty():
        empty_list = [(i, j) for i in range(9) for j in range(9) if grid[i][j] == 0]
        if empty_list:
            empty_list.sort(key=lambda x: (x[1], x[0]))
            return empty_list[0]
        return None
    
    def domain_size(pos):
        row, col = pos
        possible_nums = set(range(1, 10))
        for i in range(9):
            possible_nums.discard(grid[row][i])
            possible_nums.discard(grid[i][col])
        box_x, box_y = col // 3, row // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                possible_nums.discard(grid[i][j])
        return len(possible_nums)
    
     #determines the degree at a specific position.
    def degree(pos):
        row, col = pos
        count = 0
        for i in range(9):
            if grid[row][i] == 0:
                count += 1
            if grid[i][col] == 0:
                count += 1
        box_x, box_y = col // 3, row // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if grid[i][j] == 0:
                    count += 1
        return count

    assignment_counter = 0
    

    def solve():
        nonlocal assignment_counter
        empty = find_empty()
        if not empty:
            return True
        row, col = empty
        
        for i in range(1, 10):
            if is_valid(i, (row, col)):
                if assignment_counter < 4:
                    print(f"Variable: ({row+1}, {col+1}), Domain Size: {domain_size((row+1, col+1))}, Degree: {degree((row+1, col+1))}, Value: {i}")
                    assignment_counter += 1
                grid[row][col] = i
                #print(grid[row][col])
            
                if solve():
                    return True

                grid[row][col] = 0
                #print('\t', grid[row][col])
        return False

    solve()
    return grid             

class Board:
    def __init__(self, nonESquares = [], rows = 9, columns = 9):
        """
        Initializes the space as a nxm matrix by rows and columns, 

        ## Parameters
         * nonESquares:  List of non empty spaces in the 9x9 board
            * Type: List of tuples

        * rows:  Number of rows for space 
            * Type: int

        * columns: Number of columns for space 
            * Type: int
        """
        
        self.eSquares = list() 
        for i in range(rows):
            for j in range(columns):
                if((i+1,j+1) not in nonESquares): 
                    self.eSquares.append((i+1, j+1))

        #init values to themselves        
        self.nonESquares = dict()

        for i in nonESquares:
            self.nonESquares[i[0]] = i[1]

        self.rows = rows
        self.columns = columns
    

    #given a location, return ' ' if empty, the number associated if not empty
    def locStatus(self, location):
        if location in self.nonESquares.keys():
            return self.nonESquares.get(location)
        else:
            return ' '

    # method that formats and prints the board state
    def printFloorLayout(self):
        """
        Displays the layout of the space
        each sell has format (row, colum)
        * If the space contains a piece it will display its number
        """
        for row in range(self.rows+1):
            numColor = "\033[36m"
            boardColor = "\033[35m"
            pieceColor = "\033[32m"
            dataStr = f"{boardColor}"
            spacerStr = f""
            
            for column in range(self.columns+1):
                if row % 3 == 0 and row != 0 and row != self.rows:
                    rowBold = True 
                else:
                    rowBold = False
                if column % 3 == 0 and column != 0 and column != self.columns:
                    columnBold = True
                else:
                    columnBold = False
                rowPiece = "\u2501" if rowBold else "\u2500"
                columnPiece = "\u2503" if columnBold else "\u2502"
                match rowBold, columnBold:
                        case True, True:
                            intersectionPiece = "\u254b"
                        case False, False:
                            intersectionPiece = "\u253c"
                        case True, False:
                            intersectionPiece = "\u253f"
                        case False, True:
                            intersectionPiece = "\u2542"
                if (row == self.rows):
                    if columnBold:
                        intersectionPiece = "\u2538"
                    else:
                        intersectionPiece = "\u2534"
                if (column == self.columns):
                    if row == self.rows:
                        intersectionPiece = "\u2518"

                    elif rowBold:
                        intersectionPiece = "\u2525"
                    else:
                        intersectionPiece = "\u2524"

                if row == 0:
                    if column == 0:
                        dataStr += f"  {columnPiece}"
                    else:
                        dataStr += f' {numColor}{column}{boardColor} {columnPiece}'

                else:
                    if(column==0):
                        dataStr += f'{numColor}{row}{boardColor} {columnPiece}'
                    else:
                        dataStr += f' {pieceColor}{self.locStatus((row,column))}{boardColor} {columnPiece}'

                if (column % 3 == 0 and column != 0):
                    spacerStr += rowPiece * 3 + intersectionPiece
                elif column == 0:
                    spacerStr += rowPiece * 2 + intersectionPiece
                else:
                    spacerStr += rowPiece * 3 + intersectionPiece
            print(dataStr)
            print(spacerStr)
            
def main():

    boardA = [((1,3),1),((1,6),2),((2,3),5),((2,6),6),((2,8),3),((3,1),4),((3,2),6),((3,6),5),((4,4),1),((4,6),4),((5,1),6),((5,4),8),((5,7),1),((5,8),4),((5,9),3),((6,5),9),((6,7),5),((6,9),8),((7,1),8),((7,5),4),((7,6),9),((7,8),5),((8,1),1),((8,4),3),((8,5),2),((9,3),9),((9,7),3)]
    boardB = [((1,3),5),((1,5),1),((2,3),2),((2,6),4),((2,8),3),((3,1),1),((3,3),9),((3,7),2),((3,9),6),((4,1),2),((4,5),3),((5,2),4),((5,7),7),((6,1),5),((6,6),7),((6,9),1),((7,4),6),((7,6),3),((8,2),6),((8,4),1),((9,5),7),((9,8),5)]
    boardC = [((1,1),6),((1,2),7),((2,2),2),((2,3),5),((3,2),9),((3,4),5),((3,5),6),((3,7),2),((4,1),3),((4,5),8),((4,7),9),((5,7),8),((5,9),1),((6,4),4),((6,5),7),((7,3),8),((7,4),6),((7,8),9),((8,8),1),((9,1),1),((9,3),6),((9,5),5),((9,8),7)]
    
    #Solves boards A, B, and C
    for presetBoard in [boardA, boardB, boardC]:
        spaces = np.zeros((9, 9), dtype=int)
        for i in presetBoard:
            spaces[i[0][0]-1][i[0][1]-1] = i[1]
    
        # return
        print("*"*39 +'\n\n\n')
        board = Board(nonESquares=presetBoard, rows=9,columns=9)
        board.printFloorLayout()
        start = time.process_time()
        solvedBoard = solve_sudoku(spaces)
        #print(solvedBoard)
        end = time.process_time()

        solvedBoardList = []
        for i, row in enumerate(solvedBoard):
            for j, value in enumerate(row):
                solvedBoardList.append(((i+1, j+1), int(value)))

        print("*"*39)
        board = Board(nonESquares = solvedBoardList, rows =9, columns =9)
        board.printFloorLayout()
        print(f'Time taken: {end-start}s')

    return 0

if(__name__ == "__main__"):
    main()