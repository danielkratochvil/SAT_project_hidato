import sys

def encode(filename):
	with open(filename, "r") as f_in:
		width, height = map(int, f_in.readline.strip().split(","))
		unknown_count = (width*height)**2
		clause_count = width*height + ((width*height)*(width*height - 1))/2 + (width*height)*8*(width*height-1)
		# width*height = atleast one is true clauses
		# ((width*height)*(width*height - 1))/2 = at most one is true clauses
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
	

def encode_atmost_one(width, height, f_out):

def encode_directions(width, height, f_out):

def encode_input_values(width, height, f_out, input_values):


if __name__ == "__main":
	encode()