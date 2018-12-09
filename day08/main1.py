#encoding: utf-8
import os

def main():
	input_file = './input.txt'

	with open(input_file, 'r') as f:
		lines = [l.strip() for l in f]

	entries = [int(x) for x in lines[0].split(' ')]
	
	def process_node(entries):
		m_sum = 0
		ch, m = entries[0:2]
		del entries[0:2]
		for c in range(ch):
			m_sum += process_node(entries)
		for m in range(m):
			m_sum += entries[m]
		del entries[0:m + 1]		
		return m_sum
	
	print process_node(entries)


if __name__ == '__main__':
	main()