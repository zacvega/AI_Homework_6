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
        
        print("  | ", end="")

        for i in range(self.rows+1):
            for j in range(self.columns+1):
                if (i==0):
                    if j != self.columns:
                        print(j+1, end=" | ")
                else:
                    if(j==0):
                        print(i, end=" | ")
                    else:
                        # print(" ", end="")
                        print(self.locStatus((i,j)), end=" | ")
            print()

            
def main():
    #create playing area
    board = Board(nonESquares=[((3,3), 4), ((1,1), 2)], rows=9,columns=9)   
    board.printFloorLayout()
    board.PlacePiece((2,1), 4)
    board.printFloorLayout()

    return 0

if(__name__ == "__main__"):
    main()