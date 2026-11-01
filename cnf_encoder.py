import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", default=None, type=str, help="File with hidato instance")

def encode(filename):
	FIRST_LINE_LENGTH = 100
	with open(filename, "r") as f_in:
		row, column = map(int, f_in.readline().strip().split(","))
		number_count = row*column
		clause_count = 0
		input_values = [[-1] * column for _ in range(row)]
		for line in f_in:
			i, j, value = map(int, line.strip().split(","))
			input_values[i][j] = value
			if (value == 0):
				number_count -= 1
	with open("cnf.txt", "w") as f_out:
		f_out.write(" " * FIRST_LINE_LENGTH + "\n")
		clause_count += encode_atleast_one(row, column, number_count, input_values, f_out)
		clause_count += encode_atmost_one(row, column, number_count, input_values, f_out)
		clause_count += encode_directions(row, column, number_count, input_values, f_out)
		clause_count += encode_input_values(row, column, number_count, input_values, f_out)
		f_out.seek(0)
		unknown_count = (row*column)*number_count
		header = f"p cnf {unknown_count} {clause_count}"
		f_out.write(header.ljust(FIRST_LINE_LENGTH))
	
def encode_atleast_one(row, column, number_count, input_values, f_out):
	clause_count = 0
	for i in range(row):
		for j in range(column):
			if(input_values[i][j] == 0):
				continue
			for k in range(number_count):
				var = get_index(i, j, k, column, number_count)
				f_out.write(f"{var} ")
			f_out.write("0\n")
			clause_count += 1
	return clause_count


def encode_atmost_one(row, column, number_count, input_values, f_out):
	clause_count = 0
	for i in range(row):
		for j in range(column):
			if(input_values[i][j] == 0):
				continue
			for k in range(number_count):
				it = get_index(i, j, k, column, number_count)
				l = it
				while (l % (number_count) != 0):
					l += 1
					f_out.write(f"{-it} {-l} 0\n")
					clause_count += 1
	return clause_count


def encode_directions(row, column, number_count, input_values, f_out):
	directions = [(1,0), (0,1), (1,1), (-1,0), (0,-1), (-1,-1), (1,-1), (-1,1)]
	clause_count = 0
	for i in range(row):
		for j in range(column):
			if(input_values[i][j] == 0):
				continue
			for k in range(number_count - 1):
				current = get_index(i, j, k, column, number_count)
				f_out.write(f"{-current} ")
				for direction in directions:
					if(i + direction[0] >= 0 and j + direction[1] >= 0 and i + direction[0] < row and j + direction[1] < column and k < row*column - 1):
						index = get_index(i + direction[0], j + direction[1], k + 1, column, number_count)
						f_out.write(f"{index} ")
				f_out.write("0\n")
				clause_count += 1
	return clause_count


def encode_input_values(row, column, number_count,  input_values, f_out):
	clause_count = 0
	for i in range(row):
		for j in range(column):
			value = input_values[i][j]
			if (value > 0):
				index = get_index(i, j, value - 1, column, number_count)
				f_out.write(f"{index} 0\n")
				clause_count += 1
			elif (value == 0):
				for k in range(number_count):
					index = get_index(i, j , k, column, number_count)
					f_out.write(f"{-index} 0\n")
					clause_count += 1
	return clause_count
			

def get_index(row_index, column_index, value, column_count, number_count):
	return (row_index*(column_count*number_count) + column_index*(number_count) + value + 1)


if __name__ == "__main__":
	args = parser.parse_args([] if "__file__" not in globals() else None)
	encode(args.input_file)