import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", default=None, type=str, help="File with hidato instance")

def encode(filename):
	FIRST_LINE_LENGTH = 100
	with open(filename, "r") as f_in:
		row, column = map(int, f_in.readline().strip().split(","))
		unknown_count = (row*column)**2
		clause_count = 0
		input_values = []
		for line in f_in:
			i, j, value = map(int, line.strip().split(","))
			input_values.append((i,j,value))
	with open("cnf.txt", "w") as f_out:
		f_out.write(" " * FIRST_LINE_LENGTH + "\n")
		clause_count += encode_atleast_one(row, column, f_out)
		clause_count += encode_atmost_one(row, column, f_out)
		clause_count += encode_directions(row, column, f_out)
		clause_count += encode_input_values(row, column, f_out, input_values)
		f_out.seek(0)
		header = f"p cnf {unknown_count} {clause_count}"
		f_out.write(header.ljust(FIRST_LINE_LENGTH))
	
def encode_atleast_one(row, column, f_out):
	clause_count = 0
	for i in range(row):
		for j in range(column):
			for k in range(row*column):
				var = get_index(i, j, k, row, column)
				f_out.write(f"{var} ")
			f_out.write("0\n")
			clause_count += 1
	return clause_count


def encode_atmost_one(row, column, f_out):
	clause_count = 0
	for i in range(row):
		for j in range(column):
			for k in range(row*column):
				it = get_index(i, j, k, row, column)
				l = it
				while (l % (row*column) != 0):
					l += 1
					f_out.write(f"{-it} {-l} 0\n")
					clause_count += 1
	return clause_count


def encode_directions(row, column, f_out):
	directions = [(1,0), (0,1), (1,1), (-1,0), (0,-1), (-1,-1), (1,-1), (-1,1)]
	clause_count = 0
	for i in range(row):
		for j in range(column):
			for k in range(row*column - 1):
				current = get_index(i, j, k, row, column)
				f_out.write(f"{-current} ")
				for direction in directions:
					if(i + direction[0] >= 0 and j + direction[1] >= 0 and i + direction[0] < row and j + direction[1] < column and k < row*column - 1):
						index = get_index(i + direction[0], j + direction[1], k + 1, row, column)
						f_out.write(f"{index} ")
				f_out.write("0\n")
				clause_count += 1
	return clause_count


def encode_input_values(row, column, f_out, input_values):
	clause_count = 0
	for value in input_values:
		if (value[2] > 0):
			index = get_index(value[0], value[1], value[2], row, column)
			f_out.write(f"{index} 0\n")
			clause_count += 1
		else:
			for i in range(row*column):
				index = get_index(value[0], value[1], i, row, column)
				f_out.write(f"{-index} 0\n")
				clause_count += 1
	return clause_count
			

def get_index(row_index, column_index, value, row_count, column_count):
	return (row_index*(row_count*column_count**2) + column_index*(row_count*column_count) + value + 1)


if __name__ == "__main__":
	args = parser.parse_args([] if "__file__" not in globals() else None)
	encode(args.input_file)