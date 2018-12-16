#encoding: utf-8
import os
import re

def main():
	input_file = './input.txt'

	with open(input_file, 'r') as f:
		lines = [l.strip() for l in f]

	players, last_marble = map(int, re.match('(\d+) players; last marble is worth (\d+) points', lines[0]).groups())

	class Node:
		def __init__(self, val):
			self.val = val
			self.next = None
			self.prev = None
		
		def remove(self):
			if self.prev:
				self.prev.next = self.next
			if self.next:
				self.next.prev = self.prev
		
		def insert_after(self, node):
			self.prev = node
			self.next = node.next
			if node.next:
				node.next.prev = self
			node.next = self

	def print_circle(node_start, node_current, player):
		node = node_start
		s = ['[{0}] '.format(player + 1)]
		while True:
			if node == node_current:
				s.append('({0})'.format(node.val))
			else:
				s.append(' {0} '.format(node.val))
			node = node.next
			if not node or node == node_start:
				break
		print ' '.join(s)

	
	last_marble = last_marble * 100
	scores = [0] * players
	current_marble = 0
	current_player = 0

	node_start = Node(0)
	node_start.next = node_start
	node_start.prev = node_start
	node_current = node_start

	while current_marble < last_marble:
		current_marble += 1
		if current_marble % 23 == 0:
			node_to_remove = node_current
			for i in range(7):
				node_to_remove = node_to_remove.prev
			scores[current_player] += current_marble + node_to_remove.val
			node_current = node_to_remove.next
			node_to_remove.remove()
		else:
			node_new = Node(current_marble)
			node_new.insert_after(node_current.next)
			node_current = node_new
		current_player = (current_player + 1) % players
	print max(scores)


if __name__ == '__main__':
	main()