#encoding: utf-8
import os
import string
import itertools
from collections import Counter

def main():
	input_file = './input.txt'

	with open(input_file, 'r') as f:
		lines = [l.strip() for l in f]

	coords = [tuple(map(int, l.split(', '))) for l in lines]
	
	min_x = min([c[0] for c in coords])
	max_x = max([c[0] for c in coords])
	min_y = min([c[1] for c in coords])
	max_y = max([c[1] for c in coords])
	
	matrix = [[('.', 0)] * (max_x + 1) for y in range(max_y + 1)]
	def print_matrix():
		print '\n'.join([''.join(map(lambda x: str(x[0]), m)) for m in matrix])

	max_sum = 10000
	safe_coords = []
	for x in range(max_x + 1):
		for y in range(max_y + 1):
			dist_sum = 0
			for c in coords:
				cx, cy = c
				dist_sum += abs(cx - x) + abs(cy - y)
				if dist_sum >= max_sum:
					break
			else:
				safe_coords.append((x, y))
				matrix[y][x] = ('#', dist_sum)
	
	print len(safe_coords)

if __name__ == '__main__':
	main()