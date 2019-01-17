"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/

From:
http://programarcadegames.com/python_examples/f.php?file=maze_runner.py

Explanation video: http://youtu.be/5-SbFanyUkQ

Part of a series:
http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py
http://programarcadegames.com/python_examples/f.php?file=maze_runner.py
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py
http://programarcadegames.com/python_examples/f.php?file=platform_moving.py
http://programarcadegames.com/python_examples/sprite_sheets/
"""
import pygame
import random
from combatEngine import do_combat

BLACK  = (   0,   0,   0)
WHITE  = ( 255, 255, 255)
BLUE   = (   0,   0, 255)
GREEN  = (   0, 255,   0)
RED    = ( 255,   0,   0)
PURPLE = ( 255,   0, 255)
LIGHT_GRAY = (60, 60, 60)


class Wall(pygame.sprite.Sprite):
	"""This class represents the bar at the bottom that the player controls """

	def __init__(self, x, y, width, height, color):
		""" Constructor function """

		# Call the parent's constructor
		super().__init__()

		# Make a BLUE wall, of the size specified in the parameters
		self.image = pygame.Surface([width, height])
		self.image.fill(color)

		# Make our top-left corner the passed-in location.
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x

class TeleportWall(Wall):
	def __init__(self, x, y, width, height, color, new_room):
		super().__init__(x, y, width, height, color)
		
		self.new_room = new_room
		
	def teleport(self):
		print("Teleporting!")

class Character(pygame.sprite.Sprite):
	def __init__(self, x, y, color, name, health, level, max_damage, defence, shield, attack_time, defensive_mode):
	
		super().__init__()
		
		self.image = pygame.Surface([15, 15])
		self.image.fill(color)
		
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x
		
		self.name = name
		self.health = health
		self.level = level
		self.max_damage = max_damage
		self.defence = defence
		self.shield = shield		
		self.defensive_mode = defensive_mode
		
		self.attack_time = attack_time
		self.next_attack = 0
		
	def move(self, walls, dx, dy):
		""" Find a new position for the player """
		# Move left/right
		self.rect.x += dx

		special_block = None
		
		# Did this update cause us to hit a wall?
		block_hit_list = pygame.sprite.spritecollide(self, walls, False)
		for block in block_hit_list:
			if type(block) is TeleportWall:
				special_block = block
		
			# If we are moving right, set our right side to the left side of
			# the item we hit
			if dx > 0:
				self.rect.right = block.rect.left
			else:
				# Otherwise if we are moving left, do the opposite.
				self.rect.left = block.rect.right

		# Move up/down
		self.rect.y += dy

		# Check and see if we hit anything
		block_hit_list = pygame.sprite.spritecollide(self, walls, False)
		for block in block_hit_list:
			if type(block) is TeleportWall:
				special_block = block
		
			# Reset our position based on the top/bottom of the object.
			if dy > 0:
				self.rect.bottom = block.rect.top
			else:
				self.rect.top = block.rect.bottom
				
		return special_block
			

class Mob(Character):
	
	def __init__(self, x, y, name, health, level, max_damage, defence, shield):
		super().__init__(x, y, RED, name, health, level, max_damage, defence, shield, 1000, "block")
		
	def move(self, walls, player_x, player_y, max_distr):
		""" Find a new position for the player """
		
		dist_x = player_x - self.rect.x
		dist_y = player_y - self.rect.y
		if abs(dist_x) < 40 and abs(dist_y) < 40:
			self.image.fill(BLUE)
		else:
			self.image.fill(RED)
		#Cap the distance moved with the max_distr input
		if dist_x > max_distr:
			dist_x = max_distr
		elif dist_x < -max_distr:
			dist_x = -max_distr

		if dist_y > max_distr:
			dist_y = max_distr
		elif dist_y < -max_distr:
			dist_y = -max_distr
			
		dx = dist_x + random.randint(-5,5)
		dy = dist_y + random.randint(-5,5)
		
		super().move(walls, dx, dy)
			
class Player(Character):
	""" This class represents the bar at the bottom that the player controls """

	# Set speed vector
	change_x = 0
	change_y = 0

	def __init__(self, x, y, name, health, level, max_damage, defence, shield):
		""" Constructor function """

		# Call the parent's constructor
		super().__init__(x, y, WHITE, name, health, level, max_damage, defence, shield, 500, "parry")
		
	def changespeed(self, x, y):
		""" Change the speed of the player. Called with a keypress. """
		self.change_x += x
		self.change_y += y

	def move(self, walls):
		""" Find a new position for the player """
		teleportblock = super().move(walls, self.change_x, self.change_y)
		
		return teleportblock


class Room(object):
	""" Base class for all rooms. """

	""" Each room has a list of walls, and of enemy sprites. """
	wall_list = None
	enemy_sprites = None

	def __init__(self):
		""" Constructor, create our lists. """
		self.wall_list = pygame.sprite.Group()
		self.enemy_sprites = pygame.sprite.Group()

class Room1(Room):
	"""This creates all the walls in room 1"""
	def __init__(self):
		Room.__init__(self)
		# Make the walls. (x_pos, y_pos, width, height)

		# This is a list of walls. Each is in the form [x, y, width, height]
		walls = [[0, 0, 20, 250, WHITE],
				 [0, 350, 20, 250, WHITE],
				 [780, 0, 20, 250, WHITE],
				 [780, 350, 20, 250, WHITE],
				 [20, 0, 760, 20, WHITE],
				 [20, 580, 760, 20, WHITE],
				 [390, 50, 20, 500, BLUE]
				]

		# Loop through the list. Create the wall, add it to the list
		for item in walls:
			wall = Wall(item[0], item[1], item[2], item[3], item[4])
			self.wall_list.add(wall)

		teleport = TeleportWall(250, 250, 15, 15, BLUE, 2)
		self.wall_list.add(teleport)

class Room2(Room):
	"""This creates all the walls in room 2"""
	def __init__(self):
		Room.__init__(self)

		walls = [[0, 0, 20, 250, RED],
				 [0, 350, 20, 250, RED],
				 [780, 0, 20, 250, RED],
				 [780, 350, 20, 250, RED],
				 [20, 0, 760, 20, RED],
				 [20, 580, 760, 20, RED],
				 [190, 50, 20, 500, GREEN],
				 [590, 50, 20, 500, GREEN]
				]

		for item in walls:
			wall = Wall(item[0], item[1], item[2], item[3], item[4])
			self.wall_list.add(wall)

		teleport = TeleportWall(350, 250, 15, 15, BLUE, 0)
		self.wall_list.add(teleport)

class Room3(Room):
	"""This creates all the walls in room 3"""
	def __init__(self):
		Room.__init__(self)

		walls = [[0, 0, 20, 250, PURPLE],
				 [0, 350, 20, 250, PURPLE],
				 [780, 0, 20, 250, PURPLE],
				 [780, 350, 20, 250, PURPLE],
				 [20, 0, 760, 20, PURPLE],
				 [20, 580, 760, 20, PURPLE]
				]

		for item in walls:
			wall = Wall(item[0], item[1], item[2], item[3], item[4])
			self.wall_list.add(wall)

		for x in range(100, 800, 100):
			for y in range(50, 451, 300):
				wall = Wall(x, y, 20, 200, RED)
				self.wall_list.add(wall)

		for x in range(150, 700, 100):
			wall = Wall(x, 200, 20, 200, WHITE)
			self.wall_list.add(wall)
			
class HealthBar:
	def __init__(self, screen, font, rect, name, max_health, background, foreground):
		self.screen = screen
		self.font = font
		self.rect = rect
		self.name = name
		self.background = background
		self.foreground = foreground
		self.max_health = max_health
		self.current_health = max_health
		
	def set_health(self, new_health):
		self.current_health = new_health
		if new_health < 0:
			self.current_health = 0
		elif new_health > self.max_health:
			self.current_health = self.max_health
		else:
			self.current_health = new_health
			
	def reset_health(self):
		self.current_health = self.max_health
		
	def take_health(self, lost_health):
		self.set_health(self.current_health - lost_health)
		
	def draw(self):
		mytext = self.font.render(self.name, False, BLUE)

		self.screen.set_clip(self.rect)
		self.screen.fill(self.background)

		health_percent = self.current_health / self.max_health
		bar_width = health_percent * self.rect.width
		
		health_bar = self.rect.copy()
		health_bar.width = bar_width
		self.screen.set_clip(health_bar)
		self.screen.fill(self.foreground)
		
		self.screen.set_clip(None)
		self.screen.blit(mytext, [self.rect.x - mytext.get_width() , self.rect.y])

def adjust_viewport(scene, viewport, player):
	buffer = 60
	# The scene has swidth x sheight
	# The viewport has vwidth x vheight
	# The viewport should shift when the player comes within buffer of the viewport edge
	oldviewport = viewport.copy()

	if (player.x - buffer) < viewport.x:
		viewport.x = player.x - buffer
	elif (player.x + buffer) > (viewport.x + viewport.width):
		viewport.x = player.x + buffer - viewport.width

	if (player.y - buffer) < viewport.y:
		viewport.y = player.y - buffer
	elif (player.y + buffer) > (viewport.y + viewport.height):
		viewport.y = player.y + buffer - viewport.height

	viewport = viewport.clamp(scene)

	#print(f"{scene} {player} {oldviewport} {viewport}")

	return viewport
	
def main():
	""" Main Program """

	# Call this function so the Pygame library can initialize itself
	pygame.init()
	
	
	healthbarfont = pygame.font.Font('Typodermic - JoystixMonospace-Regular.ttf', 16)
	turnchoosefont = pygame.font.Font('Typodermic - JoystixMonospace-Regular.ttf', 12)
	
	
	# Create an 800x600 sized screen
	screen = pygame.display.set_mode([860, 560])
	viewport = pygame.Rect([100,100,400,300])

	# Set the title of the window
	pygame.display.set_caption('Maze Runner')

	# Create the player paddle object
	level = 55
	#player = Player(50, 50, "Fred", 100 + level * 20, level, 20 + 5 * level, 5 + 1 * level, 0.2)
	player = Player(50, 50, "Fred", 2000, 1, 20, 10, .3)
	movingsprites = pygame.sprite.Group()
	movingsprites.add(player)

	#mob = Mob(50, 70, f"Orc1", 600, 1, 70, 10 * 5, 0.4)
	mob = Mob(50, 70, f"Orc1", 600, 1, 20, 10, 0.4)
	movingsprites.add(mob)
	
	rooms = []

	room = Room1()
	rooms.append(room)

	room = Room2()
	rooms.append(room)

	room = Room3()
	rooms.append(room)
   
	current_room_no = 0
	current_room = rooms[current_room_no]

		#
	clock = pygame.time.Clock()

	done = False

	p1_bar = HealthBar(screen, healthbarfont, pygame.Rect(220, 430, 80, 20), f"{player.name}", player.health, RED, GREEN)
	p2_bar = HealthBar(screen, healthbarfont, pygame.Rect(220, 455, 80, 20), f"{mob.name}", mob.health, RED, GREEN)
	
	MODE_RUNNING = 1
	MODE_COMBAT = 2
	
	selected = 1
	
	game_mode = MODE_RUNNING

	while not done:

		# --- Event Processing ---

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					player.changespeed(-5, 0)
				if event.key == pygame.K_RIGHT:
					player.changespeed(5, 0)
				if event.key == pygame.K_UP:
					player.changespeed(0, -5)
				if event.key == pygame.K_DOWN:
					player.changespeed(0, 5)
				if event.key == pygame.K_ESCAPE:
					done = True
				if event.key == pygame.K_SPACE:
					if game_mode == MODE_RUNNING:
						game_mode = MODE_COMBAT
						p2_bar.reset_health()
					else:
						game_mode = MODE_RUNNING
				

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					player.changespeed(5, 0)
				if event.key == pygame.K_RIGHT:
					player.changespeed(-5, 0)
				if event.key == pygame.K_UP:
					player.changespeed(0, 5)
				if event.key == pygame.K_DOWN:
					player.changespeed(0, -5)

		# --- Game Logic ---

		if game_mode == MODE_RUNNING:
			# Change if wanting mobs to move during combat
			collision = player.move(current_room.wall_list)
			if type(collision) is TeleportWall:
				current_room_no = collision.new_room
				current_room = rooms[current_room_no]
				
			mob.move(current_room.wall_list, player.rect.x, player.rect.y, pygame.time.get_ticks() / 10000.0)


		if player.rect.x < -15:
			if current_room_no == 0:
				current_room_no = 2
				current_room = rooms[current_room_no]
				player.rect.x = 790
			elif current_room_no == 2:
				current_room_no = 1
				current_room = rooms[current_room_no]
				player.rect.x = 790
			else:
				current_room_no = 0
				current_room = rooms[current_room_no]
				player.rect.x = 790

		if player.rect.x > 801:
			if current_room_no == 0:
				current_room_no = 1
				current_room = rooms[current_room_no]
				player.rect.x = 0
			elif current_room_no == 1:
				current_room_no = 2
				current_room = rooms[current_room_no]
				player.rect.x = 0
			else:
				current_room_no = 0
				current_room = rooms[current_room_no]
				player.rect.x = 0

		# --- Combat ---
		#print(f"{pygame.time.get_ticks()} {player.next_attack} {mob.next_attack}")
		if player.health > 0 and mob.health > 0 and pygame.time.get_ticks() > player.next_attack:
			do_combat(player, mob)
			player.next_attack = pygame.time.get_ticks() + player.attack_time
			if player.health <= 0:
				movingsprites.remove(player)
			if mob.health <= 0:
				movingsprites.remove(mob)

		if player.health > 0 and mob.health > 0 and pygame.time.get_ticks() > mob.next_attack:
			do_combat(mob,player)
			mob.next_attack = pygame.time.get_ticks() + mob.attack_time
			if player.health <= 0:
				movingsprites.remove(player)
			if mob.health <= 0:
				movingsprites.remove(mob)
				
				
		# --- Drawing ---
		screen.fill(BLACK)

		level = pygame.Surface([800,600])
		level.fill(LIGHT_GRAY)

		movingsprites.draw(level)
		current_room.wall_list.draw(level)

		screen.set_clip(None)
		
		# Level Overview
		screen.blit(pygame.transform.scale(level, [400,300]), [20, 20])

		# Close-up view
		screen.set_clip(pygame.Rect(440,20,400,300))
		viewport = adjust_viewport(level.get_rect(), viewport, player.rect)
		screen.blit(level, [440, 20], viewport)

		# Detail panel
		screen.set_clip(pygame.Rect(20, 340, 820, 200))
		screen.fill(WHITE)
		
		# Detail panel seperation
		screen.set_clip(pygame.Rect(20, 414, 820, 2))
		screen.fill(BLACK)
		
		screen.set_clip(pygame.Rect(319, 415, 2, 200))
		screen.fill(BLACK)
		
		screen.set_clip(pygame.Rect(429, 340, 2, 200))
		screen.fill(BLACK)		

		if game_mode == MODE_COMBAT:
			
			# Draw a sample bar
			#screen.set_clip(pygame.Rect(40, 360, 80, 20))
			#screen.fill(RED)

			#health = max(0, 80 - (pygame.time.get_ticks() / 2000.0))
			#screen.set_clip(pygame.Rect(40, 360, health, 20))
			#screen.fill(GREEN)
			
			# Draw a new bar
			p1_bar.take_health(0.2)
			p1_bar.draw()

			p2_bar.take_health(0.3)
			p2_bar.draw()

			screen.set_clip(None)
			# Draw some text
			mytext = turnchoosefont.render("Weapon", False, BLUE)
			screen.blit(mytext, [325, 415])
			
			mytext = turnchoosefont.render("Shield", False, BLUE)
			screen.blit(mytext, [325, 430])
			
			mytext = turnchoosefont.render("Misc Items", False, BLUE)
			screen.blit(mytext, [325, 445])
			
			mytext = turnchoosefont.render("Cast Spell", False, BLUE)
			screen.blit(mytext, [325, 460])
			
			mytext = turnchoosefont.render("Attack", False, BLUE)
			screen.blit(mytext, [325, 475])
			
			mytext = turnchoosefont.render("Diplomacy", False, BLUE)
			screen.blit(mytext, [325, 490])
			
			mytext = turnchoosefont.render("Run!", False, BLUE)
			screen.blit(mytext, [325, 505])
			
			mytext = turnchoosefont.render("React", False, BLUE)
			screen.blit(mytext, [325, 520])
			
		# Draw
		pygame.display.flip()

		clock.tick(60)

	pygame.quit()

if __name__ == "__main__":
	main()
