import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", default=None, type=str, help="File with hidato instance")

def encode(filename):
	FIRST_LINE_LENGTH = 100
	with open(filename, "r") as f_in:
		width, height = map(int, f_in.readline().strip().split(","))
		unknown_count = (width*height)**2
		clause_count = 0
		input_values = [[0] * width for _ in range(height)]
		for line in f_in:
			i, j, value = map(int, line.strip().split(","))
			input_values[i][j] = value
	with open("cnf.txt", "w") as f_out:
		f_out.write(" " * FIRST_LINE_LENGTH + "\n")
		clause_count += encode_atleast_one(width, height, f_out)
		clause_count += encode_atmost_one(width, height, f_out)
		clause_count += encode_directions(width, height, f_out)
		clause_count += encode_input_values(width, height, f_out, input_values)
		f_out.seek(0)
		header = f"p cnf {unknown_count} {clause_count}"
		f_out.write(header.ljust(FIRST_LINE_LENGTH))
	
def encode_atleast_one(width, height, f_out):
	clause_count = 0
	for i in range(width):
		for j in range(height):
			for k in range(width*height):
				var = get_index(i, j, k, width, height)
				f_out.write(f"{var} ")
			f_out.write("0\n")
			clause_count += 1
	return clause_count


def encode_atmost_one(width, height, f_out):
	clause_count = 0
	for i in range(width):
		for j in range(height):
			for k in range(width*height):
				it = get_index(i, j, k, width, height)
				l = it
				while (l % (width*height) != 0):
					l += 1
					f_out.write(f"{-it} {-l} 0\n")
					clause_count += 1
	return clause_count


def encode_directions(width, height, f_out):
	directions = [(1,0), (0,1), (1,1), (-1,0), (0,-1), (-1,-1), (1,-1), (-1,1)]
	clause_count = 0
	for i in range(width):
		for j in range(height):
			for k in range(width*height):
				current = get_index(i, j, k, width, height)
				f_out.write(f"{-current} ")
				for direction in directions:
					if(i + direction[0] >= 0 and j + direction[1] >= 0 and i + direction[0] < width and j + direction[1] < height and k < width*height - 1):
						index = get_index(i + direction[0], j + direction[1], k + 1, width, height)
						f_out.write(f"{index} ")
				f_out.write("0\n")
				clause_count += 1
	return clause_count


def encode_input_values(width, height, f_out, input_values):
	clause_count = 0
	for value in input_values:
		if (value[2] > 0):
			index = get_index(value[0], value[1], value[2], width, height)
			f_out.write(f"{index} 0\n")
			clause_count += 1
		else:
			for i in range(width*height):
				index = get_index(value[0], value[1], i, width, height)
				f_out.write(f"{-index} 0\n")
				clause_count += 1
	return clause_count
			

def get_index(column, row, number, width, heigt):
	return (column*(width*heigt**2) + row*(width*heigt) + number + 1)


if __name__ == "__main__":
	args = parser.parse_args([] if "__file__" not in globals() else None)
	encode(args.input_file)