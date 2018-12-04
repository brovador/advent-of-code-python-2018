#encoding: utf-8
import os
import re

def main():
	input_file = './input.txt'

	with open(input_file, 'r') as f:
		lines = [l.strip() for l in f]

	def debug(fabric):
		print '\n'.join([' '.join(x) for x in fabric])
	
	w, h = 1000, 1000
	fabric = [['.'] * w for i in range(h)]

	r = re.compile(r'\#(\d+) \@ (\d+),(\d+): (\d+)x(\d+)')
	for l in lines:
		m = r.match(l)
		_id, x, y, w, h = map(int, m.groups())
		for _x in range(x, x + w):
			for _y in range(y, h + y):
				fabric[_y][_x] = str(_id) if fabric[_y][_x] == '.' else 'x'
	print sum([len([x for x in f if x == 'x']) for f in fabric])


if __name__ == '__main__':
	main()