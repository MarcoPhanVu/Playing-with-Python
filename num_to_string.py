def build_star_tree() -> None:
	while True:
		try:
			star_height = int(input("Please enter the height of the star tree: "))
			if star_height <= 0:
				print("Height must be a positive integer.")
				continue # height invalid
			break
		except ValueError:
			print("Invalid input. Please enter an integer value.")
	star_height += 1
	off_set = star_height - 1

	for i in range(star_height):
		for j in range(off_set):
			print(" ", end="")
		for k in range(i * 2 - 1):
			print("*", end="")
		for j in range(off_set):
			print(" ", end="")
		off_set -= 1
		print()

build_star_tree()