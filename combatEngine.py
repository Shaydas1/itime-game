import pygame
import random
import time

def react(attacker, defender):
	successful_decider = random.randint(0,100)
	
	damage_a = 0
	damage_d = 0
	result = ""
	
	choice = defender.defensive_mode
	
	if choice == "block" and successful_decider <= 30:
		damage_a = calculate_damage(attacker, defender) * defender.shield
		result = f"{defender.name} blocked and took {damage_a:.0f} damage!"
	elif choice == "dodge" and successful_decider <= 20:
		result = f"{defender.name} dodged!"
	elif choice == "parry" and successful_decider <= 7:
		damage_d = calculate_damage(defender, attacker)
		result = f"{defender.name} parried and counterattacked!"
	else:
		damage_a = calculate_damage(attacker, defender)
		result = (f"{defender.name} took damage.")
		
	return (result,damage_a,damage_d)
	
def calculate_damage(attacker, defender):
	offense = random.randint(attacker.max_damage - 10, attacker.max_damage)
	defence = random.randint(defender.defence - 2, defender.defence)
	damage =  offense - defence
	if damage < 0:
		damage = 0
	
	#print(f"  Damage ... {attacker.max_damage:>2} vs {defender.defence:>2} --> {damage:>2} {offense:>2} {defence:>2}")
		
	return damage
	
def do_combat(attacker, defender):
	# Calculate the results when "attacker" attacks "defender"
	(result, damage_a, damage_d) = react(attacker, defender)
	
	attacker.health -= damage_d
	defender.health -= damage_a
	
	print(f"{attacker.name} attacked {defender.name}. {result} Defender's health is now {defender.health}.")
	

	
