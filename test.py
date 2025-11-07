import tkinter as tk
import random
import os
import threading
import time


#values to change the board
num_rows, num_cols = 16, 16        #rows are Y and cols are X... confusing I know, thats matrices for you.
num_mines = 40

class MinesweeperBoard:
    #default constructor has a 9x9 with 10 mines, frames are mandatory as parameters
    def __init__(self, root, rows=9, cols=9, mines=10):
        #set the rows, columns, number of mines, empty spaces, and game_over
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.game_over = False
        self.empty_squares = (self.rows*self.cols)-self.mines  #this is how many spaces in the board are not mines

        #check for error case
        if self.empty_squares<1:
            raise ValueError("Number of mines cannot excede the number of empty spaces.")

        #create a copy of the root for restart button
        self.root = root
        #frame1, top frame in a grid for title, mines left, and empty spaces left in the game
        self.frame1 = tk.Frame(root, bd=10, relief=tk.SUNKEN, bg="gray")
        self.frame1.grid(row=0, column=0, sticky='ew')

        self.title_frame = tk.Frame(self.frame1, bg="gray")
        self.title_frame.pack(fill=tk.X)

        #create the restart button
        self.restart_button = tk.Button(self.title_frame, text="Restart", font=("Helvetica", 9, "bold"), command=self.restart_game)
        self.restart_button.pack(side=tk.RIGHT)
        #blanck label to make the title centered 
        self.blank_label = tk.Label(self.title_frame, text=" ", width=self.restart_button.cget("width"), bg="gray")
        self.blank_label.pack(side=tk.LEFT)

        #frame2, bottom frame in a grid to hold the game frame, formating porpuses
        self.frame2 = tk.Frame(root, bd=10, relief=tk.SUNKEN, bg="gray")
        self.frame2.grid(row=1, column=0, sticky='ew')

        #game_frame is not directly in frame2, but INSIDE in order to keep the "grid" intact so the top and bottom frame keep same width
        self.game_frame = tk.Frame(self.frame2, bd=0)
        self.game_frame.pack()
        
        #create the minesweeper title, labels for mines and empty spaces
        self.title = tk.Label(self.title_frame, text="Minesweeper", bg="gray", font=("Helvetica", 24, "bold"), foreground="white")
        self.title.pack()
        self.mines_label = tk.Label(self.frame1, text=f"Mines: {self.mines}", bg="gray", fg="white", font=("Helvetica", 12, "bold"))
        self.mines_label.pack(side=tk.LEFT)
        self.empty_spaces_label = tk.Label(self.frame1, text=f"Spaces: {self.empty_squares}", bg="gray", fg="white", font=("Helvetica", 12, "bold"))
        self.empty_spaces_label.pack(side=tk.LEFT)
      
        #create 2 empty lists full of 0s. buttons will be filled with create_buttons. 
        #solution board will change when mines are added with their numbers around.
        self.buttons = [[0 for _ in range(cols)] for _ in range(rows)]
        self.create_buttons()
        self.solution_board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.place_mines()

        #create the timer
        self.timer_label = tk.Label(self.frame1, text="Time: 0", bg="gray", fg="white", font=("Helvetica", 12, "bold"))
        self.timer_label.pack(side=tk.RIGHT)
        self.start_timer()


    #updates the text of the labels
    def update_counters(self):
        self.mines_label.config(text=f"Mines: {self.mines}")
        self.empty_spaces_label.config(text=f"Spaces: {self.empty_squares}")

    #adds all the buttons to the empty list of 0s 
    def create_buttons(self):
        for y in range(self.rows):
            for x in range(self.cols):
                #creates a button, then adds it to the list
                button = tk.Button(self.game_frame, text=" ", width=2, height=1, font=("Helvetica", 9, "bold"))
                button.grid(row=y, column=x, sticky="nw")
                button["border"] = 3
                button.bind('<Button-1>', lambda event, button=button, y=y, x=x: self.on_left_click(button, y, x))
                button.bind('<Button-3>', lambda event, button=button, y=y, x=x: self.on_right_click(button, y, x)) #y and x not needed, but for debugging
                self.buttons[y][x] = button

    #places the mins in the solution board
    def place_mines(self):
        mines_to_place = self.mines #copy counter

        while mines_to_place!=0:                          #loop that sets the mines 
            yrand = random.randint(0,self.rows-1)
            xrand = random.randint(0,self.cols-1)

            if(self.solution_board[yrand][xrand] != "x"):
                self.solution_board[yrand][xrand] = "x"
                mines_to_place -= 1
                self.MarkNumber(yrand-1, xrand-1)        #top left
                self.MarkNumber(yrand-1, xrand)          #top
                self.MarkNumber(yrand-1, xrand+1)        #top right
                self.MarkNumber(yrand, xrand-1)          #left
                self.MarkNumber(yrand, xrand+1)          #right 
                self.MarkNumber(yrand+1, xrand-1)        #bottom left
                self.MarkNumber(yrand+1, xrand)          #bottom
                self.MarkNumber(yrand+1, xrand+1)        #bottom right

    #adds 1 to the position entered if 3 conditions met
    def MarkNumber(self, y, x):
        if 0<=y<self.rows and 0<=x<self.cols and self.solution_board[y][x]!="x":
            self.solution_board[y][x] += 1

    #function for the left click scenarion of a button
    def on_left_click(self, cur_button, y, x):
        # print(f"position clicked is: {y}, {x}")

        #states to ignore the click
        if cur_button["text"]=="F" or cur_button["state"]==tk.DISABLED:
            return

        if self.solution_board[y][x] == "x":        #case 1 it's a mine, LOSE
            for y in range(self.rows):
                for x in range(self.cols):
                    #show all mines in the board as red and pushed, also disable all other buttons
                    if self.solution_board[y][x] == "x":
                        self.buttons[y][x].config(text=f"{self.solution_board[y][x]}", bg = "#DC143C", state=tk.DISABLED, relief=tk.SUNKEN)
                    else:
                        self.buttons[y][x].config(state=tk.DISABLED)
            self.game_over = True
            self.title["fg"] = "#8B0000"
            self.title["text"] = "Game Over"
        elif self.solution_board[y][x] == 0:        #case 2 it's an empty with a 0    
            self.discover_recur(y, x)
        else:                                       #case 3 it's an empty square with a number
            cur_button.config(text = self.solution_board[y][x], state=tk.DISABLED, relief=tk.SUNKEN)
            self.empty_squares -= 1

        #very important for the counters to be here
        self.update_counters()
        if self.empty_squares == 0:                 #no empty squares left, WIN
            for y in range(self.rows):
                for x in range(self.cols):
                    if self.solution_board[y][x] == "x":
                        self.buttons[y][x].config(text=f"{self.solution_board[y][x]}", bg = "#7CFC00", state=tk.DISABLED)
            self.game_over = True
            self.title["fg"] = "#7CFC00"
            self.title["text"] = "You Won!"

    #function for flagging.
    def on_right_click(self, cur_button, y, x):
        # print(f"position clicked is: {y}, {x}")
        #states to ignore the click
        if self.game_over==True or cur_button["relief"]==tk.SUNKEN:
            return
        #if not flagged then do it otherwise unflag it
        if cur_button["text"] == " ":
            cur_button.config(text="F", state=tk.DISABLED)
            self.mines -= 1
        elif cur_button["text"] == "F":
            cur_button.config(text=" ", state=tk.ACTIVE)
            self.mines += 1
        #update the counters because of the flags
        self.update_counters()

    #recursive function that checks wether it has a 0, if so it openst it and calls recursion for the ones around it
    def discover_recur(self, y, x):
        if 0<=y<self.rows and 0<=x<self.cols and self.solution_board[y][x]!="x" and self.buttons[y][x].cget("state") == tk.NORMAL:
            self.buttons[y][x].config(state=tk.DISABLED, relief=tk.SUNKEN)
            self.empty_squares -= 1
            if 0<self.solution_board[y][x]<9:
                self.buttons[y][x]["text"] = self.solution_board[y][x]
            elif self.solution_board[y][x]==0:
                self.buttons[y][x]["text"] = " "
                self.discover_recur(y-1, x-1)        #top left
                self.discover_recur(y-1, x)          #top
                self.discover_recur(y-1, x+1)        #top right
                self.discover_recur(y, x-1)          #left
                self.discover_recur(y, x+1)          #right
                self.discover_recur(y+1, x-1)        #bottom left
                self.discover_recur(y+1, x)          #bottom
                self.discover_recur(y+1, x+1)        #bottom right

    #function that starts the timer
    def start_timer(self):
        self.start_time = time.time()
        self.timer_thread = threading.Thread(target=self.update_timer)
        self.timer_thread.daemon = True
        self.timer_thread.start()

    #function that updates the timer
    def update_timer(self):
        while not self.game_over:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed_time}")
            time.sleep(1)

    #function that restarts the game
    def restart_game(self):
        for widget in self.game_frame.winfo_children():
            widget.destroy() # Destroy the widgets inside the game frame
        self.game_over = False # Reset the game_over flag
        self.__init__(self.root, num_rows, num_cols, num_mines) # Reinitialize the game
        self.start_timer() # Restart the timer

#Create a Tkinter window
root = tk.Tk()
if os.path.exists("mine.ico"):  #attempts to add the icon to the window
    root.iconbitmap("mine.ico")

root.title("Minesweeper Game")
root.configure(background="gray")

#create the board with game_frame as interactive frame
board = MinesweeperBoard(root, num_rows, num_cols, num_mines)

root.mainloop()