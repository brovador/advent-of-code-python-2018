#encoding: utf-8
import os
import itertools

def main():
	input_file = './input.txt'

	with open(input_file, 'r') as f:
		lines = [l.strip() for l in f]

	serial_number = int(lines[0])
	
	class Grid():
		def __init__(self, serial_number):
			self.width = 300
			self.height = 300
			self.serial_number = serial_number
			self.grid = [[0] * self.width for i in range(self.height)]
			for y in range(self.height):
				for x in range(self.width):
					self.grid[y][x] = self._calculate_power_level(x + 1, y + 1)
		
		def get(self, cx, cy):
			return self.grid[cy][cx]
		
		def _calculate_power_level(self, cx, cy):
			rack_id = cx + 10
			power_level = rack_id * cy
			power_level += self.serial_number
			power_level *= rack_id
			power_level = power_level / 100 - power_level / 1000 * 10
			power_level -= 5
			return power_level
		
		def power(self, cx, cy, sizex, sizey):
			result = 0
			for y in range(cy, cy + sizey):
				for x in range(cx, cx + sizex):
					result += self.grid[y][x]
			return result
	
	grid = Grid(serial_number)
	
	max_power = 0
	max_power_coords = (0, 0, 0)

	for size in range(300):
		s = size + 1
		start_power = grid.power(0, 0, s - 1, s - 1)

		for y in range(grid.height - s + 1):

			if y > 0:
				#remove previous row
				start_power -= grid.power(0, y - 1, s - 1, 1)
			
			#add new row
			start_power += grid.power(0, y + s - 1, s - 1, 1)
			power = start_power
			
			for x in range(grid.width - s + 1):
				
				if x > 0:
					#remove previous col
					power -= grid.power(x - 1, y, 1, s)
				
				#add latest col
				power += grid.power(x + s - 1, y, 1, s)

				if power > max_power:
					max_power = power
					max_power_coords = (x + 1, y + 1, s)

		print 'Tested size: {0}, max_power: {1}, coords: {2}'.format(s, max_power, max_power_coords)
	
	print max_power
	print ','.join(map(str, max_power_coords))

	



if __name__ == '__main__':
	main()