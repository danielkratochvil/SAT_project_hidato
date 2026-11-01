import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("--output_file", default=None, type=str, help="File with hidato solution")
parser.add_argument("--row", default=0, type=int, help="Row count")
parser.add_argument("--column", default=0, type=int, help="Column count")
parser.add_argument("--number_count", default=0, type=int, help="Number count")

def generate_hidato(output_file, row, column, number_count):
	grid = [[-1] * column for _ in range(row)]
	directions = [(1,0), (0,1), (1,1), (-1,0), (0,-1), (-1,-1), (1,-1), (-1,1)]
	while True:
		grid = [[-1] * column for _ in range(row)]
		row_index = random.randrange(0, row)
		column_index = random.randrange(0, column)
		
		grid[row_index][column_index] = 0
		success = True

		for number in range(1, number_count):
			direction_index = random.randrange(0, 8)
			moved = False
			
			for _ in range(8):
				new_row = row_index + directions[direction_index][0]
				new_col = column_index + directions[direction_index][1]
				
				# Opravená kontrola hranic mřížky
				if (0 <= new_row < row and 0 <= new_col < column and grid[new_row][new_col] == -1):
					grid[new_row][new_col] = number
					row_index = new_row
					column_index = new_col
					moved = True
					break
					
				direction_index = (direction_index + 1) % 8
			
			# Pokud není kam pokračovat (slepá ulička), přerušíme pokus a zkusíme to znovu
			if not moved:
				success = False
				break
				
		if success:
			break

	with open(output_file, "w") as f:
		f.write(f"{row},{column}\n")
		for i in range(row):
			for j in range(column):
				value = grid[i][j]
				if(value == -1):
					f.write(f"{i},{j},0\n")
				else:
					if(random.getrandbits(1) or value == 0 or value == number_count - 1):
						f.write(f"{i},{j},{value + 1}\n")
			



if __name__ == "__main__":
	args = parser.parse_args([] if "__file__" not in globals() else None)
	generate_hidato(args.output_file, args.row, args.column, args.number_count) 