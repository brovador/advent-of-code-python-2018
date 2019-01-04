#encoding: utf-8
import os
import sys

class Room:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.N = None
		self.S = None
		self.E = None
		self.W = None
	
	def pos(self):
		return (self.x, self.y)
	
	def __str__(self):
		return 'Room {0} N: {1}, S: {2}, E: {3}, W: {4}'.format(self.pos(), self.N, self.S, self.E, self.W)
	
	def __repr__(self):
		return str(self)

paths_count = {}

def main(test = ''):
	input_file = './input{0}.txt'.format(test)

	with open(input_file, 'r') as f:
		lines = [l.rstrip() for l in f]
	
	current_room = Room(0, 0)
	start_room = current_room
	rooms = {
		(0, 0) : current_room
	}
	line = lines[0]
	
	def process_branch(line, current_room, rooms):
		i = 0
		while i < len(line):
			c = line[i]
			i += 1
			if c in '^$':
				continue
			elif c in 'NSEW':
				new_room = Room(current_room.x, current_room.y)
				if c == 'N':
					new_room.y -= 1
					current_room.N = new_room.pos()
					new_room.S = current_room.pos()
				elif c == 'S':
					new_room.y += 1
					current_room.S = new_room.pos()
					new_room.N = current_room.pos()
				elif c == 'E':
					new_room.x += 1
					current_room.E = new_room.pos()
					new_room.W = current_room.pos()
				elif c == 'W':
					new_room.x -= 1
					current_room.W = new_room.pos()
					new_room.E = current_room.pos()
				current_room = new_room
				if current_room.pos() in rooms:
					old_room = rooms[current_room.pos()]
					current_room.N = current_room.N or old_room.N
					current_room.S = current_room.S or old_room.S
					current_room.E = current_room.E or old_room.E
					current_room.W = current_room.W or old_room.W
				rooms[current_room.pos()] = current_room
			elif c == '(':
				open_branches = 1
				option_start_idx = i
				options = []
				j = i
				while open_branches > 0:
					c = line[j]
					j += 1
					if c == '|' and open_branches == 1:
						options.append((option_start_idx, j - 1))
						option_start_idx = j
					elif c == '(':
						open_branches += 1
					elif c == ')':
						open_branches -= 1
						if open_branches == 0:
							options.append((option_start_idx, j - 1))
				
				base_room_pos = current_room.pos()
				for o in options:
					branch = line[o[0]:o[1]]
					process_branch(branch, current_room, rooms)
				current_room = rooms[base_room_pos]
				i = j
	
	process_branch(line, current_room, rooms)
	def find_path(room, current_path, best_path):

		global paths_count
		current_distance = paths_count.get(current_path[-1], 100000000)
		paths_count[current_path[-1]] = min(current_distance, len(current_path) - 1)

		choices = [x for x in [room.N, room.S, room.W, room.E] if x and not x in current_path]
		if not choices:
			return current_path if len(current_path) > len(best_path) else best_path
		else:
			for choice in choices:
				result = find_path(rooms[choice], current_path[:] + [choice], best_path)
				if len(result) > len(best_path):
					best_path = result
			return result
	
	sys.setrecursionlimit(10000)
	result = find_path(start_room, [start_room.pos()], [])
	print len([x for x in paths_count.values() if x >= 1000])

	# positions = sorted(rooms.keys())
	# min_pos = positions[0]
	# max_pos = positions[-1]
	# cols = max_pos[0] - min_pos[0] + 1
	# rows = max_pos[1] - min_pos[1] + 1
	
	# data_cols = 2 * cols + 1
	# data_rows = 2 * rows + 1
	# data = [['#'] * data_cols for r in range(data_rows)]
	# for pos in positions:
	# 	room = rooms[pos]
	# 	x, y = pos
	# 	posx = x - min_pos[0]
	# 	posy = y - min_pos[1]
	# 	datax = 2 * posx + 1
	# 	datay = 2 * posy + 1
	# 	data[datay][datax] = '.' if room != start_room else 'X'
	# 	if room.N:
	# 		data[datay - 1][datax] = '-'
	# 	if room.S:
	# 		data[datay + 1][datax] = '-'
	# 	if room.E:
	# 		data[datay][datax + 1] = '|'
	# 	if room.W:
	# 		data[datay][datax - 1] = '|'
	
	# print '\n'.join([''.join(x) for x in data])

		

		
		
	

	

if __name__ == '__main__':
	args = ''
	if len(sys.argv) > 1:
		script, args = sys.argv
	main(args)