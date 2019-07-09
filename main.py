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

def savePuzzleState():
    '''
        Function to save the state of the puzzle
    '''
    file = filedialog.asksaveasfile(mode='w', defaultextension='(state_save).txt', title='Save game state')
    if file is None:    #ask user to save file
        return      #if user cancels, exit
    text = ''   #text to write into file
    m = matrix(buttonList)  #get the entire displayed matrix
    states = [[0 for i in range(9)] for j in range(9)]  #create a matrix to hold the states
    for i in range(9):  #iterate over every button
        for j in range(9):
            if buttonList[i][j].button['state'] == 'disabled':  #if it is disabled, set it to '2'
                states[i][j] = 2
            else:   #if it is enabled
                if buttonList[i][j].button['fg'] == 'red':  #if it is red, set it to '0'
                    states[i][j] = 0
                else:   #if it is blue, set it to '1'
                    states[i][j] = 1
    for i in range(9):  #first 9 lines, is the matrix 'm'
        text += ''.join(list(map(str, m[i]))) + '\n'
    for i in range(9):  #the next 9 lines are the matrix 'state'
        text += ''.join(list(map(str, states[i]))) + '\n'
    file.write(text)    #write the text to the file
    file.close()    #close the file

def loadPuzzleState():
    '''
        Function to load a save puzzle state
    '''
    filename = filedialog.askopenfilename(filetypes=(("Puzzle state files", "*.(state_save).txt"), ("All Files", "*.*")))
    if filename is None:    #open a file through Open File Dialog
        return      #if user cancels, exit
    m, states = [], []  #make two matrices, one being the display, the other to set the states of the buttons representing the values
    try:
        file = open(filename, 'r')  #open the file
        temp = file.read().splitlines() #read all the lines
        for line in temp[:9]:   #read the first 9 lines 
            m.append(list(map(int, list(line))))    #write them to the matrix 'm'
        setMatrix(m, buttonList)    #display the matrix m
        for line in temp[9:]:   #read the next 9 lines
            states.append(list(map(int, list(line))))   #write them to the matrix 'states'
        for i in range(9):  #iterate over every button in buttonList
            for j in range(9):
                if states[i][j] == 2:   #2 represents the 'disabled' states
                    buttonList[i][j].button.configure(state='disabled') #set the state accordingly
                else:   #if not 2, then that means that they are enabled
                    buttonList[i][j].button.configure(state = 'normal') #set them to the normal state
                    if states[i][j] == 1:   #1 represents the blue marked values during the save
                        buttonList[i][j].button.configure(fg='blue')    #set their color to blue
                    else:   #0 represents the red marked values during the save
                        buttonList[i][j].button.configure(fg='red') #set their color to red
    except FileNotFoundError as e:  #if file is not found
        messagebox.showinfo('File Not Found', "File has either been moved, or does not exist.")
    except Exception as e:  #if it is some random text file
        messagebox.showinfo('Format error','Wrong data format is stored in the selected file. Please select a different one.')


def load():
    '''
        Function to load a file into the the display
    '''
    filename = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("All Files", '*.*')))    #ask to open file
    if filename is None:    #user cancels the dialog box
        return
    m = []  #initialize the empty matrix, purpose: to write this matrix into the display
    try:    #capturing exceptions accordingly
        file = open(filename, 'r')    #open the file
        temp = file.read().splitlines()[:9] #read only the first 9 lines, because of the existence of 'state_save files', which are composed of 18 lines
        for line in temp:   #append every line from file into the matrix
            m.append(list(map(int, list(line))))
        setMatrix(m, buttonList)    #display the matrix
    except FileNotFoundError as e:  #if file is not found
        messagebox.showinfo('File Not Found', "File has either been moved, or does not exist.")
    except Exception as e:  #if some random text file is read instead
        messagebox.showinfo('Wrong data format is stored in the selected file. Please select a different one.')

def saveHelperFunc(m, title):
    '''
        Function to prevent repetition of code to save a file
        Args:
            m     -> 2D matrix to save
            title -> title of the Save File Dialog box
    '''
    file = filedialog.asksaveasfile(mode='w', defaultextension='.txt', title=title) #save as file dialog
    if file is None:    #if user cancels the dialog box
        return
    text = ''   #text to write into the file
    for i in range(9):  #writing the matrix into 'text'
        text += ''.join(list(map(str, m[i]))) + '\n'
    file.write(text)    #writing the text into the file
    file.close()    #close file

