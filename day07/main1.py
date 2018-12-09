#encoding: utf-8
import os
import re

def main():
	input_file = './input.txt'

	with open(input_file, 'r') as f:
		lines = [l.strip() for l in f]

	r = re.compile('Step (.+) must be finished before step (.+) can begin.')
	steps = {}
	for l in lines:
		pred, step = r.match(l).groups()
		steps.setdefault(pred, [])
		steps.setdefault(step, []).append(pred)
	
	order = []
	while steps.keys():
		n = sorted([k for k, v in steps.items() if v == []])[0]
		order.append(n)
		del steps[n]
		dependencies = [k for k, v in steps.items() if n in v]
		for d in dependencies:
			steps[d].remove(n)
	print ''.join(order)

	
if __name__ == '__main__':
	main()