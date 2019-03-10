#encoding: utf-8
import os
import sys
import re

def main(test = ''):
	input_file = './input{0}.txt'.format(test)

	with open(input_file, 'r') as f:
		lines = [l.rstrip() for l in f]

	class Cave():
		def __init__(self, depth, target):
			self.depth = depth
			self.target = target
			self.cols = target[0] + 1
			self.rows = target[1] + 1
			self.data = [[0] * self.cols for r in range(self.rows)]
		
		def __str__(self):
			result = []
			for r in range(self.rows):
				line = []
				for c in range(self.cols):
					if [r, c] == (0, 0):
						line.append('M')
					elif [r, c] == self.target:
						line.append('T')
					else:
						line.append('.=|'[self.data[r][c] % 3])
				result.append(''.join(line))
			return '\n'.join(result)
		
		def __repr__(self):
			return str(self)
	
	depth = int(lines[0].split(' ')[1])
	target = map(int, lines[1].split(' ')[1].split(','))

	cave = Cave(depth, target)
	risk_level = 0
	
	for y in range(cave.rows):
		for x in range(cave.cols):
			geologic_idx = 0
			pos = [x, y]
			if pos == [0, 0] or pos == target:
				geologic_idx = 0
			elif y == 0:
				geologic_idx = x * 16807
			elif x == 0:
				geologic_idx = y * 48271
			else:
				geologic_idx = cave.data[y - 1][x] * cave.data[y][x - 1]
			erosion_level = (geologic_idx + depth) % 20183
			cave.data[y][x] = erosion_level
			risk_level += erosion_level % 3
	print risk_level

	

if __name__ == '__main__':
	args = ''
	if len(sys.argv) > 1:
		script, args = sys.argv
	main(args)