def solutionChecker():
    '''
        Function to check if the solution for the given problem exists or not, without displaying the solution
        Returns:
            None -> 1) Attempting to solve a solution
                    2) Attempting to solve a puzzle that doesn't follow the rules of sudoku puzzle problems
                    3) Attempting to solve a puzzle with no solutions
            values[0] -> a 2D matrix, composed of the solution to the given puzzle (first solution if multiple solutions)
    '''
    values = solutionGenerator(customMatrixReturner(buttonList))    #generate a solution
    if values is None:  #solving a solution issue
        messagebox.showinfo('Unexpected solution', 'The file you are trying to save is a solution, or cannot be solved due to it not having any spaces left. Please use the File saving option instead.')
        return None
    if not sudoku_valid(matrix(buttonList)):    #solving an invalid solution issue
        messagebox.showinfo('Wrong puzzle', 'This is an invalid puzzle. Please try another puzzle.')
        return None
    x = solutionCounter(customMatrixReturner(buttonList))
    if x == 0:  #solving a puzzle with no solutions issue
        messagebox.showinfo('Wrong puzzle', 'This is an invalid puzzle. It has no solutions. Please try another puzzle.')
        return None
    if x == -1: #solving a puzzle with multiple solutions, just solve for the first solution
        messagebox.showinfo('Multiple solutions', 'This puzzle has multiple solutions. Only the first solution will be shown.')
    return values[0]

def save():
    '''
        Function to save a file
    '''
    saveHelperFunc(customMatrixReturner(buttonList), 'Save puzzle as')  #call the helper function to save

def solve():
    '''
        Function to solve the given puzzle and display the solution
        Returns:
            None -> 1) Attempting to solve a solution
                    2) Attempting a puzzle which does not follow the rules of sudoku puzzle problems
                    3) Attempting to solve a puzzle with no solutions
            val[0] -> a 2D matrix composed of the solution of the puzzle given (first solution only if multiple solutions)
    '''
    val = solutionGenerator(customMatrixReturner(buttonList)) #generates the solution from the disabled values only
    if val is None: #solved solution issue
        messagebox.showinfo('Unexpected solution', 'The puzzle you are trying to solve is either already solved, or has no spaces left to solve. Please load another puzzle or start a new game.')
        return None 
    if not sudoku_valid(matrix(buttonList)):    #invalid solution puzzle issue
        messagebox.showinfo('Wrong puzzle', 'This is an invalid puzzle. Please try another puzzle.')
        return None
    x = solutionCounter(customMatrixReturner(buttonList))   #count number of solutions
    if x == 0:  #no solution issue
        messagebox.showinfo('Wrong puzzle', 'This is an invalid puzzle. It has no solutions. Please try another puzzle.')
        return None
    if x == -1: #multiple solutions, only the first solution will be taken
        messagebox.showinfo('Multiple solutions', 'This puzzle has multiple solutions. Only the first solution will be shown.')
    setMatrix(val[0], buttonList)   #display the solution
    return val[0]   #return the solution

def easy():
    '''
        Function to generate an 'easy' puzzle
    '''
    sol, puzzle = problemGenerator(25)  #removes only 25 values at max
    setMatrix(puzzle, buttonList)

def medium():
    '''
        Function to generate a 'medium' sudoku puzzle
    '''
    sol, puzzle = problemGenerator(35)  #removes only 35 values at max
    setMatrix(puzzle, buttonList)

def hard():
    '''
        Function to generate a 'hard' sudoku puzzle
    '''
    sol, puzzle = problemGenerator(81)#Remove as many digits as possible
    setMatrix(puzzle, buttonList)

def saveSol():
    '''
        Function to save the solution. But not display it.
        Returns:
            -1 -> when solving is not possible
    '''
    solution = solutionChecker() #check if solution exists
    if solution is None:    #if no, exit
        return -1
    saveHelperFunc(solution, 'Save solution as')    #if yes, save the solution

def saveAndSol():
    '''
        Function to save the solution of the puzzle. Display the solution also.
        Returns:
            -1 -> when solving is not possible
    '''
    solution = solve()  #check if it is possible to solve
    if solution is None:    #if no, then exit
        return -1
    saveHelperFunc(solution, 'Save solution as')    #if yes, save the solution

def saveFileAndSol():
    '''
        Function to save the puzzle as a file and its solution as another file with '(solution)'
        attached to it.
        Returns:
            -1 -> when an exception occurs
    '''
    solution = solutionChecker()    #check if the solution exists if, yes, then move on
    if solution is None:    #if no, then exit
        return -1
    file = filedialog.asksaveasfile(mode='w', defaultextension='.txt', title='Save file and solution')
    if file is None:    #in case the user cancels the save file dialog
        return -1
    text = ''   #string to write into the file
    m = customMatrixReturner(buttonList)    #gets all the values from the buttons whose 'state' is 'disabled'
    for i in range(9):  #adding their values into the string, and ending with a newline character
        text += ''.join(list(map(str, m[i]))) + '\n'
    file.write(text)    #writing into the file
    filename = file.name.split('.')[0]  #takes the name, and takes the name, without the extension
    file.close()    #close file
    try:   
        file = open(filename + '(solution).txt', 'w')   #make the solution file
    except Exception as e:  #if exception is raised, show message and exit
        messagebox.showinfo("Solution file creation error", "Error occured during making of solution file.\n" + str(e) + "\nOn the bright side, the puzzle file has been created.")
        return -1
    text = ''   #text to write into solution file
    for i in range(9):  #writing of solution matrix
        text += ''.join(list(map(str, solution[i]))) + '\n'
    file.write(text)
    file.close()    #close solution file

