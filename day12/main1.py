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
	
	generations = 20
	pots = {}
	for i, s in enumerate(initial_state):
		pots[i] = s

	pots[-2] = '.'
	pots[-1] = '.'
	pots[len(initial_state)] = '.'
	pots[len(initial_state) + 1] = '.'
	
	offsets = range(-2, 3)
	for g in range(generations):
		new_pots = {}
		pot_ids = sorted(pots.keys())
		for pid in pot_ids:
			s = ''.join(map(lambda x: pots.setdefault(x + pid, '.'), offsets))
			new_pots[pid] = rules.get(s, '.')
		pots.update(new_pots)
	print sum([x for x in pots.keys() if pots[x] == '#'])


if __name__ == '__main__':
	main()