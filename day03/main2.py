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
	repeats = {}
	for l in lines:
		m = r.match(l)
		_id, x, y, w, h = map(int, m.groups())
		repeats.setdefault(_id, False)
		for _x in range(x, x + w):
			for _y in range(y, h + y):
				val = fabric[_y][_x]
				if val != '.':
					repeats[val] = True
					repeats[_id] = True
				fabric[_y][_x] = _id
	print reduce(lambda x, y: x if not repeats[x] else y, repeats.keys())
	

if __name__ == '__main__':
	main()