import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--output_file", default=None, type=str, help="File with hidato solution")
parser.add_argument("--row", default=0, type=int, help="Row count")
parser.add_argument("--column", default=0, type=int, help="Column count")
parser.add_argument("--number_count", default=0, type=int, help="Number count")

def decode(output_file, row, column, number_count):
	width = max(len(str(number_count)), 2)
	
	with open(output_file, "r") as f:
		done = False
		for var in map(int, f.readline().split(" ")):
			if var == 0:
				break
				
			if not done and var > 0:
				output = var % number_count
				if output == 0:
					output = number_count
				print(f"{output:>{width}}", end=" ")
				done = True
				
			if abs(var) % number_count == 0:
				if not done:
					print(f"{'x':>{width}}", end=" ")
				done = False
				
			if abs(var) % (column * number_count) == 0:
				print("\n", end="")
		

if __name__ == "__main__":
	args = parser.parse_args([] if "__file__" not in globals() else None)
	decode(args.output_file, args.row, args.column, args.number_count)