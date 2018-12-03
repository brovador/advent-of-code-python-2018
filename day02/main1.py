#encoding: utf-8
import os
from collections import Counter

def main():
	input_file = './input.txt'

	with open(input_file, 'r') as f:
		lines = [l.strip() for l in f]
	
	two_count = 0
	three_count = 0
	for l in lines:
		common = Counter(l).most_common()
		two_count += 1 if [c for c in common if c[1] == 2]  else 0
		three_count += 1 if [c for c in common if c[1] == 3]  else 0
	print two_count * three_count
	

if __name__ == '__main__':
	main()