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
	pass

if __name__ == "__main__":
	# print(f"Task 1: {sim_diff_integers(20, 4, 10000)}")
	# print(f"Task 2: {gamblers_expected_time(10, 200, 0.8, 10000)}")
	print("mains")

		