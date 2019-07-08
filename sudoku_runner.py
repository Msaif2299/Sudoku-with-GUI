import tkinter as tk
from collections import defaultdict
import random
'''---------------------------------Utility Functions---------------------------------------------'''


def matrix(buttonList):
    '''
        Function to get all the values in the button grid as matrix
        Args:
            buttonList -> a list of buttons(2D matrix of buttonGrid() objects)
        Returns:
            m -> matrix generated from reading all the button values
        NOTE: 1) Use only if the class buttonGrid() has been defined, or will result in error.
              2) To resolve this issue, import tkinter_tester (it is a file, look in same directory)
    '''
    m = [[0 for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):
            m[i][j] = buttonList[i][j].button['text']
    return m


def isComplete(board):
    '''
    Helper function to check if the given matrix is complete or not (does 0 exist in any piece)
        Args:
            board -> matrix
        Returns:
            bool -> True:  if it is complete
                    False: if it is not complete
    '''
    for r in range(0, 9):
        for c in range(0, 9):
            if board[r][c] == 0:  # Any empty cell found
                return False
    return True  # No empty cells found i.e board is completely filled


'''--------------------------------Sudoku functions------------------------------------------------'''


def sudoku_valid(m):
    '''
        Function to check if the sudoku grid is valid or not
        Args:
            m -> matrix of the sudoku
        Returns:
            bool -> True: if the sudoku is valid
                    False: if the sudoku is invalid
        NOTE: Put 0 in places of numbers which are empty (as in, to be filled later), they will be ignored
    '''
    for i in range(
        9):  # row and column checking loop (if there are only one occurance of 1-9 digits in eveyr row)
        d = defaultdict(int)  # to map all the values into the dictionary
        for x in m[i]:  # iteration over every element in given row
            if x == 0:  # ignoring 0 (check NOTE why)
                continue
            d[x] += 1  # counting number of occurances
            if d[x] > 1:  # if a second occurance is found, immediately return False
                return False
        d = defaultdict(int)  # to map all values into the dictionary
        for x in m[:][i]:  # iteration over every element in given column
            if x == 0:  # ignoring 0 (check NOTE why)
                continue
            d[x] += 1  # counting number of occurances
            if d[x] > 1:  # if a second occurance is found, immediately return False
                return False
    for i in [0, 3, 6]:  # loop to check all the subgrids in the sudoku puzzle, the 3x3 ones
        for j in [0, 3, 6]:  # every subgrid is represented by i, j similar to a matrix
            # to map all the values in the subgrid into the dictionary
            d = defaultdict(int)
            for x in range(i, i + 3):  # iterating the rows in the subgrid
                for y in range(j, j + 3):  # iterating the columns in the subgrid
                    if m[x][y] == 0:  # ignoring 0 (see NOTE why)
                        continue
                    d[m[x][y]] += 1  # counting number of occurances
                    if d[m[x][y]] > 1:  # if second occurance is found, immediately return False
                        return False
    return True  # everything is fine, return True


def solutionGenerator(board):
    '''
        Generates a solution for the board in question (first solution it finds)
        Args:
            board -> a sudoku matrix
        Returns:
            board -> the solved matrix
            bool -> True:  if there is a solution
                    False: if there is no solution
        NOTE: Does not account for multiple solutions, only returns the first solution it encounters.
    '''
    for r in range(0, 9):
        for c in range(0, 9):
            if board[r][c] == 0:
                for val in range(1, 10):    # row_check
                    if val not in board[r]:    # column_check
                        if val not in [board[0][c],
                                       board[1][c],
                                       board[2][c],
                                       board[3][c],
                                       board[4][c],
                                       board[5][c],
                                       board[6][c],
                                       board[7][c],
                                       board[8][c]]:
                        # box_check
                            box = [board[i][((c // 3) * 3):(((c // 3) * 3) + 3)]
                                             for i in range(((r // 3) * 3), (((r // 3) * 3) + 3))]
                            if val not in box[0] and val not in box[1] and val not in box[2]:
                                board[r][c] = val
                                if isComplete(board):
                                    return board, True
                                returned, solution_detected = solutionGenerator(board)
                                if solution_detected:
                                    return returned, True
                                else:  # backtrack
                                    board[r][c] = 0
                # When no solution is found after trying all possible values
                # for all possible cells
                return board, False


def solutionCounter(board):
    '''
        Function to check if sudoku has one solution, many solutions or no solution
        Arg:
            board -> sudoku matrix
        Returns:
            integer values:
                 1  -> one unique solution exists
                 0  -> no solution exists
                -1  -> many solutions exist
    '''
    count = 0
    for r in range(0,9):
        for c in range(0,9):
            if board[r][c]==0:
                for val in range(1,10):
                    # row_check
                    if val not in board[r]:
                        # column_check
                        if val not in [board[0][c],
                                       board[1][c],
                                       board[2][c],
                                       board[3][c],
                                       board[4][c],
                                       board[5][c],
                                       board[6][c],
                                       board[7][c],
                                       board[8][c] ]:
                            # box_check
                                box =[ board[i][((c//3)*3):(((c//3)*3)+3)] 
                                                 for i in range(((r//3)*3),(((r//3)*3)+3))]
                                if val not in box[0] and val not in box[1] and val not in box[2]:
                                    board[r][c] = val
                                    if isComplete(board):
                                        count+=1
                                    else:
                                        temp=solutionCounter(board)
                                        if(temp==-1):
                                            return -1
                                        count+=temp
                                    if(count>1):
                                       return -1
                                    # Backtrack
                                    board[r][c] = 0
                # When no solution is found after trying all possible values for all possible cells
                return count

                
def problemGenerator(k):
    '''
        Function to generate a sudoku puzzle
        Args:
            Number of clues to be removed
        Returns:
            temp -> the solution to the puzzle
            m -> the puzzle with removed values replaced with 0s
    '''
    valid = [i for i in range(1, 10)]   # a list of values from 1-9
    temp = [[0 for i in range(9)] for j in range(9)]    # an empty matrix for deep copy

    m = [[0 for i in range(9)] for j in range(9)]   # the puzzle initialized as all 0s
    while True:
        for x in [0, 3, 6]: # for all the diagonally placed sub-matrices
            random.shuffle(valid)   #shuffles all the values in the valid list
            counter = 0 #counter to track the valid list items
            for i in range(x, x+3): # for every row in the chosen sub-matrix
                for j in range(x, x+3): # for every column in the chosen sub-matrix
                    m[i][j] = valid[counter]    # set a value from the valid list to the sub-matrix's element
                    counter += 1    # move to the next element in the valid list
        for i in range(9):  # to make a deep copy of the matrix m, called temp
            for j in range(9):
                temp[i][j] = 0 + m[i][j]
        x = solutionCounter(temp)
        if x == 0:   # if no solutions exist then reset everything (although this case might never enter, not so sure)
            for i in range(9):
                for j in range(9):
                    m[i][j] = 0
            continue
        break   #solutions exist, there might be multiple, but we account for those while removing, we just need a valid set

    while not isComplete(m):    #to keep on filling while the board is empty
        for i in range(9):  #for every row in the matrix
            for j in range(9):  #for every column in the matrix
                valid = [i for i in range(1,10)]    #shuffle a list and choose one element from it at a time
                random.shuffle(valid)   
                for v in valid: #try each element until it fits (seems risky, I hope it is stable)
                    m[i][j] = v    
                    if not sudoku_valid(m): #if the sudoku becomes illegal, then set to 0
                        m[i][j] = 0
                    else:   #if not illegal, then move out of the inner loop
                        break
    for i in range(9):
        for j in range(9):
            temp[i][j] = 0 + m[i][j]
    count = 0   #to keep track of number of digits removed
    while count < k:    #while the number of digits removed is less than k 
        x = random.randint(0,8) #row of the randomly to be removed digit
        y = random.randint(0,8) #column of the randomly to be removed digit
        if m[x][y] == 0:    #if the digit is already removed, move on
            continue    
        else:   #if digit is not removed
            tempVal = m[x][y]   #store the value temporarily
            m[x][y] = 0 #set it to 0
            if solutionWrapper(m, solutionCounter) in [-1, 0]:  #check if the solution exists or multiple solutions exist
                m[x][y] = tempVal   #if yes, then just place the value back and move on
            else:   
                count += 1  #if no, then remove it, by placing 0
    return temp, m

def solutionWrapper(m, func):
    '''
        Function to make a deep copy and pass into the function, to avoid changing the matrix
        Args:
            m -> matrix to be passed into the function
            func -> solutionGenerator or solutionCounter functions
        Return:
            bool/int -> what the function passed in returns
    '''
    temp = [[0 for i in range(9)] for j in range(9)] #creation of deep copy
    for i in range(9):
        for j in range(9):
            temp[i][j] = 0 + m[i][j]
    return func(temp)   #calling the passed in function with the passed in matrix as argument

def problemGenerator(k):
    '''
        Function to generate a sudoku puzzle
        Args:
            Number of clues to be removed
        Returns:
            temp -> the solution to the puzzle
            m -> the puzzle with removed values replaced with 0s
    '''
    valid = [i for i in range(1, 10)]   # a list of values from 1-9
    temp = [[0 for i in range(9)] for j in range(9)]    # an empty matrix for deep copy

    m = [[0 for i in range(9)] for j in range(9)]   # the puzzle initialized as all 0s
    while True:
        for x in [0, 3, 6]: # for all the diagonally placed sub-matrices
            random.shuffle(valid)   #shuffles all the values in the valid list
            counter = 0 #counter to track the valid list items
            for i in range(x, x+3): # for every row in the chosen sub-matrix
                for j in range(x, x+3): # for every column in the chosen sub-matrix
                    m[i][j] = valid[counter]    # set a value from the valid list to the sub-matrix's element
                    counter += 1    # move to the next element in the valid list
        for i in range(9):  # to make a deep copy of the matrix m, called temp
            for j in range(9):
                temp[i][j] = 0 + m[i][j]
        x = solutionCounter(temp)
        if x == 0:   # if no solutions exist then reset everything (although this case might never enter, not so sure)
            for i in range(9):
                for j in range(9):
                    m[i][j] = 0
            continue
        break   #solutions exist, there might be multiple, but we account for those while removing, we just need a valid set

    while not isComplete(m):    #to keep on filling while the board is empty
        for i in range(9):  #for every row in the matrix
            for j in range(9):  #for every column in the matrix
                valid = [i for i in range(1,10)]    #shuffle a list and choose one element from it at a time
                random.shuffle(valid)   
                for v in valid: #try each element until it fits (seems risky, I hope it is stable)
                    m[i][j] = v    
                    if not sudoku_valid(m): #if the sudoku becomes illegal, then set to 0
                        m[i][j] = 0
                    else:   #if not illegal, then move out of the inner loop
                        break
    for i in range(9):
        for j in range(9):
            temp[i][j] = 0 + m[i][j]
    count = 0   #to keep track of number of digits removed
    while count < k:    #while the number of digits removed is less than k 
        x = random.randint(0,8) #row of the randomly to be removed digit
        y = random.randint(0,8) #column of the randomly to be removed digit
        if m[x][y] == 0:    #if the digit is already removed, move on
            continue    
        else:   #if digit is not removed
            tempVal = m[x][y]   #store the value temporarily
            m[x][y] = 0 #set it to 0
            if solutionWrapper(m, solutionCounter) in [-1, 0]:  #check if the solution exists or multiple solutions exist
                m[x][y] = tempVal   #if yes, then just place the value back and move on
            else:   
                count += 1  #if no, then remove it, by placing 0
    return temp, m

if __name__ == '__main__':
    
    import numpy as np
    m = np.zeros(81).reshape(9, 9)
    print(sudoku_valid(m))
