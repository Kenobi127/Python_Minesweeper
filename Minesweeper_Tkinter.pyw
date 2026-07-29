#tkinter_minesweeper.py 
#author: Mateo Lopez Moncaleano 
#this program implements the logic from minesweeper and the GUI from tkinter to make it complete 

import os 
import tkinter as tk 
import random 
import time 

script_dir = os.path.dirname(os.path.abspath(__file__)) 
#board size and mines 
num_rows, num_cols = 16, 16 
num_mines = 40 

class MinesweeperBoard: 
    def __init__(self, root, rows=9, cols=9, mines=10): 
        self.rows = rows 
        self.cols = cols 
        self.initial_mines = mines 
        self.mines = mines 
        self.game_over = False 
        self.timer_job = None #create loop tracker variable for reset handling
        self.empty_squares = (self.rows * self.cols) - self.mines 
        
        if self.empty_squares < 1: 
            raise ValueError("Number of mines cannot exceed the number of empty spaces.") 
            
        self.root = root 
        self.img_size = tk.PhotoImage(width=20, height=20) #placeholder empty image trick to set an exact button size 

        #colored numbers like the original game
        self.colors = {
            1: "blue",
            2: "green",
            3: "red",
            4: "darkblue",
            5: "darkred",
            6: "cyan",
            7: "black",
            8: "gray"
        }
        
        #safely load images 
        self.mine_img = None 
        self.flag_img = None 
        mine_path = os.path.join(script_dir, "mine.png") 
        flag_path = os.path.join(script_dir, "flag.png") 
        if os.path.exists(mine_path): self.mine_img = tk.PhotoImage(file=mine_path) 
        if os.path.exists(flag_path): self.flag_img = tk.PhotoImage(file=flag_path) 

        #UI 
        self.frame1 = tk.Frame(root, bd=10, relief=tk.SUNKEN, bg="gray") 
        self.frame1.grid(row=0, column=0, sticky='ew') 
        self.title_frame = tk.Frame(self.frame1, bg="gray") 
        self.title_frame.pack(fill=tk.X) 
        
        self.restart_button = tk.Button(self.title_frame, text="Restart", font=("Helvetica", 9, "bold"), command=self.restart_game) 
        self.restart_button.pack(side=tk.RIGHT) 
        
        self.blank_label = tk.Label(self.title_frame, text=" ", width=self.restart_button.cget("width"), bg="gray") 
        self.blank_label.pack(side=tk.LEFT) 
        
        self.frame2 = tk.Frame(root, bd=10, relief=tk.SUNKEN, bg="gray") 
        self.frame2.grid(row=1, column=0, sticky='ew') 
        
        self.game_frame = tk.Frame(self.frame2, bd=0) 
        self.game_frame.pack() 
        
        self.title = tk.Label(self.title_frame, text="Minesweeper", bg="gray", font=("Helvetica", 24, "bold"), foreground="white") 
        self.title.pack() 
        
        self.mines_label = tk.Label(self.frame1, text=f"Mines: {self.mines}", bg="gray", fg="white", font=("Helvetica", 12, "bold")) 
        self.mines_label.pack(side=tk.LEFT) 
        
        self.empty_spaces_label = tk.Label(self.frame1, text=f"Spaces: {self.empty_squares}", bg="gray", fg="white", font=("Helvetica", 12, "bold")) 
        self.empty_spaces_label.pack(side=tk.LEFT) 
        
        #matrices 
        self.buttons = [[0 for _ in range(cols)] for _ in range(rows)] 
        self.solution_board = [[0 for _ in range(cols)] for _ in range(rows)] 
        self.shown = [[False for _ in range(cols)] for _ in range(rows)] 
        self.flagged = [[False for _ in range(cols)] for _ in range(rows)] 

        #buttons
        self.create_buttons() 
        self.first_click = True #there wont be a mine on the first click 

        #timer
        self.timer_label = tk.Label(self.frame1, text="Time: 0", bg="gray", fg="white", font=("Helvetica", 12, "bold")) 
        self.timer_label.pack(side=tk.RIGHT) 
        self.start_timer() 

    def create_buttons(self): 
        for y in range(self.rows): 
            for x in range(self.cols): 
                #using tk.Label acting as standard raised buttons because buttons don't like images in tkinter 
                button = tk.Label(self.game_frame, image=self.img_size, text=" ", font=("Helvetica", 9, "bold"), compound="center", relief=tk.RAISED, bd=3, width=20, height=20) 
                button.grid(row=y, column=x, sticky="nw") 
                button.bind('<Button-1>', lambda event, b=button, r=y, c=x: self.on_left_click(b, r, c)) 
                button.bind('<Button-3>', lambda event, b=button, r=y, c=x: self.on_right_click(b, r, c)) 
                self.buttons[y][x] = button 

    def place_mines(self, safe_y, safe_x): 
        mines_to_place = self.mines 
        while mines_to_place != 0: 
            yrand = random.randint(0, self.rows-1) 
            xrand = random.randint(0, self.cols-1) 
            #if not a mine and not the first click set a mine then add 1 to the squares around it 
            if (self.solution_board[yrand][xrand] != "x" and not (yrand == safe_y and xrand == safe_x)): 
                self.solution_board[yrand][xrand] = "x" 
                mines_to_place -= 1 
                self.mark_number(yrand-1, xrand-1) 
                self.mark_number(yrand-1, xrand) 
                self.mark_number(yrand-1, xrand+1) 
                self.mark_number(yrand, xrand-1) 
                self.mark_number(yrand, xrand+1) 
                self.mark_number(yrand+1, xrand-1) 
                self.mark_number(yrand+1, xrand) 
                self.mark_number(yrand+1, xrand+1) 

    def mark_number(self, y, x): 
        #check for boundaries and not a mine, then add 1 
        if 0 <= y < self.rows and 0 <= x < self.cols and self.solution_board[y][x] != "x": 
            self.solution_board[y][x] += 1 

    def sink_cell(self, button): 
        #uniformly sinks a cell widget without hover artifacts 
        button.config(bg="#d9d9d9", relief=tk.SUNKEN) 

    def update_counters(self): 
        self.mines_label.config(text=f"Mines: {self.mines}") 
        self.empty_spaces_label.config(text=f"Spaces: {self.empty_squares}") 
        
        #no empty squares left and game not over, WIN
        if self.empty_squares == 0 and not self.game_over: 
            self.game_over = True 
            for r in range(self.rows): 
                #reveal the mines 
                for c in range(self.cols): 
                    if self.solution_board[r][c] == "x": 
                        self.buttons[r][c].config(image=self.mine_img, text="", bg="#7CFC00", relief=tk.SUNKEN) 
            self.title["fg"] = "#7CFC00" 
            self.title["text"] = "You Won!" 

    def on_left_click(self, cur_button, y, x): 
        #unchanged 
        if self.game_over or self.shown[y][x] or self.flagged[y][x]: 
            return 
            
        #first click 
        if self.first_click: 
            self.place_mines(y, x) 
            self.first_click = False 
            
        #mine 
        if self.solution_board[y][x] == "x": 
            self.game_over = True 
            for r in range(self.rows): 
                #blow up the board 
                for c in range(self.cols): 
                    if self.solution_board[r][c] == "x": 
                        self.buttons[r][c].config(image=self.mine_img, text="", bg="#DC143C", relief=tk.SUNKEN) 
            self.title["fg"] = "#8B0000" 
            self.title["text"] = "Game Over" 
        #empty square 
        elif self.solution_board[y][x] == 0: 
            self.discover_recur(y, x) 
        #number 
        else: 
            val = self.solution_board[y][x]
            cur_button.config(text=val, fg=self.colors.get(val, "black")) 
            self.sink_cell(cur_button) 
            self.shown[y][x] = True 
            self.empty_squares -= 1 
            self.update_counters() 

    def on_right_click(self, cur_button, y, x): 
        #unchanged after... 
        if self.game_over or self.shown[y][x]: 
            return 
            
        #set and unset flags 
        if not self.flagged[y][x]: 
            cur_button.config(image=self.flag_img, text="") 
            self.flagged[y][x] = True 
            self.mines -= 1 
        else: 
            cur_button.config(image=self.img_size, text=" ", relief=tk.RAISED)
            self.flagged[y][x] = False 
            self.mines += 1 
        self.update_counters() 

    def discover_recur(self, y, x): 
        #check for boundaries, mines and flags 
        if not (0 <= y < self.rows and 0 <= x < self.cols): 
            return 
        if self.solution_board[y][x] == "x" or self.shown[y][x] or self.flagged[y][x]: 
            return 

        self.sink_cell(self.buttons[y][x]) 
        self.shown[y][x] = True 
        self.empty_squares -= 1 
        
        #recursion logic 
        if 1 <= self.solution_board[y][x] <= 8: 
            val = self.solution_board[y][x]
            self.buttons[y][x].config(text=val, fg=self.colors.get(val, "black")) 
        elif self.solution_board[y][x] == 0: 
            self.buttons[y][x]["text"] = "" 
            self.discover_recur(y-1, x-1) 
            self.discover_recur(y-1, x) 
            self.discover_recur(y-1, x+1) 
            self.discover_recur(y, x-1) 
            self.discover_recur(y, x+1) 
            self.discover_recur(y+1, x-1) 
            self.discover_recur(y+1, x) 
            self.discover_recur(y+1, x+1) 
        self.update_counters() 

    def start_timer(self): 
        self.start_time = time.time() 
        self.update_timer() 

    def update_timer(self): 
        if not self.game_over: 
            elapsed = int(time.time() - self.start_time) 
            self.timer_label.config(text=f"Time: {elapsed}") 
            #capture background loop identifier token
            self.timer_job = self.root.after(1000, self.update_timer) 

    def restart_game(self): 
        #stop the old timer from running to avoid loop overlap
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
            
        self.frame1.destroy() 
        self.frame2.destroy() 
        self.game_over = False 
        self.__init__(self.root, num_rows, num_cols, self.initial_mines) 

#create the tkinter window 
root = tk.Tk() 

icon_path = os.path.join(script_dir, "flag.ico") 
if os.path.exists(icon_path): 
    root.iconbitmap(icon_path) 

root.title("Minesweeper Game") 
root.configure(background="gray") 
board = MinesweeperBoard(root, num_rows, num_cols, num_mines)
root.resizable(False, False)

root.mainloop()
