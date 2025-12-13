import random
import math
import json
import os
import pathlib
from pathlib import Path
import tkinter as tk
from tkinter import *
from tkinter import messagebox
# Define what will cell behave when rightclick

class MineSweeper:
	fontDefault = ("Courier New", 12)
	BOMBCellColor = "#000"
	FlaggedCellColor = "#F87575"
	UntouchedColor = "#eeeeee"
	emptyCellSign = "H"
	numberedCellColor = [
		"#BFD7EA", #0
		"#93B2AE",	#1
		"#77A1B1",	#2
		"#4E8682",	#3 
		"#4C7287",	#4
		"#33795B",	#5
		"#5C709A",	#6
		"#55444C",	#7
		"#0D2463",	#8
		"#222E50"	#Bomb
	]

	cell_flagged_count = 0
	cell_revealed_count = 0
	total_cells = 0

	actual_board = []
	display_board = []

	# Generate GUI
	def __init__(self, root: tk.Tk, actual_board: list) -> None:
		self.height = len(actual_board)
		self.width = len(actual_board[0])

		self.setup_UI(root)
		

	def __init__(self, root: Tk, width = 8, height = 8, bombs = 5):
		self.width = width
		self.height = height
		self.bombs = bombs

		self.cell_flagged_count = 0
		self.cell_revealed_count = 0
		self.total_cells = 0
		self.total_cells = self.width * self.height

		self.setup_UI(root)
		self.load_board(None, None)
		self.root.mainloop()

	def setup_UI(self, root: tk.Tk) -> None:
		self.root = root
		self.root.geometry("1280x720")
		self.root.title("Minesweeper")

		# Title
		self.label = tk.Label(self.root, text="Minesweeper", font=("Courier New", 32))
		self.label.pack()

		# Main Body
		self.main_body = tk.Frame(self.root, bg= "#30343F")
		self.main_body.pack(fill = "both", expand = True)

		# Stats Panel
		self.load_stats()

		# Display Board
		self.main_body.columnconfigure(1, weight = 3, minsize = 200) # column 1 have 3 units of space
		self.display_board_frame = tk.Frame(self.main_body, bg = "#95EA63")
		self.display_board_frame.grid(row = 0, column = 1, padx = 24, pady = 36)
		
		# Actual Board Display for debugging
		self.main_body.columnconfigure(2, weight = 3, minsize = 200)
		self.actual_board_frame = tk.Frame(self.main_body, bg = "#89023E")
		self.actual_board_frame.grid(row = 0, column = 2, padx = 24, pady = 36)

		# Menu for actions
		self.actions_menu = tk.Frame(self.root, bg ="#FFD9DA", height = 360)
		self.actions_menu.pack(fill = "both", expand = True)

		self.actions_menu.columnconfigure(3, weight = 1)
		self.save_board_button = tk.Button(	
							self.actions_menu,
							text = "Save Board",
							command= self.__save_board)

		self.new_game_button = tk.Button(	
							self.actions_menu,
							text = "New Game",
							command= self.__new_game)

		# self.open_from_file_button = tk.Button(	
		# 					self.actions_menu,
		# 					text = "Open From File",
		# 					command= self.__open_from_file)

		self.toggle_actual_board_button = tk.Button(	
							self.actions_menu,
							text = "Toggle Actual Board",
							command= self.__toggle_actual_board)

		self.save_board_button.grid(row = 0, column = 0, sticky = "NSEW")
		self.new_game_button.grid(row = 0, column = 1, sticky = "NSEW")
		self.toggle_actual_board_button.grid(row = 0, column = 2, sticky = "NSEW")

		# Toggle actual board
		
	def __save_board(self) -> None:
		filepath_P = Path("./data/saved_board")

		actual_2D_Arr = self.actual_board
		display_2D_Arr = self.display_board

		board_data = {
			"actual_board": actual_2D_Arr,
			"display_board": display_2D_Arr
		}

		location_path = "./data/saved_boards/"
		file_name = "saved_board_1.json"
		final_loc = location_path + file_name
		print(f"finalLoc = {final_loc}")
		with open(f"{location_path}{file_name}", "w") as file:
			json.dump(board_data, file, indent = 4)
			file.close()

	def __toggle_actual_board(self) -> None:
		self.actual_board_frame.forget()
		print("forget actual board")
		pass

	def __new_game(self) -> None:
		self.cell_flagged_count = 0
		self.cell_revealed_count = 0
		self.total_cells = 0

		self.load_board(None, None)

	def load_board(self, actual_board, display_board) -> None:
		if actual_board != None and display_board != None:
			print("load existing board")
		else:
			print("new board")
			# Values: [H] for hidden, [R] for revealed, [F] for flagged
			self.display_board = [[self.emptyCellSign for cell in range(self.width)] for cell in range(self.height)]

			# Values: [0-9] for amount of bombs around it and [B] is for bomb 
			self.__generate_actual_board(self.width, self.height, self.bombs)

		# Generate Boards
			# Reference to cells
		self.display_cells = []
		self.actual_cells = []

		# Visualize Boards for display and actual
		for i in range(self.height):
			self.display_board_frame.rowconfigure(i, weight = 1)
			self.display_rows = []

			self.actual_board_frame.rowconfigure(i, weight = 1)
			self.actual_rows = []

			for j in range(self.width):
				self.display_board_frame.columnconfigure(j, weight = 1)
				self.actual_board_frame.columnconfigure(j, weight = 1)

				display_cell = tk.Button(
									self.display_board_frame,
									text = " ",
									width = 3,
									font = self.fontDefault,
									command = lambda i = i, j = j: 
									self.pick(i, j))
				display_cell.bind("<Button-3>", self.__cell_flagged_toggle)
				display_cell.row_pos = i # ROW traverse (height)
				display_cell.col_pos = j # COL traverse (width)
				display_cell.grid(row = i, column = j, sticky = "NSEW")
				# , padx = 1, pady = 1)
				self.display_rows.append(display_cell)

				actual_cell = tk.Button(
									self.actual_board_frame,
									text = f"{self.actual_board[i][j]}",
									width = 3,
									font = self.fontDefault,
									command = lambda i = i, j = j: 
									self.pick(i, j))
				actual_cell.bind("<Button-3>", self.__cell_flagged_toggle)
				actual_cell.row_pos = i # same with display
				actual_cell.col_pos = j # same with display
				actual_cell.value = self.actual_board[i][j]
				actual_cell.grid(row = i, column = j, sticky = "NSEW")
				# , padx = 1, pady = 1)
				self.actual_rows.append(actual_cell)

			self.display_cells.append(self.display_rows)
			self.actual_cells.append(self.actual_rows)

		# self.__save_board()


	def __generate_actual_board(self, width = 8, height = 8, bombs = 5) -> None:
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

	def __generate_bombs(self, width, height, bombs) -> list: # private function(only functions inside Minesweeper Class can call and use this)
		# return 2D array of bomb locations
		#randomize bomb locs 1D array
		bomb_loc_1D = []
		temp = 0
		while bombs > 0:
			if (temp not in bomb_loc_1D) and (random.randint(0, 1)):
				bombs -= 1
				bomb_loc_1D.append(temp)
			temp = random.randint(0, width * height)

		# convert to 2D
		bomb_loc_2D = []
		for loc in bomb_loc_1D:
			loc -= 1 #compensate for 0
			bomb_loc_2D.append((loc // width, loc % width))   # // = integer division

		return bomb_loc_2D

	def pick(self, x, y) -> None:
		if self.actual_board[x][y] == "B":
			self.player_lost()
			return

		# Check revealed + reveal around
		if self.display_board[x][y] == "R":
			# Only reveal around if this is a non-zero cell
			if self.actual_board[x][y] != 0 and self.actual_board[x][y] != "B":
				try:
					self.__cell_reveal_around(x, y)
				except IndexError as e:
					print(e)
				except RecursionError as e:
					print(e)
			return
		
		if self.display_board[x][y] == "F": # skip flagged cells
			return

		# Flood reveal -> turn this to be a recursive function
		if self.actual_board[x][y] == 0:
			self.__flood_reveal(x, y)
			# pass

		self.display_board[x][y] = "R" # reveal current cell
		self.cell_revealed_count += 1

		self.__update_labels()
		self.__update_display_board()

	def __flood_reveal(self, x, y): # Recursive function
		# print("Flood reveal entered")
		if self.display_board[x][y] == "R" or self.actual_board[x][y] == "B": # Skip if revealed
			return

		self.display_board[x][y] = "R"

		if self.actual_board[x][y] != 0: # Stop if not 0
			return

		# OPTION 1
		# Loop through all 9 cells
		for i in [-1, 0, 1]:
			for j in [-1, 0, 1]:
				# if abs(i) == abs(j): # 0 -> self.location, # -1, 1 -> diagonal
				if i == 0 and j ==0:
					continue

				new_x = x + i
				new_y = y + j

				if (0 <= new_x < self.height) and (0 <= new_y < self.width): # ensure within bounds(flood reveal)
					if self.display_board[new_x][new_y] != "R" and self.actual_board != "B": # MAJOR CHANGE! Flood reveal calls itself, not pick()
						self.__flood_reveal(new_x, new_y)

	def load_stats(self) -> None:
		self.main_body.columnconfigure(0, weight = 1, minsize = 200)
		self.stats_panel = tk.Frame(self.main_body, bg = "#63A0EA")
		self.stats_panel.configure(width = 600, height = 800)

		# simple method of checking existed
		# tk.Label(self.stats_panel, text = "Stats Panel").pack()
		# self.stats_panel.grid_propagate(False)

		self.stats_panel.grid(row = 0, column = 0, padx = 24, pady = 36)

		self.bombs_count_label = tk.Label(
			self.stats_panel, 
			text = f"Bombs: {self.cell_flagged_count}/{self.bombs}", 
			font = self.fontDefault, 
			bg = "#20C03B"
			)

		self.cell_count_label = tk.Label(
			self.stats_panel, 
			text = f"Cells Revealed: {self.cell_revealed_count}/{self.total_cells}", 
			font = self.fontDefault, 
			bg = "#0A0050"
			)

		self.bombs_count_label.pack(pady = 12)
		self.cell_count_label.pack(pady = 12)

	def __update_labels(self):
		# Stats update
		self.bombs_count_label.config(text = f"Bombs: {self.cell_flagged_count}/{self.bombs}")
		self.cell_count_label.config(text = f"Cells Revealed: {self.cell_revealed_count}/{self.total_cells}")

	def __update_display_board(self):
		# Cells config update
		for i in range(self.height):
			for j in range(self.width):
				cell_color = self.UntouchedColor
				font_color = cell_color
				updated_text = " "
				relief = tk.RAISED

				display_state = self.display_board[i][j]
				actual_value = self.actual_board[i][j]
				if actual_value == "B":
					actual_value = 9

				if display_state == "R":
					cell_color = self.numberedCellColor[actual_value]
					updated_text = self.actual_board[i][j]
					# relief = tk.SUNKEN
					if self.actual_board[i][j] == 0:
						relief = tk.FLAT

				if display_state == "F":
					cell_color = self.FlaggedCellColor

				# if display_state == "H":
				# 	font_color = cell_color
					
				cells = self.display_cells[i][j]
				cells.config(text = updated_text, fg = font_color, bg = cell_color, relief = relief)
				# cells.config(text = updated_text, fg = font_color, bg = cell_color)


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

		if self.display_board[y][x] == "R": # Do not flag revealed cells
			return
		
		if self.display_board[y][x] == "F": # Unflag flagged cells
			cell.configure(bg = self.UntouchedColor, text = self.UntouchedColor)
			self.display_board[y][x] = "H"
			self.cell_flagged_count -= 1
			return
		 
		self.display_board[y][x] = "F"
		self.cell_flagged_count += 1
		cell.configure(bg = self.FlaggedCellColor)
		self.__update_labels()
		self.__update_display_board()

	def __cell_reveal_around(self, x, y):
		bombs_around = self.actual_board[x][y]
		flag_counts = 0
		for i in [-1, 0, 1]:
			for j in [-1, 0, 1]:
				new_x = x + i
				new_y = y + j

				if (0 <= new_x < self.height) and (0 <= new_y < self.width): # Ensure within boundaries
					if self.display_board[new_x][new_y] == "R": # Skip if revealed
						continue

					if self.display_board[new_x][new_y] == "F":
						flag_counts += 1
						if flag_counts > bombs_around:
							print("Too many flags")
							return
						
						if self.actual_board[new_x][new_y] == "B":
							print(f"Cell truly has bomb at [{new_x}][{new_y}]\n")
							continue

		if flag_counts == bombs_around:
			for i in [-1, 0, 1]:
				for j in [-1, 0, 1]:
					new_x = x + i
					new_y = y + j

					if (0 <= new_x < self.height) and (0 <= new_y < self.width):
						if self.display_board[new_x][new_y] == "H":
							# if self.actual_board[new_x][new_y] == "B" and self.actual_board[new_x][new_y] == "F":
							# 	continue # Skip correctly flagged cells
							self.pick(new_x, new_y) # Only pick if hidden
	def player_lost(self):
		tk.messagebox.showinfo("Player Lost", "Bomb activated! Game Over.")
		for i in range(self.height):
			for j in range(self.width):
				if self.actual_board[i][j] == "B":
					self.display_board[i][j] = "R"
		self.__update_display_board()

	def player_won(self):
		tk.messagebox.showinfo("Player Won", "Congratulations! You have won the game!")

if __name__ == "__main__":
	root = tk.Tk()
	MineSweeper(root, 12, 12, 12)

# TODO:
# - Timer
# - Better GUI design?
# - Editable board size and bomb count
# - Click on numbered cell to reveal surrounding cells if correct number of flags placed
# - High score tracking -> save in a file?
# - scrollable board for large sizes