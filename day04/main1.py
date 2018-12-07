#encoding: utf-8
import os
import re
from collections import Counter
from datetime import datetime
from random import shuffle

def main():
	input_file = './input.txt'

	with open(input_file, 'r') as f:
		lines = [l.strip() for l in f]

	r = re.compile(r'\[(.+)\] (.+)')
	instructions = []
	for l in lines:
		d, i = r.match(l).groups()
		d = datetime.strptime(d, '%Y-%m-%d %H:%M')
		instructions.append((d, i))
	instructions = sorted(instructions, key = lambda i: i[0])

	current_guard = None
	sleeping = False
	last_d = None
	sleeping_minutes = {}
	
	for ins in instructions:
		d, i = ins
		if last_d and sleeping:
			mins = int((d - last_d).total_seconds() / 60)
			for m in range(last_d.minute, last_d.minute + mins):
				sleeping_minutes.setdefault(current_guard, []).append(m)
		last_d = d
		if 'shift' in i:
			current_guard = int(re.match('Guard #(\d+) begins shift', i).groups()[0])
			sleeping = False
		elif 'wakes up' in i:
			sleeping = False
		elif 'asleep' in i:
			sleeping = True
	
	max_sleeping_guard = max(sleeping_minutes.items(), key = lambda kv: sum(kv[1]))
	print max_sleeping_guard[0] * Counter(max_sleeping_guard[1]).most_common(1)[0][0]


		

	
	
	
	


		


	
	


if __name__ == '__main__':
	main()