#encoding: utf-8
import os
import re
import sys

def main():
	input_file = './input.txt'

	with open(input_file, 'r') as f:
		lines = [l.strip() for l in f]

	r = re.compile(r'position=<([- \d]+),([- \d]+)> velocity=<([- \d]+),([- \d]+)>')
	
	data = map(lambda x: map(int, r.match(x).groups()), lines)
	
	class Matrix():
		def __init__(self, min_x, min_y, max_x, max_y):
			self.center = (-min_x, -min_y)
			self.cols = max_x - min_x + 1
			self.rows = max_y - min_y + 1
			self.m = [['.'] * self.cols for i in range(self.rows)]
		
		def set_coord(self, coord, val):
			cx = self.center[0] + coord[0]
			cy = self.center[1] + coord[1]
			self.m[cy][cx] = val
		
		def __str__(self):
			return '\n'.join(map(lambda m: ''.join(m), self.m))

	seconds = 0
	min_x = -sys.maxint
	min_y = -sys.maxint
	max_x = sys.maxint
	max_y = sys.maxint
	while True:
		new_min_x = sys.maxint
		new_min_y = sys.maxint
		new_max_x = -sys.maxint
		new_max_y = -sys.maxint

		for d in data:
			cx, cy, vx, vy = d
			cx = cx + vx
			cy = cy + vy
			d[0] = cx
			d[1] = cy
			new_min_x = min(new_min_x, cx)
			new_min_y = min(new_min_y, cx)
			new_max_x = max(new_max_x, cx)
			new_max_y = max(new_max_y, cx)

		streched = False
		streched = streched or new_min_x > min_x
		streched = streched or new_min_y > min_y
		streched = streched or new_max_x < max_x
		streched = streched or new_max_y < max_y

		if streched:
			min_x = max(new_min_x, min_x)
			min_y = max(new_min_y, min_y)
			max_x = min(new_max_x, max_x)
			max_y = min(new_max_y, max_y)
			seconds += 1
		else:
			#undo last iteration
			for d in data:
				cx, cy, vx, vy = d
				cx = cx - vx
				cy = cy - vy
				d[0] = cx
				d[1] = cy
			break
	matrix = Matrix(min_x, min_y, max_x, max_y)
	for d in data:
		matrix.set_coord(d[0:2], '#')
	print matrix
	print seconds
	



if __name__ == '__main__':
	main()