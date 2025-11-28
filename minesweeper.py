import random
import math
import tkinter as tk
from tkinter import *
# Define what will cell behave when rightclick

class MineSweeper:
	fontDefault = ("Courier New", 12)
	BOMBCellColor = "#000"
	FlaggedCellColor = "#F87575"
	UntouchedColor = "#eeeeee"
	emptyCellSign = 0
	numberedCellColor = [
		"#BFD7EA", #0
		"#60938C",	#1
		"#508CA4",	#2
		"#286E69",	#3
		"#295166",	#4
		"#004F2D",	#5
		"#354C7C",	#6
		"#55444C",	#7
		"#0D2463",	#8
		"#222E50"	#Bomb
	]

	def __init__(self, root, width = 8, height = 8, bombs = 5):
		self.width = width
		self.height = height
		self.bombs = bombs
		self.actual_board = []
		self.display_board = []

		# Generate GUI
		self.root = root
		self.root.geometry("1920x1080")
		self.root.title("Minesweeper")

		self.label = tk.Label(self.root, text="Minesweeper", font=("Courier New", 32))
		self.label.pack()

		# Main UI
		self.main_UI = tk.Frame(self.root, bg= "#30343F")
		self.main_UI.pack(fill = "both", expand = True)
		self.main_UI.columnconfigure(0, weight = 1, minsize = 200)
		
		self.display_board_frame = tk.Frame(self.main_UI, bg = "#EA638C")
		self.display_board_frame.grid(row = 0, column = 0, padx = 24, pady = 36)
		
		# Actual Board Display for debugging
		self.main_UI.columnconfigure(1, weight = 1, minsize = 200)
		self.actual_board_frame = tk.Frame(self.main_UI, bg = "#89023E")
		self.actual_board_frame.grid(row = 0, column = 1, padx = 24, pady = 36)

		# Menu for debugging
		self.debug_menu = tk.Frame(self.root, bg ="#FFD9DA")
		self.debug_menu.pack(fill = "both", expand = True)


		# Generate Boards
			# Reference to cells
		self.display_cells = []
		self.actual_cells = []

		# Values: [0] for hidden, [1] for revealed, [F] for flagged
		self.display_board = [[self.emptyCellSign for cell in range(width)] for cell in range(height)]

		# Values: [0-9] for amount of bombs around it and [B] is for bomb 
		self.__generate_actual_board(self.width, self.height, self.bombs)

		# Visualize Boards for display and actual
		for i in range(self.height):
			self.display_board_frame.rowconfigure(i, weight = 1)
			self.display_rows = []

			self.actual_board_frame.rowconfigure(i, weight = 1)
			self.actual_rows = []

			for j in range(self.width):
				self.display_board_frame.columnconfigure(j, weight = 1)
				self.actual_board_frame.columnconfigure(j, weight = 1)

				display_cell = tk.Button(	self.display_board_frame,
											text = " ",
											width = 3,
											font = self.fontDefault,
											command = lambda i = i, j = j: 
											self.pick(i, j, self.display_board))
				display_cell.bind("<Button-3>", self.__cell_flagged_toggle)
				display_cell.row_pos = i # ROW
				display_cell.col_pos = j # COL
				display_cell.value = "E" #empty
				display_cell.grid(row = i, column = j, sticky = "NSEW")
				# , padx = 1, pady = 1)
				self.display_rows.append(display_cell)

				actual_cell = tk.Button(	self.actual_board_frame,
											text = f"{self.actual_board[i][j]}",
											width = 3,
											font = self.fontDefault,
											command = lambda i = i, j = j: 
											self.pick(i, j, self.actual_board))
				actual_cell.bind("<Button-3>", self.__cell_flagged_toggle)
				actual_cell.row_pos = i # ROW
				actual_cell.col_pos = j # COL
				actual_cell.value = self.actual_board[i][j]
				actual_cell.grid(row = i, column = j, sticky = "NSEW")
				# , padx = 1, pady = 1)
				self.actual_rows.append(actual_cell)

			self.display_cells.append(self.display_rows)
			self.actual_cells.append(self.actual_rows)

		self.root.mainloop()

	def __generate_actual_board(self, width = 8, height = 8, bombs = 5):
		board = []
		bomb_locs = self.__generate_bombs(width, height, bombs)

		for i in range(height):
			board.append([])
			for j in range(width):
				if (i, j) in bomb_locs:
					board[i].append("B")
				else:
					board[i].append(0)
		self.actual_board = board

		self.__generate_cell_num()

	def __generate_bombs(self, width, height, bombs): # private function(only functions inside Minesweeper Class can call and use this)
		#randomize bomb locs 1D array
		bomb_loc_1D = []
		temp = 0
		while bombs > 0:
			if (temp not in bomb_loc_1D) and (random.randint(0, 1)):
				bombs -= 1
				bomb_loc_1D.append(temp)
			temp = random.randint(0, width * height)

		# bomb_loc_1D = [3, 18, 8, 55, 12] 

		# convert to 2D
		bomb_loc_2D = []
		for loc in bomb_loc_1D:
			loc -= 1 #compensate for 0
			bomb_loc_2D.append((loc // width, loc % width))   # // = integer division

		return bomb_loc_2D

	def pick(self, x, y, board_in_general):
		# Check revealed
		if self.display_board[x][y] == 1:
			print(f"Cell at [{x}][{y}] revealed already")
			print(f"Show surrounding cells around Cell:[{x}][{y}]\n")

			# # Show surronding cells
			# for i in range(-1, 2): # to include 1
			# 	for j in [-1, 0, 1]: # same as above
			# 		new_x = i + x
			# 		new_y = j + y
			# 		self.pick(new_x, new_y, board_in_general)
			return
		
		if self.display_board[x][y] == "F":
			return

		self.display_board[x][y] = 1 # revealed

		# Flood reveal -> turn this to be a recursive function
		if self.actual_board[x][y] == 0:
			self.__flood_reveal(x, y)
			# pass

		self.__update_display_board()

		#debug session
		if board_in_general == self.actual_board:
			print("Picking from Actual Board")
		elif board_in_general == self.display_board:
			print("Picking from Display Board")	
		try:
			board_in_general[x][y]
			print(f"pick at [{x}][{y}]\n")
		except IndexError as e:
			print(f"IndexErr(pick:): [{x}][{y}] is out of range\n")

	def __flood_reveal(self, x, y): # Recursive function
		self.display_board[x][y] = 1

		# Check neighbors -> 2 ways

		# OPTION 1
		# Explicitly listing all 4 cells
		# directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
		# for dx, dy in directions:
		# 	new_x = x + dx
		# 	new_y = y + dy

		# OPTION 2
		# Loop through all 9 cells
		for i in range(-1, 2):
			for j in [-1, 0, 1]: # same as above
				if abs(i) == abs(j): # 0 -> self.location, # -1, 1 -> diagonal
					continue

				new_x = x + i
				new_y = y + j

				if (0 <= new_x < self.height) and (0 <= new_y < self.width): # ensure within bounds(flood reveal)
					if self.actual_board[new_x][new_y] != "B":
						self.pick(new_x, new_y, self.display_board)
		print()

	def __update_display_board(self):
		for i in range(self.height):
			for j in range(self.width):
				cell_color = self.UntouchedColor
				font_color = cell_color
				updated_text = " "

				display_state = self.display_board[i][j]
				actual_value = self.actual_board[i][j]
				if actual_value == "B":
					actual_value = 9

				if display_state == 1:
					cell_color = self.numberedCellColor[actual_value]
					updated_text = self.actual_board[i][j]

				if display_state == "F":
					cell_color = self.FlaggedCellColor

				# if display_state == 0:
				# 	font_color = cell_color
					
				cells = self.display_cells[i][j]
				cells.config(text = updated_text, fg = font_color, bg = cell_color)


	def __generate_cell_num(self):
		for x in range(self.height):
			for y in range(self.width):
				if self.actual_board[x][y] != "B":
					for i in [-1, 0, 1]:
						for j in [-1, 0, 1]:
							if i == 0 and j == 0:
								continue
							new_x = i + x
							new_y = j + y
							if (0 <= new_x < self.height) and (0 <= new_y < self.width):
								if self.actual_board[new_x][new_y] == "B":
									if self.actual_board[x][y] == 0:
										self.actual_board[x][y] = 1
									else:
										self.actual_board[x][y] += 1

	def __cell_flagged_toggle(self, event):
		cell = event.widget
		y = cell.row_pos
		x = cell.col_pos

		if self.display_board[y][x] == 1: # Do not flag revealed cells
			return
		
		if self.display_board[y][x] == "F": # Do not flag revealed cells
			cell.configure(bg = self.UntouchedColor, text = self.UntouchedColor)
			self.display_board[y][x] = 0
			return
		 
		self.display_board[y][x] = "F"
		cell.configure(bg = self.FlaggedCellColor, text = "")

if __name__ == "__main__":
	root = tk.Tk()
	MineSweeper(root, 16, 16, 36)

# TODO:
# - Flagging cells *
# - Right click to flag
# - Win/Lose detection
# - Better flood reveal (show numbers around revealed 0s)
# - Timer
# - Better GUI design?
# - Editable board size and bomb count
# - Click on numbered cell to reveal surrounding cells if correct number of flags placed
# - High score tracking -> save in a file?
# - scrollable board for large sizes