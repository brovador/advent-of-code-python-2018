#encoding: utf-8
import os
import sys
import re

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
	
	best = max(nanobots, key = lambda x: x[3])
	in_range = [n for n in nanobots if distance(best, n) <= best[3]]
	print len(in_range)

		

	

if __name__ == '__main__':
	args = ''
	if len(sys.argv) > 1:
		script, args = sys.argv
	main(args)