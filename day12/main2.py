#encoding: utf-8
import os
import re

def main():
	input_file = './input.txt'

	with open(input_file, 'r') as f:
		lines = [l.strip() for l in f]

	initial_state,  = re.match(r'initial state: (.+)', lines[0]).groups()
	
	r = re.compile(r'(.+) => (.)')
	rules = {}
	for l in lines[2:]:
		k, v = r.match(l).groups()
		rules[k] = v
	
	generations = 50000000000
	pots = {}
	for i, s in enumerate(initial_state):
		pots[i] = s

	pots[-2] = '.'
	pots[-1] = '.'
	pots[len(initial_state)] = '.'
	pots[len(initial_state) + 1] = '.'
	
	offsets = range(-2, 3)
	g = 0
	prev_sum = 0
	prev_diff = 0
	stable_count = 0
	while g < generations:
		new_pots = {}
		pot_ids = sorted(pots.keys())
		for pid in pot_ids:
			s = ''.join(map(lambda x: pots.setdefault(x + pid, '.'), offsets))
			new_pots[pid] = rules.get(s, '.')
		pots.update(new_pots)
		
		s = sum([x for x in pots.keys() if pots[x] == '#'])

		stable_count = stable_count + 1 if s - prev_sum == prev_diff else 0
		
		if stable_count == 5:
			print s + (generations - g - 1) * (prev_diff)
			break
		
		prev_diff = s - prev_sum
		prev_sum = s
		
		g += 1


if __name__ == '__main__':
	main()