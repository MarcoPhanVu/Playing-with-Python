import random
import math
import tkinter as tk

root = tk.Tk()

root.geometry("500x500")
root.title("Minesweeper")
label = tk.Label(root, text="Minesweeper", font=("Courier New", 32))
label.pack()

textbox = tk.Text(root, height=3, font=("Courier New", 16))
textbox.pack(padx=32, pady=32)



boardFrame = tk.Frame(root)
boardFrame.columnconfigure(0, weight=1)
boardFrame.columnconfigure(1, weight=1)
boardFrame.columnconfigure(2, weight=1)
boardFrame.columnconfigure(3, weight=2)

btn1 = tk.Button(boardFrame, text="1", font=("Courier New", 16))
btn1.grid(row=0, column=0, sticky=tk.W + tk.E)

btn1 = tk.Button(boardFrame, text="2", font=("Courier New", 16))
btn1.grid(row=0, column=1, sticky=tk.W + tk.E)

btn1 = tk.Button(boardFrame, text="3", font=("Courier New", 16))
btn1.grid(row=0, column=2, sticky=tk.W + tk.E)

btn1 = tk.Button(boardFrame, text="4", font=("Courier New", 16))
btn1.grid(row=1, column=2, sticky=tk.W + tk.E)

btn1 = tk.Button(boardFrame, text="5", font=("Courier New", 16))
btn1.grid(row=1, column=3, sticky=tk.W + tk.E)

btn1 = tk.Button(boardFrame, text="6", font=("Courier New", 16))
btn1.grid(row=2, column=0, sticky=tk.W + tk.E)

boardFrame.pack(padx=32, pady=32, fill="x")

root.mainloop()

def generate_board(width = 8, height = 8, bombs = 5):
    board = []
    bomb_locs = generate_bombs(width, height, bombs)

    for i in range(height):
        board.append([])    #ensure row existed
        for j in range(width):
            # if (bombs > 0) and (random.randint(0, int(width + height)) == int((width + height)/2)):
            #     board[i].append(1)
            #     bombs -= 1
            #     continue
            if (i, j) in bomb_locs:
                board[i].append(1)
            else:
                board[i].append(0)
    return board

def generate_bombs(width, height, bombs):
    #randomize bomb locs 1D array
    bomb_loc_1D = []
    temp = 0
    while bombs > 0:
        if (temp not in bomb_loc_1D) and (random.randint(0, 1)):
            bombs -= 1
            bomb_loc_1D.append(temp)
        temp = random.randint(0, width * height)

    bomb_loc_1D = [3, 18, 8, 55, 12] 
    print(bomb_loc_1D)

    # convert to 2D
    bomb_loc_2D = []
    for loc in bomb_loc_1D:
        loc -= 1 #compensate for 0
        bomb_loc_2D.append((loc // width, loc % width))   # // = integer division
    print(bomb_loc_2D)

    return bomb_loc_2D

def draw_board(board_in_general):
    height = len(board_in_general)
    width = len(board_in_general[0])
    for i in range(height): #y, x order
        if (i == 0):
            for j in range(width + 1):
                print(j, end = "  ")
            print()
            
        for j in range(width): #y, x order
            if (j == 0):
                print(chr(i + 65), end = " ")
            
            if board_in_general[i][j] == 1:
                print("🟥", end = " ")
            elif board_in_general[i][j] == 0:
                print("⬛", end = " ")
            elif board_in_general[i][j] == 2:
                print("🚩", end = " ")
        print()

def flag(x, y, board_in_general):
    try:
        x = ord(x) - 65 - 1
        y = int(y)
        # - 1 to compensate for 0

        board_in_general[x][y] = 2
        print(f"flag at {x}, {y}")
    except IndexError as e:
        print(f"IndexErr: {x}, {y} is out of range")

def pick(x, y, board_in_general):
    try:
        x = ord(x) - 65
        y = int(y)

        board_in_general[x][y] = "2"
        print(f"pick at {x}, {y}")
    except IndexError as e:
        print(f"IndexErr: {x}, {y} is out of range")

def print_board(board_in_general):
    for row in board_in_general:
        print(row)

def main():

    game_over = False
    board_state = generate_board()
    board_display = []
    for i in range(len(board_state)):
        board_display.append([])
        for j in range(len(board_state[0])):
            board_display[i].append(0)

    # print_board(board_display)


    draw_board(board_state)
    print("board displayaasasdasd")
    draw_board(board_display)

    # while(not game_over):
    #     # choice = int(input("Flag(1) or Pick(0)?:"))
    #     choice = 1
    #     if (choice == 1):
    #         # flag_loc = input("Please choose location:")
    #         flag_loc = "C2"
    #         flag(flag_loc[0], flag_loc[1], board_state)
    #     elif (choice == 0):
    #         pick_loc = input("Please choose location:")
    #         pick(pick_loc[0], pick_loc[1], board_state)
    #     else:
    #         print("Invalid input")
    #         continue
    #     draw_board(board_state)

    #     game_over = True
# main()