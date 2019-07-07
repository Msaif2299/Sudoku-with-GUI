import tkinter as tk
from collections import defaultdict
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
	for r in range(0,9):
		for c in range(0,9):
			if board[r][c] == 0:	#Any empty cell found
				return False
	return True		#No empty cells found i.e board is completely filled
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
	for i in range(9):	#row and column checking loop (if there are only one occurance of 1-9 digits in eveyr row)
		d = defaultdict(int)	#to map all the values into the dictionary
		for x in m[i]:	#iteration over every element in given row
			if x == 0:	#ignoring 0 (check NOTE why)
				continue
			d[x] += 1	#counting number of occurances
			if d[x] > 1:	#if a second occurance is found, immediately return False
				return False
		d = defaultdict(int)	#to map all values into the dictionary
		for x in m[:][i]:	#iteration over every element in given column
			if x == 0:	#ignoring 0 (check NOTE why)
				continue	
			d[x] += 1	#counting number of occurances
			if d[x] > 1:	#if a second occurance is found, immediately return False
				return False
	for i in [0, 3, 6]:	#loop to check all the subgrids in the sudoku puzzle, the 3x3 ones
		for j in [0, 3, 6]:	#every subgrid is represented by i, j similar to a matrix
			d = defaultdict(int)	#to map all the values in the subgrid into the dictionary
			for x in range(i, i+3):	#iterating the rows in the subgrid
				for y in range(j, j+3):	#iterating the columns in the subgrid
					if m[x][y] == 0:	#ignoring 0 (see NOTE why)
						continue	
					d[m[x][y]] += 1	#counting number of occurances
					if d[m[x][y]] > 1:	#if second occurance is found, immediately return False
						return False
	return True	#everything is fine, return True

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
	for r in range(0,9):
		for c in range(0,9):
 			if board[r][c] == 0:
 				for val in range(1,10):	#row_check
					if val not in board[r]:	#column_check
						if val not in [board[0][c],board[1][c],board[2][c],board[3][c],board[4][c],board[5][c],board[6][c],board[7][c],board[8][c] ]:
                        #box_check
                        	box = [ board[i][((c//3)*3):(((c//3)*3)+3)] for i in range(((r//3)*3),(((r//3)*3)+3))]
								if val not in box[0] and val not in box[1] and val not in box[2]:
									board[r][c] = val
									if isComplete(board):
										return board, True
									returned, solution_detected = bruteForce(board)
									if solution_detected:
										return returned, True
									else:	#backtrack
										board[r][c] = 0
                #When no solution is found after trying all possible values for all possible cells
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
				-1	-> many solutions exist
	'''
    count = 0
    for r in range(0,9):
        for c in range(0,9):
            if board[r][c]==0:
                for val in range(1,10):
                    #row_check
                    if val not in board[r]:
                        #column_check
                        if val not in [board[0][c],board[1][c],board[2][c],board[3][c],board[4][c],board[5][c],board[6][c],board[7][c],board[8][c] ]:
                            #box_check
                                box =[ board[i][((c//3)*3):(((c//3)*3)+3)] for i in range(((r//3)*3),(((r//3)*3)+3))]
                                if val not in box[0] and val not in box[1] and val not in box[2]:
                                    board[r][c] = val
                                    if isComplete(board):
                                        count+=1
                                    else:
                                        temp=bruteForce(board)
                                        if(temp==-1):
                                            return -1
                                        count+=temp
                                    if(count>1):
                                       return -1
                                    #Backtrack
                                    board[r][c] = 0
                #When no solution is found after trying all possible values for all possible cells
                return count

if __name__ == '__main__':
	
	import numpy as np
	m = np.zeros(81).reshape(9, 9)
	print(sudoku_valid(m))
