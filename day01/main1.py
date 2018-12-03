#encoding: utf-8
import os

def main():
	input_file = './input.txt'

	with open(input_file, 'r') as f:
		frequency = sum([int(l.strip()) for l in f])       
        print frequency
	

if __name__ == '__main__':
	main()