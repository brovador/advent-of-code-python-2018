#encoding: utf-8
import os
import sys
import itertools

class Grid():
	def __init__(self, lines):
		self.rows = len(lines)
		self.cols = len(lines[0])
		self.data = [['.'] * self.cols for r in range(self.rows)]
		for row, line in enumerate(lines):
			for col, c in enumerate(line):
				self.data[row][col] = c
	
	def adjacent_list(self, x, y):
		offsets = range(-1, 2)
		adj_positions = list(itertools.product(offsets, repeat = 2))
		adj_positions.remove((0, 0))
		result = []
		for o in adj_positions:
			ox, oy = map(sum, zip((x, y), o))
			if not self.is_valid_position(ox, oy):
				continue
			result.append(self.data[oy][ox])
		return result

	def resource_value(self):
		acres = 0
		lumberyards = 0
		for row in range(self.rows):
			for col in range(self.cols):
				acres += 1 if self.data[row][col] == '|' else 0
				lumberyards += 1 if self.data[row][col] == '#' else 0
		return acres * lumberyards
	
	def is_valid_position(self, x, y):
		return x >= 0 and y >= 0 and x < self.cols and y < self.rows


	def __str__(self):
		return '\n'.join([''.join(x) for x in self.data])
	
	def __repr__(self):
		return str(self)


def main(test = ''):
	input_file = './input{0}.txt'.format(test)

	with open(input_file, 'r') as f:
		lines = [l.rstrip() for l in f]
	
	grid = Grid(lines)
	minutes = 10

	for minute in range(minutes):
		lines = []
		for row in range(grid.rows):
			line = ''
			for col in range(grid.cols):
				d = grid.data[row][col]
				adj_values = grid.adjacent_list(col, row)
				
				if d == '.':
					line += '|' if adj_values.count('|') >= 3 else '.'
				elif d == '|':
					line += '#' if adj_values.count('#') >= 3 else '|'
				elif d == '#':
					line += '#' if adj_values.count('#') >= 1 and adj_values.count('|') >= 1 else '.'
			lines.append(line)
		grid = Grid(lines)
	print grid.resource_value()
				



	
		

if __name__ == '__main__':
	args = ''
	if len(sys.argv) > 1:
		script, args = sys.argv
	main(args)