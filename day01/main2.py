#encoding: utf-8
import os

def main():
	input_file = './input.txt'

	with open(input_file, 'r') as f:
		lines = [int(l.strip()) for l in f]
    
	frequency = 0
	line_idx = 0
	frequencies = set([frequency])
	while True:
		frequency += lines[line_idx % len(lines)]
		if frequency in frequencies:
			break
		frequencies.add(frequency)
		line_idx += 1
	print frequency
			

if __name__ == '__main__':
	main()