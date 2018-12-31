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
	registers = [0] * 4

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
				i -= 1
		else:
			test_program.append(map(int, line.split(' ')))

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
		registers[c] = 1 if a > registers[b] else 0
	def gtri(a, b, c): 
		registers[c] = 1 if registers[a] > b else 0
	def gtrr(a, b, c): 
		registers[c] = 1 if registers[a] > registers[b] else 0
	def eqir(a, b, c): 
		registers[c] = 1 if a == registers[b] else 0
	def eqri(a, b, c): 
		registers[c] = 1 if registers[a] == b else 0
	def eqrr(a, b, c): 
		registers[c] = 1 if registers[a] == registers[b] else 0

	opcodes = [
		addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr
	]

	opcodes_numbers = []
	for opcode in opcodes:
		valid_opcode_numbers = set([])
		invalid_opcode_numbers = set([])
		for sample in samples:
			before, operation, after = sample
			opcode_number, args = operation[0], operation[1:]
			registers = list(before)
			opcode(*args)
			if registers == after:
				valid_opcode_numbers.add(opcode_number)
			else:
				invalid_opcode_numbers.add(opcode_number)
		valid_opcode_numbers -= invalid_opcode_numbers
		opcodes_numbers.append(valid_opcode_numbers)
	

	def assign(current_assign):
		next_idx = len(current_assign)
		if next_idx == len(opcodes):
			return current_assign
		next_candidate = opcodes_numbers[next_idx]
		next_candidate = [x for x in next_candidate if not x in current_assign]
		if not next_candidate:
			return None
		for c in next_candidate:
			result = assign(current_assign[:] + [c])
			if result:
				break
		return result
	
	assigned_opcodes = assign([])
	
	opcodes = dict(zip(assigned_opcodes, opcodes))
	registers = [0] * 4
	for l in test_program:
		opcode = l[0]
		args = l[1:]
		opcodes[opcode](*args)
	print registers[0]

if __name__ == '__main__':
	args = ''
	if len(sys.argv) > 1:
		script, args = sys.argv
	main(args)