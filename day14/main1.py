#encoding: utf-8
import os

def main():
	input_file = './input.txt'

	with open(input_file, 'r') as f:
		lines = [l.rstrip() for l in f]

	recipe = '37'
	pos1 = 0
	pos2 = 1

	def print_state():		
		result = []
		for i, r in enumerate(recipe):
			if i == pos1:
				result.append('({0})'.format(r))
			elif i == pos2:
				result.append('[{0}]'.format(r))
			else:
				result.append(' {0} '.format(r))
		return ''.join(result)

	scoring_recipes = int(lines[0])
	score = ''
	while len(recipe) < scoring_recipes + 10:
		r1 = int(recipe[pos1])
		r2 = int(recipe[pos2])
		recipe += str(r1 + r2)
		pos1 = (pos1 + r1 + 1) % len(recipe)
		pos2 = (pos2 + r2 + 1) % len(recipe)
	print recipe[scoring_recipes:scoring_recipes + 10]
	
	

if __name__ == '__main__':
	main()