#encoding: utf-8
import os
import sys
import re
import math

def main(test = ''):
	input_file = './input{0}.txt'.format(test)

	with open(input_file, 'r') as f:
		lines = [l.rstrip() for l in f]

	nanobots = []
	r = re.compile(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)')
	for l in lines:
		nanobots.append(map(int, r.match(l).groups()))

	def distance(n1, n2):
		return sum(map(lambda x: abs(x[0] - x[1]), zip(n1[0:3],n2[0:3])))

	def add(p1, p2):
		return map(lambda x: x[0] + x[1], zip(p1, p2))

	min_x = min(nanobots, key = lambda x: x[0])[0]
	min_y = min(nanobots, key = lambda x: x[1])[1]
	min_z = min(nanobots, key = lambda x: x[2])[2]
	cmin = (min_x, min_y, min_z)
	
	max_x = max(nanobots, key = lambda x: x[0])[0]
	max_y = max(nanobots, key = lambda x: x[1])[1]
	max_z = max(nanobots, key = lambda x: x[2])[2]
	cmax = (max_x, max_y, max_z)

	def process_octree(c, r):
		nr = map(lambda x: x / 2 + (0 if x % 2 == 0 or x == 1 else 1), r)
		if nr != [0,0,0]:
			rx, ry, rz = nr
		else:
			rx, ry, rz = [1,1,1]
		
		c1 = add(c, (-rx, -ry, -rz))
		c2 = add(c, ( rx, -ry, -rz))
		c3 = add(c, (-rx,  ry, -rz))
		c4 = add(c, ( rx,  ry, -rz))
		c5 = add(c, (-rx, -ry,  rz))
		c6 = add(c, ( rx, -ry,  rz))
		c7 = add(c, (-rx,  ry,  rz))
		c8 = add(c, ( rx,  ry,  rz))
		c9 = c
		
		best = 0
		candidates = []
		for c in [c1, c2, c3, c4, c5, c6, c7, c8, c9]:
			n = len(nanobots_in_cube(c, nr))
			if n > best:
				candidates = [c]
				best = n
			elif n == best:
				candidates.append(c)
		return candidates, best, nr
	
	def nanobots_in_cube(c, r):
		cmin = map(lambda x: x[0] - x[1], zip(c, r))
		cmax = map(lambda x: x[0] + x[1], zip(c, r))
		
		result = []
		for n in nanobots:
			npos = n[:3]
			nr = n[3]

			cx = max(cmin[0], min(cmax[0], npos[0]))
			cy = max(cmin[1], min(cmax[1], npos[1]))
			cz = max(cmin[2], min(cmax[2], npos[2]))
			
			clamp_pos = (cx, cy, cz)
			
			if distance(npos, clamp_pos) <= nr:
				result.append(n)
		return result
	
	# can't explain why, but we need a big radius here
	r = map(lambda x: (x[1] - x[0]) * 10, zip(cmin, cmax))
	c = map(lambda x: x[0] + x[1], zip(cmin, r))

	candidates = [(c,r, 0)]
	best_n = -1
	result = None
	processed_candidates = set([])
	while len(candidates) > 0:
		candidates = [c for c in candidates if c[2] > best_n and not (tuple(c[0]), tuple(c[1])) in processed_candidates]
		candidates = sorted(candidates, key = lambda x: (x[2], distance([0,0,0], x[1]), distance(x[0], [0,0,0])))
		if not candidates:
			break
		
		candidate, r, n = candidates[0]
		processed_candidates.add((tuple(candidate), tuple(r)))
		del candidates[0]

		new_candidates, new_n, new_r = process_octree(candidate, r)

		if all(map(lambda x: x == 0, new_r)):
			if new_n > best_n:
				result = new_candidates[0]
				best_n = new_n
				print 'best: ', result, best_n
		elif new_n >= best_n:
			candidates += [(c, new_r, new_n) for c in new_candidates]
	print int(distance((0,0,0), map(lambda x: round(x), result)))

if __name__ == '__main__':
	args = ''
	if len(sys.argv) > 1:
		script, args = sys.argv
	main(args)