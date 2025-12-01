import random

# def party(n: int):
	
def sim_diff_integers(n: int, k: int, NUM_SIM: int) -> float:
	count = 0.0
	for i in range (NUM_SIM):
		int_given = []
		
		for i in range(n):
			int_given.append(random.randint(1, k))
		
		int_given = set(int_given)

		if len(int_given) == k:
			count += 1.0
	return count / float(NUM_SIM)

def gamblers_expected_time(k: int, M: int, p: float, NUM_SIM: int) -> int:
	"""_summary_
	Args:
		k (int): _initial amount_
		M (int): _goal amount_
		p (float): _chance of winning_
		NUM_SIM (int): _number of simulations_
	"""
	total_trials = []
	for i in range(NUM_SIM):
		funds = k
		count = 0
		choices = [1, 0]
		prob = [p, 1 - p]
		while (funds > 0):
			if (random.choices(choices, prob)[0] == 1):
				funds += 1
			else:
				funds -= 1

			if funds > M:
				break

			count += 1

		total_trials.append(count)

		# print(f"{i} out of {NUM_SIM}")
		# print(total_trials)

	avg = int (sum(total_trials)/len(total_trials))
	return avg

def run_of_success(p: float, S: int, F: int, NUM_SIM: int) -> float:
	prob = [p, 1 - p]
	choices = [1, 0]

	S_count = 0
	F_count = 0

	S_First = 0
	F_First = 0

	for i in range(NUM_SIM):
		S_count = 0
		F_count = 0
		while (S_count != S) and (F_count != F):
			res = random.choices(choices, prob)[0]
			if (res == 1):
				S_count += 1
				F_count = 0
			elif (res == 0):
				F_count += 1
				S_count = 0
		if (S_count == S):
			S_First += 1
		if (F_count == F):
			F_First += 1

	print(f"S_first: {S_First}")
	print(f"F_first: {F_First}")
	return (float(S_First) / float(NUM_SIM))
	


if __name__ == "__main__":
	# print(f"Task 1: {sim_diff_integers(20, 4, 10000)}")
	# print(f"Task 2: {gamblers_expected_time(10, 200, 0.8, 10000)} times")
	print(f"Task 3: {run_of_success(0.7, 10, 5, 10000)} times")
	print("mains")

		