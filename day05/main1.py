#encoding: utf-8
import os

def main():
	input_file = './input.txt'

	with open(input_file, 'r') as f:
		lines = [l.strip() for l in f]

	s = lines[0]
	s = map(ord, s)
	i = 0
	while i < len(s) - 1:
		c1, c2 = s[i], s[i + 1]
		if abs(c1 - c2) == 32:
			s = s[:i] + s[i + 2:]
			i = i - 1 if i > 0 else 0
		else:
			i += 1
	print len(s)


if __name__ == '__main__':
	main()