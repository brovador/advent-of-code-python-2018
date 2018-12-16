#encoding: utf-8
import os
import itertools

def main():
	input_file = './input.txt'

	with open(input_file, 'r') as f:
		lines = [l.strip() for l in f]

	serial_number = int(lines[0])
	width = 300
	height = 300
	grid = [[0] * width for i in range(height)]

	def calculate_power_level(cx, cy, serial_number):
		rack_id = cx + 10
		power_level = rack_id * cy
		power_level += serial_number
		power_level *= rack_id
		power_level = power_level / 100 - power_level / 1000 * 10
		power_level -= 5
		return power_level

	for y in range(height):
		for x in range(width):
			grid[x][y] = calculate_power_level(x + 1, y + 1, serial_number)
	
	max_power = 0
	max_power_coords = (0, 0)
	offsets = list(itertools.product([-1, 0, 1], repeat = 2))

	for y in range(1, height - 1):
		for x in range(1, width - 1):
			power = sum(map(lambda o: grid[o[0] + x][o[1] + y], offsets))
			
			if power > max_power:
				max_power = power
				max_power_coords = (x, y)
	
	print ','.join(map(str, max_power_coords))

	



if __name__ == '__main__':
	main()