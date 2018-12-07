#encoding: utf-8
import os

def main():
	input_file = './input.txt'

	with open(input_file, 'r') as f:
		lines = [l.strip() for l in f]

	line = map(ord, lines[0])
	removes = set(map(ord, lines[0].lower()))
	best = len(line)
	for r in removes:
		s = filter(lambda x: x != r and x + 32 != r, line)
		i = 0
		while i < len(s) - 1:
			c1, c2 = s[i], s[i + 1]
			if abs(c1 - c2) == 32:
				s = s[:i] + s[i + 2:]
				i = i - 1 if i > 0 else 0
			else:
				i += 1
		if len(s) < best:
			best = len(s)
	print best


if __name__ == '__main__':
	main()