import random
import math
import tkinter as tk
from tkinter import *
# Define what will cell behave when rightclick
def cell_flagged_triggered(event):
	event.widget.configure(bg="red")
	print(event.winfo_children())
	print(type(event))
	print("cell flagged")

class MineSweeper:
	fontDefault = ("Courier New", 12)
	BOMBCellColor = "#000"
	emptyCellSign = "@"
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
		
		self.display_board_frame = tk.Frame(self.main_UI, bg= "#EA638C")
		self.display_board_frame.grid(row = 0, column = 0, padx = 24, pady = 36)
		
		# Actual Board Display for debugging
		self.main_UI.columnconfigure(1, weight = 1, minsize = 200)
		self.actual_board_frame = tk.Frame(self.main_UI, bg= "#89023E")
		self.actual_board_frame.grid(row = 0, column = 1, padx = 24, pady = 36)

		# Menu for debugging
		self.debug_menu = tk.Frame(self.root, bg="#FFD9DA")
		self.debug_menu.pack(fill = "both", expand = True)


		# Generate Boards
			# Reference to cells
		self.display_cells = []
		self.actual_cells = []

		self.display_board = [[self.emptyCellSign for cell in range(width)] for cell in range(height)]

		self.generate_actual_board(self.width, self.height, self.bombs)

		# Visualize Boards for display and actual
		for i in range(self.height):
			self.display_board_frame.rowconfigure(i, weight = 1)
			self.display_rows = []

			self.actual_board_frame.rowconfigure(i, weight = 1)
			self.actual_rows = []

			for j in range(self.width):
				self.display_board_frame.columnconfigure(j, weight = 1)
				self.actual_board_frame.columnconfigure(j, weight = 1)

				cell = tk.Button(	self.display_board_frame,
									# text = f"{j} d",
									text = " ",
									width = 3,
									font = self.fontDefault,
									command = lambda i = i, j = j: 
									self.pick(i, j, self.display_board))
				cell.bind("<Button-3>", cell_flagged_triggered)
				cell.grid(row = i, column = j, sticky = "NSEW")
				# , padx = 1, pady = 1)
				self.display_rows.append(cell)

				cell = tk.Button(	self.actual_board_frame,
									# text = f"{j} a",
									text = f"{self.actual_board[i][j]}",
									width = 3,
									font = self.fontDefault,
									command = lambda i = i, j = j: 
									self.pick(i, j, self.actual_board))
				cell.bind("<Button-3>", cell_flagged_triggered)
				cell.grid(row = i, column = j, sticky = "NSEW")
				# , padx = 1, pady = 1)
				self.actual_rows.append(cell)

			self.display_cells.append(self.display_rows)
			self.actual_cells.append(self.actual_rows)

		self.root.mainloop()

	def generate_actual_board(self, width = 8, height = 8, bombs = 5):
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

		self.generate_cell_num()

	def __generate_bombs(self, width, height, bombs):
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
		if self.display_board[x][y] == self.actual_board[x][y] or self.display_board[x][y] == "F":
			print(f"Cell at [{x}][{y}] revealed already\n")
			print(f"Show surrnding cells around Cell:[{x}][{y}]\n")

			# # Show surronding cells
			# for i in range(-1, 2): # to include 1
			# 	for j in [-1, 0, 1]: # same as above
			# 		new_x = i + x
			# 		new_y = j + y
			# 		self.pick(new_x, new_y, board_in_general)
			return
		
		if self.actual_board[x][y] != 0:
			self.display_board[x][y] = self.actual_board[x][y]

		# Flood reveal -> turn this to be a recursive function
		elif self.actual_board[x][y] == 0:
			self.display_board[x][y] = 0

			# Check neighbors
			for i in range(-1, 2):
				for j in [-1, 0, 1]:
					new_x = i + x
					new_y = j + y
					if i == 0 and j == 0:
						continue
					if (0 <= new_x < self.height) and (0 <= new_y < self.width): # ensure within bounds(flood reveal)
						if self.actual_board[new_x][new_y] != "B":
							self.pick(new_x, new_y, board_in_general)
			print()

		self.update_display_board()
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

	def flood_reveal(self, x, y):
		pass

	def update_display_board(self):
		for i in range(self.height):
			for j in range(self.width):
				cell_value = self.display_board[i][j]
				updated_text = cell_value
				font_color = "#fff"
				cell_color = "#eeeeee"

				if cell_value == "B":
					cell_color = self.BOMBCellColor
				elif cell_value != self.emptyCellSign:
					# print(f"Cell Value: {cell_value} at Y{i}, X{j}")
					cell_color = self.numberedCellColor[cell_value]
					

				cells = self.display_cells[i][j]
				cells.config(text = updated_text, fg = font_color, bg = cell_color)


	def generate_cell_num(self):
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


if __name__ == "__main__":
	root = tk.Tk()
	MineSweeper(root, 16, 16, 64)

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