#encoding: utf-8
import os
import re

class Cart():
	def __init__(self, row, col, orientation):
		self.row = row
		self.col = col
		self.orientation = orientation
		self.intersections = 0
	
	def move(self, tracks):
		next_coords = { '^' : (-1, 0), 'v' : (1, 0), '>' : (0, 1), '<' : (0, -1) }
		next_row = self.row + next_coords[self.orientation][0]
		next_col = self.col + next_coords[self.orientation][1]
		next_tile = tracks[next_row][next_col]
		next_orientation = self.orientation

		if next_tile == '+':
			orientation_sequence = '^>v<'
			next_orientation = orientation_sequence.index(self.orientation)
			if self.intersections % 3 == 0:
				next_orientation -= 1
			elif self.intersections % 3 == 2:
				next_orientation += 1
			next_orientation = orientation_sequence[next_orientation % len(orientation_sequence)]
			self.intersections += 1
		elif next_tile == '\\':
			next_orientation = ('<^' if self.orientation in '<^' else 'v>').replace(self.orientation, '')
		elif next_tile == '/':
			next_orientation = ('>^' if self.orientation in '^>' else 'v<').replace(self.orientation, '')

		self.row = next_row
		self.col = next_col
		self.orientation = next_orientation


def main():
	input_file = './input.txt'

	with open(input_file, 'r') as f:
		lines = [l.rstrip() for l in f]

	max_rows = len(lines)
	max_cols = max(map(len, lines))
	tracks = [[' '] * max_cols for l in lines]
	
	carts = []
	cart_symbols = '^v><'
	for row, line in enumerate(lines):
		for col, c in enumerate(line):
			if c in cart_symbols:
				carts.append(Cart(row, col, c))
				c = '|' if c == '^' or c == 'v' else '-'
			tracks[row][col] = c
	
	while True:
		crash = None
		
		positions = set(())
		for c in carts:
			pos = (c.col, c.row)
			if pos in positions:
				crash = pos
				break
			positions.add(pos)
		
		if crash:
			print ','.join(map(str, crash))
			break

		carts = sorted(carts, key = lambda c: (c.row, c.col, ))
		map(lambda c: c.move(tracks), carts)


if __name__ == '__main__':
	main()