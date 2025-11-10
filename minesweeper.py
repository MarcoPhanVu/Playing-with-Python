import random
import math
import tkinter as tk

class MineSweeper:
	fontDefault = ("Courier New", 8)

	def __init__(self, width = 8, height = 8, bombs = 5):
		self.width = width
		self.height = height
		self.bombs = bombs
		self.actual_board = []
		self.display_board = []

		# Generate GUI
		self.root = tk.Tk()
		self.root.geometry("500x500")
		self.root.title("Minesweeper")

		self.label = tk.Label(self.root, text="Minesweeper", font=("Courier New", 32))
		self.label.pack()

		self.main_UI = tk.Frame(self.root)
		self.main_UI.pack(fill= "both", expand = True)
		self.main_UI.columnconfigure(0, weight = 1)
		self.main_UI.columnconfigure(1, weight = 1)

		self.display_board_frame = tk.Frame(self.main_UI, bg= "light grey")
		self.display_board_frame.grid(row = 0, column = 0, padx = 24)
		self.actual_board_frame = tk.Frame(self.main_UI, bg= "light grey")
		self.actual_board_frame.grid(row = 0, column = 1, padx = 24)

		# Generate Boards
		self.display_board = [[0 for cell in range(width)] for cell in range(height)]

		self.generate_actual_board(self.width, self.height, self.bombs)
		print("Actual Board:")
		self.print_board(self.actual_board)
		print("Display Board:")
		self.print_board(self.display_board)

		# Visualize Boards for display and actual
		for i in range(self.height):
			self.display_board_frame.rowconfigure(i, weight = 1)
			self.actual_board_frame.rowconfigure(i, weight = 1)

			for j in range(self.width):
				self.display_board_frame.columnconfigure(j, weight = 1)
				self.actual_board_frame.columnconfigure(j, weight = 1)

				cell = tk.Button(	self.display_board_frame,
									# text = f"{j} d",
									text = f"{self.actual_board[i][j]}",
									font = self.fontDefault,
									command = lambda i = i, j = j: 
									self.pick(i, j, self.display_board))
				cell.grid(row = i, column = j, sticky = "NSEW")

				cell = tk.Button(	self.actual_board_frame,
									# text = f"{j} a",
									text = f"{self.actual_board[i][j]}",
									font = self.fontDefault,
									command = lambda i = i, j = j: 
									self.pick(i, j, self.actual_board))
				cell.grid(row = i, column = j, sticky = "NSEW")

		self.root.mainloop()

	def generate_actual_board(self, width = 8, height = 8, bombs = 5):
		board = []
		bomb_locs = self.__generate_bombs(width, height, bombs)

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
		self.actual_board = board

	def __generate_bombs(self, width, height, bombs):
		#randomize bomb locs 1D array
		bomb_loc_1D = []
		temp = 0
		while bombs > 0:
			if (temp not in bomb_loc_1D) and (random.randint(0, 1)):
				bombs -= 1
				bomb_loc_1D.append(temp)
			temp = random.randint(0, width * height)

		bomb_loc_1D = [3, 18, 8, 55, 12] 
		# print(bomb_loc_1D)

		# convert to 2D
		bomb_loc_2D = []
		for loc in bomb_loc_1D:
			loc -= 1 #compensate for 0
			bomb_loc_2D.append((loc // width, loc % width))   # // = integer division
		# print(bomb_loc_2D)

		return bomb_loc_2D

	def draw_board(self, board_in_general):
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

	def flag(self, x, y, board_in_general):
		try:
			board_in_general[x][y] = 2
			print(f"flag at {x}, {y}")
		except IndexError as e:
			print(f"IndexErr(flag): {x}, {y} is out of range")

	def pick(self, x, y, board_in_general):
		try:
			board_in_general[x][y] = "2"
			print(f"pick at {x}, {y}")
		except IndexError as e:
			print(f"IndexErr(pickl): {x}, {y} is out of range")

	def print_board(self, board_in_general):
		for row in board_in_general:
			print(row)

MineSweeper()



class NOTMineSweeperLOL:
	width = 8
	height = 8
	bombs = 5
	actual_board_state = []
	display_board_state = []

	def __init__(self):
		self.root = tk.Tk()
		# @[shortened]
		self.main_UI = tk.Frame(self.root)
		self.display_board_frame = tk.Frame(self.main_UI, bg= "light grey")
		self.actual_board_frame = tk.Frame(self.main_UI, bg= "light grey")
		# [shortened]@

		#I'm not sure about this part, is this creating the actual_board correctly?
		self.generate_actual_board(self.width, self.height, self.bombs)

	def generate_bombs(width, height, bombs):
		bomb_loc_2D = []
		return bomb_loc_2D
	
	def generate_actual_board(self, width = 8, height = 8, bombs = 5):
		board = []
		bomb_locs = self.__generate_bombs(width, height, bombs)

		for i in range(height):
			board.append([])
			for j in range(width):
				if (i, j) in bomb_locs:
					board[i].append(1)
				else:
					board[i].append(0)
		self.actual_board = board