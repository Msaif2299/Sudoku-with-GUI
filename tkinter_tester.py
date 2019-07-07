import tkinter as tk
from sudoku_runner import matrix
'''--------------------------------------Utility Functions----------------------------------------'''
def framer(i, j, frameList):
	'''
		Function to choose the correct frame for the buttons
		Args:
			i -> row of the button in the grid
			j -> column of the button in the grid
			frameList -> list of frames to choose from
		Returns:
			frameList[_][_], an item from the list of frames
	'''
	val = i*9+j+1	#calculation of the button number. Frames will be assigned on this basis
	if val in [1, 2, 3, 10, 11, 12, 19, 20, 21]:
		return frameList[0][0]
	elif val in [4, 5, 6, 13, 14, 15, 22, 23, 24]:
		return frameList[1][0]
	elif val in [7, 8, 9, 16, 17, 18, 25, 26, 27]:
		return frameList[2][0]
	elif val in [28, 29, 30, 37, 38, 39, 46, 47, 48]:
		return frameList[0][1]
	elif val in [31, 32, 33, 40, 41, 42, 49, 50, 51]:
		return frameList[1][1]
	elif val in [34, 35, 36, 43, 44, 45, 52, 53, 54]:
		return frameList[2][1]
	elif val in [55, 56, 57, 64, 65, 66, 73, 74, 75]:
		return frameList[0][2]
	elif val in [58, 59, 60, 67, 68, 69, 76, 77, 78]:
		return frameList[1][2]
	else:
		return frameList[2][2]
'''--------------------------------------Class Definitions--------------------------------------'''
class buttonGrid():
	'''
		Class to create buttons for the grid of buttons on display
		Args:
			master -> the frame which the button will be a part of
			row    -> row of the button in the grid
			col    -> column of the button in the grid
			data   -> initial text in the label of the button
	'''
	def __init__(self, master, row, col, data):
		self.row = row
		self.col = col
		self.button = tk.Button(master, bg = "white", width = 10, height = 5 , text = data, borderwidth = 2)
		self.button.grid(row = self.row, column = self.col, padx = 0, pady = 0)

'''---------------------------------------------------------------------------------------------'''
if __name__ == '__main__':
	main = tk.Tk()					#create the main app
	main.title('Sudoku')			#set title to 'Sudoku'
	buttonFrame = tk.Frame(main, bg = 'black')	#create frame to pack the other frames into
	buttonFrame.pack()				#pack the frame
	frameList = [[None for i in range(3)] for j in range(3)] 	#create the list of frames
	buttonList = [[None for i in range(9)] for j in range(9)]	#create the list of buttons
	for i in range(3):	#frame creation loop, 3x3 frames created
		for j in range(3):
			frame = tk.Frame(buttonFrame, highlightbackground="black", highlightcolor="black", highlightthickness=2)
			frame.grid(column = i, row = j)	#setting of frame
			frameList[i][j] = frame #setting the created frame into the list
	for i in range(9):	#button creation loop, 9x9 buttons are created
		for j in range(9):
			buttonList[i][j] = buttonGrid(framer(i, j, frameList), i, j, f"{i*9+j+1}") #the f-string is just to tell the button number on display

	main.mainloop()	#the main loop