#encoding: utf-8
import os
import re

def main():
	input_file = './input.txt'

	with open(input_file, 'r') as f:
		lines = [l.strip() for l in f]

	players, last_marble = map(int, re.match('(\d+) players; last marble is worth (\d+) points', lines[0]).groups())

	def print_status(current_player, current_pos, circle):
		circle = ''.join([' ' + str(m) + ' ' if i != current_pos else '(' + str(m) + ')' for i, m in enumerate(circle)])
		print '[{0}] {1}'.format(current_player, circle)
	
	scores = [0] * players
	current_marble = 0
	current_pos = 0
	current_player = 0
	circle = [0]

	while current_marble < last_marble:
		current_marble += 1
		l = len(circle)
		if current_marble % 23 == 0:
			m7_pos = (current_pos - 7) % l
			scores[current_player] += current_marble + circle[m7_pos]
			del circle[m7_pos]
			current_pos = m7_pos
		else:
			next_pos = (current_pos + 1) % l + 1
			circle.insert(next_pos, current_marble)
			current_pos = next_pos
		current_player = (current_player + 1) % players
	print max(scores)


if __name__ == '__main__':
	main()