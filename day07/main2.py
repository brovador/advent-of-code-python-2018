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
	
	num_workers = 5
	step_time_offset = 60
	workers = [('.', -1)] * num_workers
	total_time = 0
	while steps.keys() or [w for w in workers if w[0] != '.']:
		
		#check completions and clean dependencies
		for i, w in enumerate(workers):
			s, t = w
			if s != '.' and t - 1 < total_time:
				dependencies = [k for k, v in steps.items() if s in v]
				for d in dependencies:
					steps[d].remove(s)
				workers[i] = ('.', -1)

		#check available steps
		next = sorted([k for k, v in steps.items() if v == []])

		#assign to workers
		for i, w in enumerate(workers):
			if w[0] == '.' and len(next):
				n = next[0]
				t = ord(n)
				del next[0]
				del steps[n]
				step_time = (step_time_offset + ord(n) - ord('A') + 1)
				workers[i] = (n, total_time + step_time)
		
		#increment time
		total_time += 1
	
	print total_time - 1

	
if __name__ == '__main__':
	main()