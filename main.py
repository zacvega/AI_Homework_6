import copy
import time


class Board:
    def __init__(self, nonESquares = [], rows = 9, columns = 9):
        """
        Initializes the space as a nxm matrix by rows and columns, 

        ## Parameters
        * rows:  Number of rows for space 
            * Type: int

        * columns: Number of columns for space 
            * Type: int
        * eSquares: List of location(s) (ordered pairs) for empty squares 
            * Type: [(int, int),...]
            * (1 based index)
        * nonESquares: List of location(s) (ordered pairs) and their values for squares claimed 
            * Type: [((int, int)) int),...]
            * (1 based index)
        """
        #the number of squares in the board that are not x or o
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


    #place a number at a given board location
    def PlacePiece(self, location, number):
        #validate location is on the board
        if(location[0]<1 or location[0]>= self.rows+1 or location[1]<1 or location[1] >= self.columns+1): 
            return
        
        #if pos is empty, place 
        if location in self.eSquares: 
            self.eSquares.remove(location)
            self.nonESquares[location] = number
            return location
    
    
    #clear a board space (just used for debugging)
    def clearPiece(self, location): 

        #clear from o spaces
        if location in self.nonESquares.keys(): 
            del self.nonESquares[location]

        if location not in self.eSquares: 
            self.eSquares.append(location)
        
        return location


    #given a location, return ' ' if empty, the number associated if not empty
    def locStatus(self, location):
        if location in self.nonESquares.keys():
            return self.nonESquares.get(location)
        else:
            return ' '

   
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
    #create playing area
    board = Board(nonESquares=[((3,3), 4), ((1,1), 2)], rows=9,columns=9)
    board.printFloorLayout()
    print()
    board.PlacePiece((2,1), 4)
    board.printFloorLayout()

    return 0

if(__name__ == "__main__"):
    main()