

#This came from http://programarcadegames.com/index.php?lang=en






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

BLACK  = (	 0,	  0,   0)
WHITE  = ( 255, 255, 255)
BLUE   = (	 0,	  0, 255)
GREEN  = (	 0, 255,   0)
RED	   = ( 255,	  0,   0)
PURPLE = ( 255,	  0, 255)
LIGHT_GREY = (60, 60, 60)
DARK_GREY = (180, 180, 180)

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

class Mob(pygame.sprite.Sprite):
	
	def __init__(self, x, y):
	
		super().__init__()
		
		self.image = pygame.Surface([15, 15])
		self.image.fill(RED)
		
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x
		
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
			
		self.change_x = dist_x + random.randint(-5,5)
		self.change_y = dist_y + random.randint(-5,5)
		
		# Move left/right
		self.rect.x += self.change_x
		
		# Did this update cause us to hit a wall?
		block_hit_list = pygame.sprite.spritecollide(self, walls, False)
		for block in block_hit_list:
			# If we are moving right, set our right side to the left side of
			# the item we hit
			if self.change_x > 0:
				self.rect.right = block.rect.left
			else:
				# Otherwise if we are moving left, do the opposite.
				self.rect.left = block.rect.right

		# Move up/down
		self.rect.y += self.change_y

		# Check and see if we hit anything
		block_hit_list = pygame.sprite.spritecollide(self, walls, False)
		for block in block_hit_list:
			# Reset our position based on the top/bottom of the object.
			if self.change_y > 0:
				self.rect.bottom = block.rect.top
			else:
				self.rect.top = block.rect.bottom
		
class Player(pygame.sprite.Sprite):
	""" This class represents the bar at the bottom that the player controls """

	# Set speed vector
	change_x = 0
	change_y = 0

	def __init__(self, x, y):
		""" Constructor function """

		# Call the parent's constructor
		super().__init__()

		# Set height, width
		self.image = pygame.Surface([15, 15])
		self.image.fill(WHITE)

		# Make our top-left corner the passed-in location.
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x

	def changespeed(self, x, y):
		""" Change the speed of the player. Called with a keypress. """
		self.change_x += x
		self.change_y += y

	def move(self, walls):
		""" Find a new position for the player """

		# Move left/right
		self.rect.x += self.change_x

		special_block = None
		
		# Did this update cause us to hit a wall?
		block_hit_list = pygame.sprite.spritecollide(self, walls, False)
		for block in block_hit_list:
			if type(block) is TeleportWall:
				special_block = block

			# If we are moving right, set our right side to the left side of
			# the item we hit
			if self.change_x > 0:
				self.rect.right = block.rect.left
			else:
				# Otherwise if we are moving left, do the opposite.
				self.rect.left = block.rect.right

		# Move up/down
		self.rect.y += self.change_y

		# Check and see if we hit anything
		block_hit_list = pygame.sprite.spritecollide(self, walls, False)
		for block in block_hit_list:
			if type(block) is TeleportWall:
				special_block = block
			
			# Reset our position based on the top/bottom of the object.
			if self.change_y > 0:
				self.rect.bottom = block.rect.top
			else:
				self.rect.top = block.rect.bottom
				
		return special_block

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
		self.walls = [[0, 0, 20, 350, DARK_GREY],
				 [35, 0, 20, 765, DARK_GREY],
				 [0, 450, 20, 350, DARK_GREY],
				 [1380, 0, 20, 350, DARK_GREY],
				 [1380, 450, 20, 350, DARK_GREY],
				 [20, 0, 1360, 20, DARK_GREY],
				 [20, 780, 1360, 20, DARK_GREY],
				 [390, 50, 20, 500, DARK_GREY]
				]

	   # Loop through the list. Create the wall, add it to the list
		for item in self.walls:
			wall = Wall(item[0], item[1], item[2], item[3], item[4])
			self.wall_list.add(wall)
			
		teleport = TeleportWall(250, 250, 15, 15, BLUE, 2)
		self.wall_list.add(teleport)
		
	def rebuild(self, scale):
		self.wall_list.empty()
		
		for item in self.walls:
			scaled_item = [ val * scale for val in item[0:4] ]
			wall = Wall(scaled_item[0], scaled_item[1], scaled_item[2], scaled_item[3], item[4])
			self.wall_list.add(wall)

		teleport = TeleportWall(250 * scale, 250 * scale, 15 * scale, 15 * scale, BLUE, 2)
		self.wall_list.add(teleport)
		

class Room2(Room):
	"""This creates all the walls in room 2"""
	def __init__(self):
		Room.__init__(self)

		walls = [[0, 0, 20, 250, DARK_GREY],
				 [0, 350, 20, 250, DARK_GREY],
				 [780, 0, 20, 250, DARK_GREY],
				 [780, 350, 20, 250, DARK_GREY],
				 [20, 0, 760, 20, DARK_GREY],
				 [20, 580, 760, 20, DARK_GREY],
				 [190, 50, 20, 500, DARK_GREY],
				 [590, 50, 20, 500, DARK_GREY]
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

		walls = [[0, 0, 20, 250, DARK_GREY],
				 [0, 350, 20, 250, DARK_GREY],
				 [780, 0, 20, 250, DARK_GREY],
				 [780, 350, 20, 250, DARK_GREY],
				 [20, 0, 760, 20, DARK_GREY],
				 [20, 580, 760, 20, DARK_GREY]
				]

		for item in walls:
			wall = Wall(item[0], item[1], item[2], item[3], item[4])
			self.wall_list.add(wall)

		for x in range(100, 800, 100):
			for y in range(50, 451, 300):
				wall = Wall(x, y, 20, 200, DARK_GREY)
				self.wall_list.add(wall)

		for x in range(150, 700, 100):
			wall = Wall(x, 200, 20, 200, DARK_GREY)
			self.wall_list.add(wall)

def main():
	""" Main Program """

	# Call this function so the Pygame library can initialize itself
	pygame.init()

	# Create an 800x600 sized screen
	screen = pygame.display.set_mode([1400, 800])

	# Set the title of the window
	pygame.display.set_caption('Maze Runner')

	# Create the player paddle object
	player = Player(50, 50)
	movingsprites = pygame.sprite.Group()
	movingsprites.add(player)

	mob = Mob(50, 70)
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

	clock = pygame.time.Clock()

	done = False

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

		collision = player.move(current_room.wall_list)
		if type(collision) is TeleportWall:
			current_room_no = collision.new_room
			current_room = rooms[current_room_no]
			
		mob.move(current_room.wall_list, player.rect.x, player.rect.y, pygame.time.get_ticks() / 10000.0)

		if player.rect.x < -15:
			if current_room_no == 0:
				current_room_no = 2
				current_room = rooms[current_room_no]
				player.rect.x = 1390
			elif current_room_no == 2:
				current_room_no = 1
				current_room = rooms[current_room_no]
				player.rect.x = 1390
			else:
				current_room_no = 0
				current_room = rooms[current_room_no]
				current_room.rebuild(0.5)				
				player.rect.x = 790

		if player.rect.x > 1401:
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

		# --- Drawing ---
		screen.fill(LIGHT_GREY)

		movingsprites.draw(screen)
		current_room.wall_list.draw(screen)

		pygame.display.flip()

		clock.tick(60)

	pygame.quit()

if __name__ == "__main__":
	main()
