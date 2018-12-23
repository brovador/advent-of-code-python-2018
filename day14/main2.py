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

	score_to_find = lines[0]
	score = ''
	while True:
		r1 = int(recipe[pos1])
		r2 = int(recipe[pos2])
		recipe += str(r1 + r2)
		if score_to_find in recipe[-len(score_to_find) - 1:]:
			break
		l = len(recipe)
		pos1 = (pos1 + r1 + 1) % l
		pos2 = (pos2 + r2 + 1) % l
	idx = recipe.index(score_to_find)
	print len(recipe[0:idx])
	
	

if __name__ == '__main__':
	main()