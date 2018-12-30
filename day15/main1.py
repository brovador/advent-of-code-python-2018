#encoding: utf-8
import os
import sys

class Unit:
	def __init__(self, unit_type, row, col):
		self.unit_type = unit_type
		self.row = row
		self.col = col
		self.hit_points = 200
		self.attack_power = 3
	
	def valid_attack_targets(self, targets):
		result = []
		near_positions = adjacent_positions(self.row, self.col)
		for t in targets:
			if (t.row, t.col) in near_positions:
				result.append(t)
		return result
	
	def position(self):
		return (self.row, self.col)

	def __str__(self):
		return '{0}({1},{2}) HP:{3}'.format(self.unit_type, self.row, self.col, self.hit_points)
	
	def __repr__(self):
		return str(self)


def adjacent_positions(rpos, cpos):
	return map(lambda o: (rpos + o[0], cpos + o[1]), [(0, -1), (-1, 0), (0, 1), (1, 0)])


def is_valid_pos(map_tiles, rpos, cpos, is_free = True):
	result = True
	result = result and rpos >= 0 and rpos < len(map_tiles) 
	result = result and cpos >= 0 and cpos < len(map_tiles[0])
	if is_free:
		result = result and map_tiles[rpos][cpos] == '.'
	return result

def reachable_targets(unit, dest_pos, map_tiles):
	result = []
	unit_adjacents = [x for x in adjacent_positions(*unit.position()) if is_valid_pos(map_tiles, *x)]
	open_positions = dest_pos
	visited_positions = []
	while open_positions:
		new_positions = []
		for pos in open_positions:
			visited_positions.append(pos)
			if pos in unit_adjacents:
				result.append(pos)
				continue
			for offset_pos in adjacent_positions(*pos):
				if not offset_pos in new_positions:
					new_positions.append(offset_pos)
		if result:
			break
		open_positions = [pos for pos in new_positions if pos not in visited_positions and is_valid_pos(map_tiles, *pos)]
	return result


def main(test = ''):
	input_file = './input{0}.txt'.format(test)

	with open(input_file, 'r') as f:
		lines = [l.rstrip() for l in f]

	map_tiles = [['#'] * len(lines[0]) for l in lines]
	units = []

	def print_map():
		return '\n'.join(map(''.join, map_tiles))
	
	for row, line in enumerate(lines):
		for col, c in enumerate(line):
			map_tiles[row][col] = c
			if c in 'EG':
				units.append(Unit(c, row, col))

	rounds = 0
	while True:

		units = sorted(units, key = lambda u: (u.row, u.col, ))
		units = [u for u in units if u.hit_points > 0]

		combat_ended = False

		for i, unit in enumerate(units):
			#skip units killed during turn
			if unit.hit_points < 0:
				continue

			#targets
			targets = [x for x in units if x.unit_type != unit.unit_type and x.hit_points > 0]
			combat_ended = not targets

			if combat_ended:
				break

			#check if can attack
			attack_targets = unit.valid_attack_targets(targets)
			
			if not attack_targets:
				paths = {}
				
				#in range
				in_range = []
				for target in targets:
					pos = target.position()
					for offset_pos in adjacent_positions(*pos):
						if is_valid_pos(map_tiles, *offset_pos) and not offset_pos in in_range:
							in_range.append(offset_pos)
				
				#reachable
				reachable = reachable_targets(unit, in_range, map_tiles)
				
				if reachable:
					reachable = sorted(reachable)
					step = reachable[0]

					#move
					map_tiles[unit.row][unit.col] = '.'
					map_tiles[step[0]][step[1]] = unit.unit_type
					unit.row = step[0]
					unit.col = step[1]
					
					#search targets to attack again
					attack_targets = unit.valid_attack_targets(targets)
			
			if attack_targets:
				attack_targets = sorted(attack_targets, key = lambda x: (x.hit_points, x.row, x.col))
				attack_target = attack_targets[0]
				attack_target.hit_points -= unit.attack_power

				if attack_target.hit_points <= 0:
					map_tiles[attack_target.row][attack_target.col] = '.'
		
		if combat_ended:
			result = rounds * sum([x.hit_points for x in units if x.hit_points > 0])
			print result
			break
		rounds += 1

	
	

	

if __name__ == '__main__':
	args = ''
	if len(sys.argv) > 1:
		script, args = sys.argv
	main(args)