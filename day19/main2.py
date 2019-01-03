#encoding: utf-8
import os
import sys
import re

def main(test = ''):
	input_file = './input{0}.txt'.format(test)

	with open(input_file, 'r') as f:
		lines = [l.rstrip() for l in f]
	
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

	operations = {
		'addr' : addr, 'addi' : addi, 'mulr' : mulr, 'muli' : muli, 
		'banr' : banr, 'bani' : bani, 'borr' : borr, 'bori' : bori,
		'setr' : setr, 'seti' : seti, 'gtir' : gtir, 'gtri' : gtri,
		'gtrr' : gtrr, 'eqir' : eqir, 'eqri' : eqri, 'eqrr' : eqrr,
	}

	s = '''
	result achived after analyzing the code and the different loops on it
	code is obtaining divisors of the number: 10551389 and adding them together:
	'''
	print s
	n = 10551389
	print sum([x for x in range(1, n / 2) if n % x == 0]) + n

	

if __name__ == '__main__':
	args = ''
	if len(sys.argv) > 1:
		script, args = sys.argv
	main(args)