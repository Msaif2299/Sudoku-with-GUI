import tkinter as tk
from collections import defaultdict
import random
'''---------------------------------Utility Functions---------------------------------------------'''
def customMatrixReturner(buttonList):
    '''
        Function to return only the values of the displayed matrix that are disabled
        Args:
            buttonList -> 2D matrix of buttonGrid() objects
        Returns:
            m -> matrix with the values of the labels of the buttons
    '''
    m = [[0 for i in range(9)] for j in range(9)]   #initialize the matrix
    for i in range(9):  #iterate over every button
        for j in range(9):
            if buttonList[i][j].button['state'] == 'disabled':  #write the value of the button 
                m[i][j] = int(buttonList[i][j].button['text'])  #if it is disabled
            else:
                m[i][j] = 0 #if it is enabled, then just write 0
    return m         #returns the matrix

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
            if buttonList[i][j].button['text'] == ' ':
                m[i][j] = 0
                continue
            m[i][j] = int(buttonList[i][j].button['text'])
    return m

def setMatrix(m, buttonList):
    '''
        Function to set the values from the given matrix to the buttonList
        Args:
            m          -> matrix to be set
            buttonList -> the list of buttons to set
    '''
    for i in range(9):
        for j in range(9):
            if m[i][j] == 0:
                buttonList[i][j].button.configure(text = ' ')
                buttonList[i][j].button.configure(state='normal')   #enable the changable buttons
            else:
                buttonList[i][j].button.configure(text = str(m[i][j]))
                buttonList[i][j].button.configure(state='disabled') #prevent change to the question

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


def elementValid(x,y,m):
    '''
        Function that checks if the element is valid or not, by checking its 
        uniqueness in the column and row and sub-matrix
        Args:
            x -> the row number of the element
            y -> the column number of the element
            m -> matrix where this element is to be checked
        Returns:
            bool -> True:   if it is valid, i.e. unique in its row, column and sub-matrix
                    False:  if it is invalid, and a duplicate exists
    '''
    element = m[x][y]   #just take the element
    if m[x].count(element) > 1: #count the element's occurence in its row
        return False    #if its more than 1, then return False
    col = [m[i][y] for i in range(9)]   #turn the column into a list
    if col.count(element) > 1:  #count the element's occurence in its column
        return False    #if its more than 1, then return False
    subX, subY = 0, 0   #to find the sub-matrix the element lies in
    for sx in [0, 3, 6]:    #find the x coordinate of the sub-matrix
        if sx <= subX and sx+3 > subX:
            subX = sx
    for sy in [0, 3, 6]:    #find the y coordinate of the sub-matrix
        if sy <= subY and sy+3 > subY:
            subY = sy
    d = defaultdict(int)    #make a default dictionary
    for sx in range(subX, subX+3):  #iterating over all the elements in the sub-matrix
        for sy in range(subY, subY+3):
            if m[sx][sy] == 0:  #ignore if it is 0
                continue
            d[m[sx][sy]] += 1   #increment its count in the dictionary
            if d[m[sx][sy]] > 1:    #if it's count is more than 0, then return False
                return False
    return True #means it is unique, so, return True


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
    for i in range(9):  # row and column checking loop (if there are only one occurance of 1-9 digits in eveyr row)
        d = defaultdict(int)  # to map all the values into the dictionary
        for x in m[i]:  # iteration over every element in given row
            if x == 0:  # ignoring 0 (check NOTE why)
                continue
            d[x] += 1  # counting number of occurances
            if d[x] > 1:  # if a second occurance is found, immediately return False
                return False
        d = defaultdict(int)  # to map all values into the dictionary
        colset = [m[row][i] for row in range(0,9)] 
        for x in colset:  # iteration over every element in given column
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
        Generates a random solution for the board in question (first solution it finds)
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
                valid = [i for i in range(1,10)]    #shuffle a list and choose one element from it at a time
                random.shuffle(valid)  
                for val in valid:    # row_check
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

    m,unnecessary = solutionGenerator(m) #unnecessary will always be True as previous loop assures a solvable matrix m
    for i in range(9):
        for j in range(9):
            temp[i][j] = 0 + m[i][j]
    parsed = [[0 for i in range(9)] for j in range(9)]    # an empty matrix to keep track of digits which have already been checked
    flag = 0
    count = 0   #to keep track of number of digits removed
    while count < k:    #while the number of digits removed is less than k (and less than 52)
        x = random.randint(0,8) #row of the randomly to be removed digit
        y = random.randint(0,8) #column of the randomly to be removed digit
        if m[x][y] == 0 or parsed[x][y] == 1:    #if the digit is already removed, move on
            flag+=1
            continue    
        else:   #if digit is not removed
            tempVal = m[x][y]   #store the value temporarily
            m[x][y] = 0 #set it to 0
            parsed[x][y] = 1
            if solutionWrapper(m, solutionCounter) in [-1, 0]:  #check if the solution exists or multiple solutions exist
                m[x][y] = tempVal   #if yes, then just place the value back mark it as checked and move on
                flag+=1
                if(flag > 81): #to prevent an infinite loop when further removal of digits is not possible
                    break
            else:   
                count += 1  #if no, then remove it, by placing 0
                if(count >= 52): #set as limiter as solutionCounter performs really slowly beyond this value on average
                    break
                flag = 0    #reset flag since one removal happened
    return temp, m

if __name__ == '__main__':
    
    import numpy as np
    m = np.zeros(81).reshape(9, 9)
    print(sudoku_valid(m))
