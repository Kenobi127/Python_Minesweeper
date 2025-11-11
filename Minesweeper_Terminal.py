# File: Minesweeper.py
# Programmer: Mateo Lopez Moncaleano
# Date: 07/16/2023
# This program simulates a Minesweeper game in the terminal doing a 9x9 board with 10 mines. 
# It also creates a file with the board uncovered and all moves done by the player

import random

Y = 9                                                   #rows are y
X = 9                                                   #columns are x
MINES = 10                                              
emptySquares = (Y*X)-MINES                              #how many squares don't have mines
board = [[0 for _ in range(X)] for _ in range(Y)]       #solution board
board2 = [["+" for _ in range(X)] for _ in range(Y)]    #game board

def main():
    global emptySquares
    numMines = MINES
    minesLeft = MINES
    movesList = []

    while numMines!=0:                          #loop that sets the mines 
        yrand = random.randint(0,Y-1)
        xrand = random.randint(0,X-1)

        if(board[yrand][xrand] != "x"):
            board[yrand][xrand] = "x"
            numMines -= 1
            MarkNumber(yrand-1, xrand-1)        #top left
            MarkNumber(yrand-1, xrand)          #top
            MarkNumber(yrand-1, xrand+1)        #top right
            MarkNumber(yrand, xrand-1)          #left
            MarkNumber(yrand, xrand+1)          #right 
            MarkNumber(yrand+1, xrand-1)        #bottom left
            MarkNumber(yrand+1, xrand)          #bottom
            MarkNumber(yrand+1, xrand+1)        #bottom right

    while True:                                 #loop that plays each turn
        print()
        print("Board")
        print(f"Empty spaces left to win: {emptySquares}")
        print(f"Mines left: {minesLeft}")
        print()
        printBoard()

        while True:                             #loop that validates user input
            try:
                y1 = int(input(f"Enter y position from 1 to {Y}: "))
                x1 = int(input(f"Enter x position from 1 to {X}: "))

                y1 -= 1
                x1 -= 1

                if not (0<=y1<Y) or not (0<=x1<X):  #out of bounds
                    print("Out of bounds.")
                elif board2[y1][x1]!="+":           #not a "+" square
                    print("Invalid position")
                else:                               #everything correct, exit loop
                    break                   

            except ValueError:
                print("Enter a valid number.")

        mode = " "
        mode = input('Enter "F" or "f" to flag a mine, otherwise enter any other character to continue: ')


        if mode == "F" or mode == "f":                      #put a flag
            movesList.append(f"{y1+1}, {x1+1} Flag")        #mark the move in the list
            board2[y1][x1] = "F"
            minesLeft -= 1
        else:
            movesList.append(f"{y1+1}, {x1+1}")             #mark the move in the list
            if board[y1][x1] == "x":                        #case 1 it's a mine
                movesList[-1] += " BOOOOM!!!"
                movesList.append("GAME OVER")         

                board2[y1][x1] = board[y1][x1]
                emptySquares -= 1
                print()
                print("GAME OVER")
                print(f"Empty spaces left: {emptySquares}")
                print(f"Mines left: {minesLeft}")
                print()
                printBoard()
                break
            elif board[y1][x1] == 0:                        #case 2 it's an empty with a 0    
                DiscoverRecur(y1, x1)
            else:                                           #case 3 it's an empty square with a number
                board2[y1][x1] = board[y1][x1]
                emptySquares -= 1

            if emptySquares == 0:                           #no empty squares left
                movesList.append("YOU WON")

                print()
                print("YOU WON")
                print(f"Empty spaces left: {emptySquares}")
                print(f"Mines left: {minesLeft}")
                print()
                printBoard()
                break
    
    file = open("MineSweeperMoves.txt", "w")                #write the file with the solution board and the moves
    
    file.write("\n")
    file.write("Board\n")
    file.write(f"Empty spaces left: {emptySquares}\n")
    file.write(f"Mines left: {minesLeft}\n")
    file.write("\n")

    file.write(" ")                                         #write the board
    for count in range(X):
        file.write(f"{count+1:5}")
    file.write("\n")
    for y1 in range(Y):
        file.write(f"{y1+1}    ")
        for x1 in range(X):
            file.write(f"{board[y1][x1]}    ")
        file.write("\n")
        file.write("\n")

    for line in movesList:                                  #write the moves
        file.write(f"{line}\n")

    file.close()

#prints the game board into the terminal
def printBoard():                                           
    print(f" ", end="")
    for count in range(X):
        print(f"{count+1:5}", end="")
    print()
    for y1 in range(Y):
        print(f"{y1+1}    ", end="")
        for x1 in range(X):
            print(f"{board2[y1][x1]}    ", end = "")
        print()
        print()

#adds 1 to the position entered if 3 conditions met
def MarkNumber(y1, x1):
    if 0<=y1<Y and 0<=x1<X and board[y1][x1]!="x":
        board[y1][x1] += 1

#recursive function that checks itself for the following conditions: in board, not a mine, is not opened. 
#Then opens itself and if it was a 0 calls recursion to the 8 places around it
def DiscoverRecur(y1, x1):
    if 0<=y1<Y and 0<=x1<X and board[y1][x1]!="x" and board2[y1][x1]=="+":
        board2[y1][x1] = board[y1][x1]
        global emptySquares 
        emptySquares -= 1
        if board[y1][x1]==0:
            DiscoverRecur(y1-1, x1-1)        #top left
            DiscoverRecur(y1-1, x1)          #top
            DiscoverRecur(y1-1, x1+1)        #top right
            DiscoverRecur(y1, x1-1)          #left
            DiscoverRecur(y1, x1+1)          #right
            DiscoverRecur(y1+1, x1-1)        #bottom left
            DiscoverRecur(y1+1, x1)          #bottom
            DiscoverRecur(y1+1, x1+1)        #bottom right
        
main()
