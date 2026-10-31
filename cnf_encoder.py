import sys

def encode(filename):
	with open(filename, "r") as f_in:
		width, height = map(int, f_in.readline.strip().split(","))
		unknown_count = (width*height)**2
		clause_count = width*height + (((width*height)*(width*height - 1))/2)*(width*height) + (width*height)*8*(width*height-1)
		# width*height = atleast one is true clauses
		# (((width*height)*(width*height - 1))/2)*(width*height) = at most one is true clauses
		# (width*height)*8*(width*height-1) direction clauses
		input_values = [][]
		for line in f_in:
			i, j, value = map(int, line.strip.split(","))
			input_values[i][j] = value
			clause_count += 1
	with open("cnf.txt", "w") as f_out:
		f_out.write(f"p cnf {unknown_count} {clause_count} \n")
		encode_atleast_one(width, height, f_out)
		encode_atmost_one(width, height, f_out)
		encode_directions(width, height, f_out)
		encode_input_values(width, height, f_out, input_values)
	return

def encode_atleast_one(width, height, f_out):
	for i in range(width):
		for j in range(height):
			for k in range(width*height):
				var = get_index(i, j, k, width, height)
				f_out.write(f"{var} ")
			f_out.write("0\n")


def encode_atmost_one(width, height, f_out):
	for i in range(width):
		for j in range(height):
			for k in range(width*height):
				it = get_index(i, j, k, width, height)
				for l in range(it + 1, width*height - it):
					f_out.write(f"{-it} {-l} 0\n")


def encode_directions(width, height, f_out):
	directions = [(1,0), (0,1), (1,1), (-1,0), (0,-1), (-1,-1), (1,-1), (-1,1)]
	for i in range(width):
		for j in range(height):
			for k in range(width*height):
				current = get_index(i, j, k, width, height)
				f_out.write(f"{-current} ")
				for direction in directions:
					if(i + direction[0] >= 0 and j + direction[1] >= 0):
						index = get_index(i + direction[0], j + direction[1], k + 1, width, height)
						f_out.write(f"{index} ")
				f_out.write("0")


def encode_input_values(width, height, f_out, input_values):
	return

def get_index(column, row, number, width, heigt):
	return (column*(width*heigt) + row*heigt + number + 1)


if __name__ == "__main":
	encode()