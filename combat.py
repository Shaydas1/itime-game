import pygame
import random
import time

class Fighter():
	def __init__(self, name, health, level, max_damage, defence, shield):
		self.name = name
		self.health = health
		self.level = level
		self.max_damage = max_damage
		self.defence = defence
		self.shield = shield

class Player(Fighter):
	def __init__(self, name, health, level, max_damage, defence, shield):
		super(Player, self).__init__(name, health, level, max_damage, defence, shield)
		
class Mob(Fighter):
	def __init__(self, name, health, level, max_damage, defence, shield):
		super(Mob, self).__init__(name, health, level, max_damage, defence, shield)		

	
def calculate_damage_old(player1, player2):
	(p1_health, p1_max_damage, p1_defense) = player1
	(p2_health, p2_max_damage, p2_defense) = player2
	
	offense = random.randint(p1_max_damage - 10, p1_max_damage)
	defense = random.randint(p2_defense - 2, p2_defense)
	damage =  offense - defense
	if damage < 0:
		damage = 0
	
	print(f"Weird one ... {p1_max_damage:>2} vs {p2_defense:>2} --> {damage:>2} {offense:>2} {defense:>2}")
		
	return damage

def react(attacker, defender, choice):
	successful_decider = random.randint(0,100)
	
	damage_a = 0
	damage_d = 0
	result = ""
	
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
		result = (f"{defender.name} failed and took damage")
		
	return (result,damage_a,damage_d)
	
def calculate_damage(attacker, defender):
	offense = random.randint(attacker.max_damage - 10, attacker.max_damage)
	defence = random.randint(defender.defence - 2, defender.defence)
	damage =  offense - defence
	if damage < 0:
		damage = 0
	
	#print(f"  Damage ... {attacker.max_damage:>2} vs {defender.defence:>2} --> {damage:>2} {offense:>2} {defence:>2}")
		
	return damage
	
level = 55
player1 = Player("Fred",100 + level * 20, level, 20 + 5 * level, 5 + 1 * level, 0.2)

number_of_opponents = 5
opponents = []

for i in range(0,number_of_opponents):
	enemy_type_chance = random.randint(1,10)
	if enemy_type_chance == 1:
		opponents.append(Player(f"Orc{i+1}", 600 * 3, 1, 70, 10 * 5, 0.4))
	elif enemy_type_chance == 2:
		opponents.append(Player(f"Orc{i+1}", 600 / 2, 1, 70 * 3, 10 * 5, 0.4))
	else:
		opponents.append(Player(f"Orc{i+1}", 600, 1, 100, 10, 0.4))
	
#player3 = Player("Orc2", 60, 1, 40, 13, 0.2)
#opponents = [player2, player3]

# Call this function so the Pygame library can initialize itself
pygame.init()
# Create an 800x600 sized screen
screen = pygame.display.set_mode([100, 100])

# Set the title of the window
pygame.display.set_caption('COMBAT!1')

player_target = 0

def find_target():
	global player_target
	number_of_runs = 0
	
	while True:
		if opponents[player_target].health <= 0:
			player_target += 1
		if player_target >= number_of_opponents:
			player_target = 0
		if opponents[player_target].health >= 1:
			break
		if number_of_runs == number_of_opponents:
			break
		number_of_runs += 1
		
done = False
	
while not done:
	# Player 1 turn
	turn = 1
	player_reaction = "block"
	
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		#print(f">>{event}<<")
		if event.type == pygame.KEYDOWN:
			#print(f">>{event.key}<<")
			first_opp = pygame.K_1
			last_opp = pygame.K_1 + number_of_opponents - 1
			if event.key >= first_opp and event.key <= last_opp:
				player_target = event.key - pygame.K_1
	#for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			print(f"{event}")
			if event.key == pygame.K_b:
				player_reaction = "block"
			elif event.key == pygame.K_d:
				player_reaction = "dodge"
			elif event.key == pygame.K_p:
				player_reaction = "parry"
		
				

	(result, damage_a, damage_d) = react(player1,opponents[player_target],"block")
	opponents[player_target].health -= damage_a
	player1.health -= damage_d
	damage1 = damage_a - damage_d
	print(f"  {result}")
	
	opp_damage_string = ""
	opp_health_string = ""
	opp_killed = 0
	for i in range(0,number_of_opponents):
		if opponents[i].health < 0:
			opp_killed += 1
			damage2 = 0
			find_target()
	#		if i == player_target:
	#			player_target += 1
	#			if player_target >= number_of_opponents:
	#				player_target = 0
	#				if 
		
		
		else:	
			(result, damage_a, damage_d) = react(opponents[i],player1,player_reaction)
			player1.health -= damage_a
			opponents[i].health -= damage_d
			damage2 = damage_a - damage_d
			print(f"  {result}")
		opp_damage_string += f"{opponents[i].name} damage={damage2:>3.0f} "
		opp_health_string += f"{opponents[i].health:>4.0f},"
			

	print(f"{player1.name} damage={damage1:>3.0f} {opp_damage_string}	Health = {player1.health:>4.0f},{opp_health_string}")
	
	
	if player1.health < 0 and opp_killed == number_of_opponents:
		print(f"Everyone killed each other!")
		break
	elif player1.health < 0:
		print(f"{player1.name} lost")
		break
	elif opp_killed == number_of_opponents:
		print(f"{player1.name} was victorious!")
		break
		
	time.sleep(3)
	
	

	
