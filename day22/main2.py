#encoding: utf-8
import os
import sys
import re
import math

def main(test = ''):
	input_file = './input{0}.txt'.format(test)

	with open(input_file, 'r') as f:
		lines = [l.rstrip() for l in f]
	
	class Node():
		def __init__(self, x, y, tool, minutes, target, parent):
			self.x = x
			self.y = y
			self.tool = tool
			self.minutes = minutes
			self.target = target
			self.parent = parent
			self.target_distance = (self.target[0] - self.x) ** 2 + (self.target[1] - self.y) ** 2
			self.target_offset = abs(self.target[0] - self.x) + abs(self.target[1] - self.y)
		
		def predicted_minutes(self):
			return self.minutes + self.target_offset + (0 if self.tool == 'T' else 7)
		
		def __str__(self):
			return '({0},{1}) t:{2} m:{3} d: {4}'.format(self.x, self.y, self.tool, self.minutes, self.target_distance)
		
		def __repr__(self):
			return str(self)

		def __hash__(self):
			return hash((self.x, self.y))

		@staticmethod
		def valid_tools(x, y, cave):
			tools = {
				0 : ['T', 'G'],
				1 : ['G', 'N'],
				2 : ['T', 'N']
			}
			return tools[cave.data[y][x] % 3]
		
		def __eq__(self, other):
			result = (self.x, self.y) == (other.x, other.y)
			result = result and (self.tool == other.tool or abs(self.minutes - other.minutes) == 7)
			return result
		
		def adjacent_nodes(self, cave):
			offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
			result = []
			current_valid_tools = Node.valid_tools(self.x, self.y, cave)
			for offset in offsets:
				(posx, posy) = (self.x + offset[0], self.y + offset[1])
				if posx >= cave.cols or posy >= cave.rows or posx < 0 or posy < 0:
					continue
				
				data = cave.data[posy][posx]
				minutes = self.minutes + 1
				tool = None
				
				#change tool if needed
				new_valid_tools = Node.valid_tools(posx, posy, cave)
				if self.tool in new_valid_tools:
					tool = self.tool
				else:
					tool = [t for t in new_valid_tools if t in current_valid_tools][0]
					minutes += 7
				if not tool:
					continue
				new_node = Node(posx, posy, tool, minutes, self.target, self)
				result.append(new_node)
			return result


	class Cave():
		def __init__(self, depth, target):
			self.depth = depth
			self.target = tuple(target)
			self.cols = target[0] + 50
			self.rows = target[1] + 50
			self.data = [[0] * self.cols for r in range(self.rows)]
		
		def __str__(self, current = None):
			result = []
			for r in range(self.rows):
				line = []
				for c in range(self.cols):
					if current and (r, c) == (current.y, current.x):
						line.append('X')
					elif (r, c) == (0, 0):
						line.append('M')
					elif (r, c) == self.target:
						line.append('T')
					else:
						line.append('.=|'[self.data[r][c] % 3])
				result.append(''.join(line))
			return '\n'.join(result)
		
		def __repr__(self):
			return str(self)
	

	depth = int(lines[0].split(' ')[1])
	target = map(int, lines[1].split(' ')[1].split(','))

	cave = Cave(depth, target)
	for y in range(cave.rows):
		for x in range(cave.cols):
			geologic_idx = 0
			pos = [x, y]
			if pos == [0, 0] or pos == target:
				geologic_idx = 0
			elif y == 0:
				geologic_idx = x * 16807
			elif x == 0:
				geologic_idx = y * 48271
			else:
				geologic_idx = cave.data[y - 1][x] * cave.data[y][x - 1]
			erosion_level = (geologic_idx + depth) % 20183
			cave.data[y][x] = erosion_level
	
	start = Node(0, 0, 'T', 0, target, None)
	current = start

	record_time = 10000000000000
	open_nodes = dict()
	visited_nodes = dict()

	open_nodes[(start.x, start.y, start.tool)] = start

	while open_nodes:
		current = min(open_nodes.values(), key = lambda x: x.predicted_minutes())
		current_key = (current.x, current.y, current.tool)

		del open_nodes[current_key]
		visited_nodes[current_key] = current


		if current_key[0:2] == tuple(target):
			if current.tool != 'T':
				current.minutes += 7
			if current.minutes < record_time:
				record_time = current.minutes
				new_nodes = dict()
				for k, v in open_nodes.iteritems():
					if v.predicted_minutes() < record_time:
						new_nodes[k] = v
				open_nodes = new_nodes
				print 'new record:', record_time, len(open_nodes)
			continue
		
		adjacent = current.adjacent_nodes(cave)
		for n in adjacent:
			n_key = (n.x, n.y, n.tool) 
			if n.predicted_minutes() >= record_time:
				continue
			elif n_key in visited_nodes:
				old_n = visited_nodes[n_key]
				if old_n.minutes > n.minutes:
					del visited_nodes[n_key]
					open_nodes[n_key] = n
			elif n_key in open_nodes:
				old_n = open_nodes[n_key]
				if old_n.minutes > n.minutes:
					open_nodes[n_key] = n
			else:
				open_nodes[n_key] = n
	print record_time

if __name__ == '__main__':
	args = ''
	if len(sys.argv) > 1:
		script, args = sys.argv
	main(args)