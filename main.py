import tkinter as tk
from background import *
from tkinter import font, messagebox, filedialog
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
    val = i*9+j+1   #calculation of the button number. Frames will be assigned on this basis
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


def check():
    '''
        Function to check the sudoku instantly (Maybe pointless, but might help in case something
            goes wrong)
        Args:
            None
        Returns:
            None
    '''
    if isComplete(matrix(buttonList)) and sudoku_valid(matrix(buttonList)):
            msg = tk.messagebox.askquestion("Solved", "You Win! \n Would you like to continue?")
            if msg == 'yes':    #same as completing the sudoku puzzle successfully
                sol, puzzle = problemGenerator(25)
                setMatrix(puzzle, buttonList)
            else:
                main.destroy()
    else:   #in case it is not complete and valid
        messagebox.showinfo("Invalid", "Your solution is invalid!")

def load():
    filename = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("All Files", '*.*')))
    m = []
    try:
        file = open(filename, 'r')
        temp = file.read().splitlines()
        for line in temp:
            m.append(list(map(int, list(line))))
        setMatrix(m, buttonList)
    except FileNotFoundError as e:
        messagebox.showinfo('File Not Found', "File has either been moved, or does not exist.")

def saveHelperFunc(m, title):
    file = filedialog.asksaveasfile(mode='w', defaultextension='.txt', title=title)
    if file is None:
        return
    text = ''
    for i in range(9):
        text += ''.join(list(map(str, m[i]))) + '\n'
    file.write(text)
    file.close()

def solutionChecker():
    values = solutionGenerator(matrix(buttonList))
    if values is None:
        messagebox.showinfo('Unexpected solution', 'The file you are trying to save is a solution, or cannot be solved due to it not having any spaces left. Please use the File saving option instead.')
        return None
    return values[0]

def save():
    saveHelperFunc(matrix(buttonList), 'Save puzzle as')

def solve():
    val = solutionGenerator(matrix(buttonList))
    if val is None:
        messagebox.showinfo('Unexpected solution', 'The puzzle you are trying to solve is either already solved, or has no spaces left to solve. Please load another puzzle or start a new game.')
        return
    setMatrix(val[0], buttonList)

def new():
    sol, puzzle = problemGenerator(25)
    setMatrix(puzzle, buttonList)

def saveSol():
    solution = solutionChecker()
    if solution is None:
        return
    saveHelperFunc(solution, 'Save solution as')

def saveAndSol():
    solution = solutionChecker()
    if solution is None:
        return
    saveHelperFunc(solution, 'Save solution as')
    setMatrix(solution, buttonList)

def saveFileAndSol():
    solution = solutionChecker()
    if solution is None:
        return
    file = filedialog.asksaveasfile(mode='w', defaultextension='.txt', title='Save file and solution')
    if file is None:
        return
    text = ''
    m = matrix(buttonList)
    for i in range(9):
        text += ''.join(list(map(str, m[i]))) + '\n'
    file.write(text)
    filename = file.name.split('.')[0]
    file.close()
    file = open(filename + '(solution).txt', 'w')
    if file is None:
        return
    text = ''
    for i in range(9):
        text += ''.join(list(map(str, solution[i]))) + '\n'
    file.write(text)
    file.close()

def loader(event):
    load()

def saver(event):
    save()

def checker(event):
    '''
        Function to allow the bind() function to use check(), because it needs the 'event' parameter
    '''
    check()


def destroy(event):
    '''
        Function to allow the bind() function to use main.destroy(), because it needs the 
        'event parameter'
    '''
    main.destroy()

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
        self.button = tk.Button(master, bg = "white", width = 10, height = 5 , text = data, borderwidth = 2, command = self.press)
        self.button.grid(row = self.row, column = self.col, padx = 0, pady = 0)

    def press(self):
        '''
            Function to occur on the button press
            Args:
                self -> the object, no need to pass anything
            Description:
                Checks if the value cycled to is valid, if yes, change its color to Blue, else Red
                Checks if the board is complete and valid:
                    -> if yes then generate a dialog box
                        => box asks to repeat the game:
                            --> if yes, then generate a new puzzle and close the box
                            --> if no, then exit
                    -> if no, then do nothing

        '''
        if self.button['text'] == ' ':  #if there is nothing and its been clicked, set it to 1
            self.button.config(text = str(1))
        else:
            self.button.config(text = str(((int(self.button['text']))%9)+1))    #else cycle through 1-9
        if sudoku_valid(matrix(buttonList)): #set to blue if the number is valid
            self.button.configure(fg='blue')
        else:
            self.button.configure(fg='red') #set to red if invalid
        if isComplete(matrix(buttonList)) and sudoku_valid(matrix(buttonList)): #game finishing conditions
            msg = tk.messagebox.askquestion("Solved", "You Win! \n Would you like to continue?")
            if msg == 'yes':    #generates the new puzzle
                sol, puzzle = problemGenerator(25)
                setMatrix(puzzle, buttonList)
            else:   #exits
                main.destroy()


'''---------------------------------------------------------------------------------------------'''
if __name__ == '__main__':
    main = tk.Tk()                  #create the main app
    main.title('Sudoku')            #set title to 'Sudoku'
    buttonFrame = tk.Frame(main, bg = 'black')  #create frame to pack the other frames into
    buttonFrame.pack()              #pack the frame
    frameList = [[None for i in range(3)] for j in range(3)]    #create the list of frames
    buttonList = [[None for i in range(9)] for j in range(9)]   #create the list of buttons
    for i in range(3):  #frame creation loop, 3x3 frames created
        for j in range(3):
            frame = tk.Frame(buttonFrame, highlightbackground="black", highlightcolor="black", highlightthickness=2)
            frame.grid(column = i, row = j) #setting of frame
            frameList[i][j] = frame #setting the created frame into the list
    for i in range(9):  #button creation loop, 9x9 buttons are created
        for j in range(9):
            buttonList[i][j] = buttonGrid(framer(i, j, frameList), i, j, ' ') #the f-string is just to tell the button number on display
    menu = tk.Menu(main, tearoff = False)
    main.config(menu = menu)
    fileOptions = tk.Menu(menu, tearoff=False)
    openOptions = tk.Menu(fileOptions, tearoff=False)
    fileOptions.add_command(label = 'Open file', command = load, accelerator="Ctrl+O")
    saveOptions = tk.Menu(fileOptions, tearoff=False)
    fileOptions.add_cascade(label='Save ', menu = saveOptions)
    saveOptions.add_command(label = 'Save file', command = save, accelerator="Ctrl+S")
    saveOptions.add_command(label = 'Save solution', command = saveSol)
    saveOptions.add_command(label = 'Save and load solution', command = saveAndSol)
    saveOptions.add_command(label = 'Save file and solution', command = saveFileAndSol)
    sudokuOptions = tk.Menu(menu, tearoff = False)
    sudokuOptions.add_command(label = 'New', command = new)
    sudokuOptions.add_command(label = 'Check', command = check, accelerator="Ctrl+Q")
    sudokuOptions.add_command(label = 'Solve', command = solve)
    sudokuOptions.add_command(label = 'Exit', command = main.destroy, accelerator="Ctrl+E")
    menu.add_cascade(label='File', menu=fileOptions)
    menu.add_cascade(label = 'Options', menu=sudokuOptions)
    main.bind_all("<Control-q>", checker)
    main.bind_all("<Control-e>", destroy)
    main.bind_all("<Control-s>", saver)
    main.bind_all("<Control-o>", loader)
    sol, puzzle = problemGenerator(25)
    setMatrix(puzzle, buttonList)
    main.mainloop() #the main loop
