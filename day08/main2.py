#encoding: utf-8
import os
import string

def main():
	input_file = './input.txt'

	with open(input_file, 'r') as f:
		lines = [l.strip() for l in f]

	entries = [int(x) for x in lines[0].split(' ')]
	
	def process_node(entries, i):
		
		ch, m = entries[0:2]
		del entries[0:2]
		
		child_values = []
		for c in range(ch):
			child_values.append(process_node(entries, i + 1))
		
		metadata = entries[0: m]
		del entries[0:m]
		
		val = sum(metadata) 
		if ch > 0:
			val = sum([child_values[m - 1] for m in metadata if m < len(child_values) + 1])
		
		return val
	
	print process_node(entries, 0)

	
if __name__ == '__main__':
	main()