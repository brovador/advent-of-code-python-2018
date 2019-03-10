#encoding: utf-8
import os
import sys
import re
import string

def main(test = ''):
	input_file = './input{0}.txt'.format(test)

	with open(input_file, 'r') as f:
		lines = [l.rstrip() for l in f if l.strip()]
	
	class Group():
		def __init__(self, gid, units, hp, weak, immune, attack, attack_type, initiative, army):
			self.gid = gid
			self.units = int(units)
			self.hp = int(hp)
			self.weak = weak
			self.immune = immune
			self.attack = int(attack)
			self.attack_type = attack_type
			self.initiative = int(initiative)
			self.army = army
		
		def effective_power(self):
			return self.units * self.attack

		def damage_to(self, other):
			damage = g.effective_power()
			if self.attack_type in other.immune:
				damage = 0
			elif self.attack_type in other.weak:
				damage = damage * 2
			return damage
		
		def __str__(self):
			return '{0} group {1}'.format(self.army, self.gid)


	boost_left = 0
	boost_right = 70
	boost = boost_left + (boost_right - boost_left) / 2

	solution_found = False
	debug = False

	while not solution_found:
		print 'trying boost: {0}'.format(boost)
		army = None
		infection_count = 0
		immune_count = 0
		groups = []
		r = re.compile(r'(\d+) units each with (\d+) hit points (\(.+\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)')
		for l in lines:
			if l == 'Immune System:':
				army = 'immune system'
			elif l == 'Infection:':
				army = 'infection'
			else:
				m = r.match(l)
				units, hp, weak_immune, attack, attack_type, initiative = m.groups()
				weak_immune = weak_immune or ''
				weak_immune = map(string.strip, weak_immune.replace('(','').replace(')','').split(';'))
				weak = []
				immune = []

				if army == 'immune system':
					attack = int(attack) + boost

				infection_count += 1 if army == 'infection' else 0
				immune_count += 1 if army == 'immune system' else 0

				for ws in weak_immune:
					if 'weak to' in ws:
						weak = map(string.strip, ws.replace('weak to', '').split(','))
					else:
						immune = map(string.strip, ws.replace('immune to', '').split(','))
				
				gid = infection_count if army == 'infection' else immune_count
				groups.append(Group(gid, units, hp, weak, immune, attack, attack_type, initiative, army))
		
		while True:
			
			immune_system = [g for g in groups if g.army == 'immune system']
			infection = [g for g in groups if g.army == 'infection']

			if debug:
				print 'Immune System:'
				for g in immune_system:
					print 'Group {0} contains {1} units, ep: {2}'.format(g.gid, g.units, g.effective_power())
				
				print 'Infection:'
				for g in infection:
					print 'Group {0} contains {1} units, ep: {2}'.format(g.gid, g.units, g.effective_power())
				print
			
			# target selection phase
			if debug:
				print 'target:'
			attacks = dict()
			groups = sorted(groups, key = lambda g: (-g.effective_power(), -g.initiative))
			for g in groups:
				enemies = [e for e in groups if not e in attacks.values() and g.army != e.army]
				targets = []
				for e in enemies:
					damage = g.damage_to(e)
					if damage:
						targets.append((e, damage))
				if targets:
					target, damage = max(targets, key = lambda x: (x[1], x[0].effective_power(), x[0].initiative))
					attacks[g] = target
					if debug:
						print '{0} targets {1} with damage {2}'.format(g, target, damage)
			
			# attack phase
			if debug:
				print 'attack:'
			groups = sorted(groups, key = lambda g: (-g.initiative))
			zero_kills = True
			for g in groups:
				if g.units == 0 or not g in attacks:
					continue
				target = attacks[g]
				damage = g.damage_to(target)
				units_killed = min(damage / target.hp, target.units)
				target.units = target.units - units_killed
				zero_kills = zero_kills and units_killed == 0
				if debug:
					print '{0} attacks {1} killing {2}'.format(g, target, units_killed)

			groups = [g for g in groups if g.units > 0]

			immune_count = sum([x.units for x in groups if x.army == 'immune system'])
			infection_count = sum([x.units for x in groups if x.army == 'infection'])

			if immune_count == 0 or infection_count == 0 or zero_kills:
				if debug:
					print (boost_left, boost_right, zero_kills)
					print boost, 'is solution?', infection_count == 0
				
				if immune_count == 0 or zero_kills:
					boost_left = boost
				elif infection_count == 0:
					boost_right = boost
				
				if boost_right == boost_left:
					solution_found = True
				elif boost_right - boost_left == 1:
					boost = boost_right if boost == boost_left else boost_left
					boost_left = boost
					boost_right = boost
				else:
					boost = boost_left + (boost_right - boost_left) / 2
				break
	if debug:
		for x in groups:
			print x, x.units
	print sum([x.units for x in groups])



	


if __name__ == '__main__':
	args = ''
	if len(sys.argv) > 1:
		script, args = sys.argv
	main(args)