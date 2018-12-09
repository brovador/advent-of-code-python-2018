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

	_ids = string.letters
	for i, c in enumerate(coords):
		_id = _ids[i]
		cx, cy = c
		for x in range(max_x + 1):
			for y in range(max_y + 1):
				dist = abs(cx - x) + abs(cy - y)
				m = matrix[y][x]
				if m[0] == '.' or m[1] > dist:
					matrix[y][x] = (_id, dist)
				elif m[1] == dist:
					matrix[y][x] = ('+', dist)
	
	invalid_ids = set([])
	for x in range(max_x + 1):
		invalid_ids.add(matrix[0][x][0])
		invalid_ids.add(matrix[max_y][x][0])
	for y in range(max_y + 1):
		invalid_ids.add(matrix[y][0][0])
		invalid_ids.add(matrix[y][max_x][0])
	
	idx_sum = ''.join([''.join(map(lambda x: str(x[0]), m)) for m in matrix])
	idx_sum = [x for x in Counter(idx_sum).most_common() if x[0] not in invalid_ids]
	print idx_sum[0][1]

if __name__ == '__main__':
	main()