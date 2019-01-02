#encoding: utf-8
import os
import sys
import re

class Grid():
	def __init__(self, min_x, min_y, max_x, max_y, coords, water_spring):
		self.min_x = min_x - 10
		self.max_x = max_x + 10
		self.min_y = min_y
		self.max_y = max_y
		self.rows = self.max_y - self.min_y + 1
		self.cols = self.max_x - self.min_x + 1
		self.data = [['.'] * self.cols for r in range(self.rows)]
		for coord in coords:
			x = coord[0] - self.min_x
			y = coord[1] - self.min_y
			self.data[y][x] = '#'
	
	def get(self, x, y):
		return self.data[y - self.min_y][x - self.min_x] if self.is_valid_pos(x, y) else '.'
	
	def set(self, x, y, val):
		if self.is_valid_pos(x, y):
			self.data[y - self.min_y][x - self.min_x] = val
	
	def is_valid_pos(self, x, y):
		return x >= self.min_x and x <= self.max_x and y >= self.min_y and y <= self.max_y
	
	def count_water(self):
		count = 0
		for row in range(self.rows):
			for col in range(self.cols):
				count += 1 if self.data[row][col] in '|~' else 0
		return count
	
	def __str__(self):
		return '\n'.join([''.join(x) for x in self.data])
	
	def __repr__(self):
		return str(self)


def find_limit(grid, start_pos, offset_inc = 1):
	result = None
	offset = 0
	x, y = start_pos
	while True:
		offset += offset_inc
		g1 = grid.get(x + offset, y)
		g2 = grid.get(x + offset, y + 1)
		g = ''.join([g1, g2])
		if g == '##' or g == '#~':
			result = ('#', x + offset)
			break
		elif g1 != '#' and g2 in '~#':
			#   .   |   .   |
			#   #   #   ~   ~
			continue
		elif g2 == '.' or g2 == '|':
			#   .  |
			#   .  .
			result = ('.', x + offset)
			break
		else:
			print 'not handled case: ', g
	return result


def main(test = ''):
	input_file = './input{0}.txt'.format(test)

	with open(input_file, 'r') as f:
		lines = [l.rstrip() for l in f]
	
	r = re.compile(r'([xy])=(\d+), ([xy])=(\d+)..(\d+)')
	coords = []
	min_x = min_y = 100000
	max_x = max_y = -100000
	for line in lines:
		axis1, coord1, axis2, coord2_1, coord2_2 = r.match(line).groups()
		coord1 = int(coord1)
		coord2_1 = int(coord2_1)
		coord2_2 = int(coord2_2)
		for c2 in range(coord2_1, coord2_2 + 1):
			c = sorted(((axis1, coord1), (axis2, c2)))
			c = (c[0][1], c[1][1])
			coords.append(c)
			min_x = min(min_x, c[0])
			max_x = max(max_x, c[0])
			min_y = min(min_y, c[1])
			max_y = max(max_y, c[1])
	
	water_spring = [500, min_y]
	grid = Grid(min_x, min_y, max_x, max_y, coords, water_spring)
	water = [water_spring]

	while True:
		
		water_to_remove = []
		water_to_add = []

		for w in water:
			wx, wy = w[0], w[1]
			g1 = grid.get(wx, wy)
			g2 = grid.get(wx, wy + 1)
			g = ''.join([g1, g2])

			if g == '..':
				#base case, advance
				grid.set(wx, wy, '|')
				w[1] += 1
			elif g2 == '|':
				#union case, remove
				grid.set(wx, wy, '|')
				water_to_remove.append(w)
			elif g2 in '#~':
				#fill case
				ltype, lxpos = find_limit(grid, w, -1)
				rtype, rxpos = find_limit(grid, w, 1)
				if ltype == rtype and ltype in '#~':
					for x in range(lxpos + 1, rxpos):
						grid.set(x, wy, '~')
					w[1] -= 1
				elif '.' in (ltype, rtype):
					#overflood case
					for x in range(lxpos + 1, rxpos):
						grid.set(x, wy, '|')
					water_to_remove.append(w)
					if ltype == '.':
						water_to_add.append([lxpos, wy])
					if rtype == '.':
						water_to_add.append([rxpos, wy])
		
		for w in water_to_remove:
			water.remove(w)
		water += water_to_add
		
		all_invalid = True
		for w in water:
			all_invalid = all_invalid and not grid.is_valid_pos(*w)
		if all_invalid:
			break
	print grid.count_water()
		

if __name__ == '__main__':
	args = ''
	if len(sys.argv) > 1:
		script, args = sys.argv
	main(args)