#encoding: utf-8
import os
import sys
import re
import string

def main(test = ''):
	input_file = './input{0}.txt'.format(test)

	with open(input_file, 'r') as f:
		lines = [l.rstrip() for l in f if l.strip()]

	def manhattan_distance(a, b):
		return sum(map(lambda x: abs(x[1] - x[0]), zip(a, b)))
	
	coords = [map(int,l.split(',')) for l in lines]
	coords = map(tuple, coords)

	distances = [[0] * len(coords) for c in coords]
	for i, c1 in enumerate(coords):
		for j, c2 in enumerate(coords[i + 1:]):
			j = j + i + 1
			d = manhattan_distance(c1, c2)
			distances[i][j] = d
			distances[j][i] = d
	
	constellations = []
	for i, c1 in enumerate(coords):
		c1_constellation = [x for x in constellations if c1 in x]
		if not c1_constellation:
			c1_constellation = set()
			c1_constellation.add(c1)
			constellations.append(c1_constellation)
		else:
			c1_constellation = c1_constellation[0]
		for j, c2 in enumerate(coords):
			if c1 == c2: continue
			dist = distances[i][j]
			if dist > 3:
				continue
			c2_constellation = [x for x in constellations if c2 in x]
			if not c2_constellation:
				c1_constellation.add(c2)
			else:
				c2_constellation = c2_constellation[0]
				if c1_constellation == c2_constellation:
					continue
				c1_constellation |= c2_constellation
				constellations.remove(c2_constellation)
	print len(constellations)

			
			
			

		
			





	


if __name__ == '__main__':
	args = ''
	if len(sys.argv) > 1:
		script, args = sys.argv
	main(args)