#encoding: utf-8
import os
import sys
import re

def main(test = ''):
	input_file = './input{0}.txt'.format(test)

	with open(input_file, 'r') as f:
		lines = [l.rstrip() for l in f]
	
	samples = []
	test_program = []

	reading_samples = True
	r = re.compile('.+: *\[(\d+), (\d+), (\d+), (\d+)]')
	i = 0
	while i < len(lines):
		line = lines[i]
		i += 1
		if not line:
			continue
		if reading_samples:
			m = r.match(line)
			if m:
				before = map(int, m.groups())
				opcode = [int(x) for x in lines[i].split(' ')]
				i += 1
				
				m = r.match(lines[i])
				i += 1
				
				after = map(int, m.groups())
				samples.append((before, opcode, after))
			else:
				reading_samples = False
		else:
			#reading test program here...
			pass

	def addr(a, b, c): 
		registers[c] = registers[a] + registers[b]
	def addi(a, b, c): 
		registers[c] = registers[a] + b
	def mulr(a, b, c): 
		registers[c] = registers[a] * registers[b]
	def muli(a, b, c): 
		registers[c] = registers[a] * b
	def banr(a, b, c): 
		registers[c] = registers[a] & registers[b]
	def bani(a, b, c): 
		registers[c] = registers[a] & b
	def borr(a, b, c): 
		registers[c] = registers[a] | registers[b]
	def bori(a, b, c): 
		registers[c] = registers[a] | b
	def setr(a, b, c): 
		registers[c] = registers[a]
	def seti(a, b, c): 
		registers[c] = a
	def gtir(a, b, c): 
		registers[c] = a > registers[b]
	def gtri(a, b, c): 
		registers[c] = registers[a] > b
	def gtrr(a, b, c): 
		registers[c] = registers[a] > registers[b]
	def eqir(a, b, c): 
		registers[c] = a == registers[b]
	def eqri(a, b, c): 
		registers[c] = registers[a] == b
	def eqrr(a, b, c): 
		registers[c] = registers[a] == registers[b]

	registers = [0] * 4
	operations = [
		addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr
	]
	
	total = 0
	for sample in samples:
		valid_operations = 0
		for operation in operations:
			before, opcode, after = sample
			registers = list(before)
			operation(*opcode[1:])
			valid_operations += 1 if registers == after else 0
		total += 1 if valid_operations >= 3 else 0
	print total	

if __name__ == '__main__':
	args = ''
	if len(sys.argv) > 1:
		script, args = sys.argv
	main(args)