def loader(event):
    '''
        Function to allow the bind() function to use load(), because it needs the 'event' parameter
    '''
    load()

def saver(event):
    '''
        Function to allow the bind() function to use save(), because it needs the 'event' parameter
    '''
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
        self.button = tk.Button(master, bg = "white" , text = data, width = 10,height = 5,borderwidth = 2, command = self.press)
        self.button.grid(row = self.row, column = self.col, padx = 0, pady = 0,sticky = tk.N+tk.E+tk.W+tk.S) #sticky to make button stick along as many edges of parent as possible
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
        elif self.button['text'] == '9':    #if it is 9, empty it and return, as we don't have any use for checking it
            self.button.config(text = ' ')
            return
        else:
            self.button.config(text = str(((int(self.button['text']))%9)+1))    #else cycle through 1-9
        if elementValid(self.row, self.col, matrix(buttonList)): #set to blue if the number is valid
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
    main = tk.Tk()#create the main app
    main.maxsize(750,750) #set max size of window to prevent case of empty frame
    main.minsize(200,200) #set min size of window to prevent grid being too small
    main.title('Sudoku')            #set title to 'Sudoku'
    buttonFrame = tk.Frame(main, bg = 'black')  #create frame to pack the other frames into
    buttonFrame.pack(fill = tk.BOTH , expand = tk.YES)#pack the frame
    for i in range(3): #setting row and column configuration to resizable in buttonFrame
        tk.Grid.rowconfigure(buttonFrame, i, weight=1)
        tk.Grid.columnconfigure(buttonFrame, i, weight=1)
    frameList = [[None for i in range(3)] for j in range(3)]    #create the list of frames
    buttonList = [[None for i in range(9)] for j in range(9)]   #create the list of buttons
    for i in range(3):  #frame creation loop, 3x3 frames created
        for j in range(3):
            frame = tk.Frame(buttonFrame, highlightbackground="black", highlightcolor="black", highlightthickness=2)
            for k in range(9): #setting row and column configuration to resizable in frame
                tk.Grid.rowconfigure(frame, k, weight=1)
                tk.Grid.columnconfigure(frame, k, weight=1)
            frame.grid(column = i, row = j,sticky = tk.N+tk.E+tk.W+tk.S) #setting of frame and making it stick to edges of buttonFrame
            frameList[i][j] = frame #setting the created frame into the list
    for i in range(9):  #button creation loop, 9x9 buttons are created
        for j in range(9):
            buttonList[i][j] = buttonGrid(framer(i, j, frameList), i, j, ' ') #the f-string is just to tell the button number on display
    menu = tk.Menu(main, tearoff = False) #menu creation
    main.config(menu = menu)
    fileOptions = tk.Menu(menu, tearoff=False)
    openOptions = tk.Menu(fileOptions, tearoff=False)
    saveOptions = tk.Menu(fileOptions, tearoff=False)
    openOptions = tk.Menu(fileOptions, tearoff=False)
    openOptions.add_command(label = 'Load file', command = load, accelerator="Ctrl+O")
    openOptions.add_command(label = 'Load puzzle state', command = loadPuzzleState)
    fileOptions.add_cascade(label='Load', menu = openOptions)
    fileOptions.add_cascade(label='Save ', menu = saveOptions)
    saveOptions.add_command(label = 'Save puzzle', command = save, accelerator="Ctrl+S")
    saveOptions.add_command(label = 'Save puzzle state', command = savePuzzleState)
    saveOptions.add_command(label = 'Save solution', command = saveSol)
    saveOptions.add_command(label = 'Save and load solution', command = saveAndSol)
    saveOptions.add_command(label = 'Save file and solution', command = saveFileAndSol)
    sudokuOptions = tk.Menu(menu, tearoff = False)
    sudokuOptions.add_command(label = 'Check', command = check, accelerator="Ctrl+Q")
    sudokuOptions.add_command(label = 'Solve', command = solve)
    sudokuOptions.add_command(label = 'Exit', command = main.destroy, accelerator="Ctrl+E")
    newOptions = tk.Menu(menu, tearoff = False)
    newOptions.add_command(label = 'Easy', command = easy)
    newOptions.add_command(label = 'Medium', command = medium)
    newOptions.add_command(label = 'Hard', command = hard)
    menu.add_cascade(label='File', menu=fileOptions)
    menu.add_cascade(label = 'Options', menu=sudokuOptions)
    menu.add_cascade(label = 'New Game', menu=newOptions)   #menu creation end
    main.bind_all("<Control-q>", checker)   #event binding
    main.bind_all("<Control-e>", destroy)
    main.bind_all("<Control-s>", saver)
    main.bind_all("<Control-o>", loader)    #event binding ends
    sol, puzzle = problemGenerator(25)  #starts off with an easy puzzle
    setMatrix(puzzle, buttonList)
    main.mainloop() #the main loop
