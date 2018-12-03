#encoding: utf-8
import os

def main():
	input_file = './input.txt'

	with open(input_file, 'r') as f:
		lines = [l.strip() for l in f]
	
	# Fast solution
	# ====================
	lines = [map(ord, l) for l in lines]
	for i, l1 in enumerate(lines):
		for l2 in lines[i + 1:]:
			diff_idx = -1
			for j, c1 in enumerate(l1):
				c2 = l2[j]
				if c2 != c1 and diff_idx != -1:
					break
				elif c2 != c1:
					diff_idx = j
			else:
				if diff_idx != -1:
					print ''.join([chr(l) for i, l in enumerate(lines[i]) if i != diff_idx])
					
				
	
	# Brute force solution
	# ====================
	# for i, l1 in enumerate(lines):
	# 	for l2 in lines[i + 1:]:
	# 		for j in range(len(l2)):
	# 			_l1 = l1[:j] + l1[j + 1:]
	# 			_l2 = l2[:j] + l2[j + 1:]
	# 			if _l1 == _l2:
	# 				print _l1
	# 				return
	
			

if __name__ == '__main__':
	main()