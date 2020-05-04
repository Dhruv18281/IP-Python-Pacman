# Name: Dhruv Yadav
# Roll no.: 2018281
# Section: B
# Group: 2


import pygame
import random
from numpy import loadtxt

#Initialization
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

grid_size = 32
screensize = grid_size * 21
win = pygame.display.set_mode((screensize, screensize + grid_size))
pygame.display.set_caption("Pac-man")
newfont = pygame.font.SysFont(None, 24)

#Adding Sprites and Making Layout
spr_home = [pygame.image.load('Sprites/Screen/spr_main_00.png'), pygame.image.load('Sprites/Screen/spr_main_01.png'), pygame.image.load('Sprites/Screen/spr_main_02.png'), pygame.image.load('Sprites/Screen/spr_main_03.png'), pygame.image.load('Sprites/Screen/spr_main_04.png'), pygame.image.load('Sprites/Screen/spr_main_05.png'), pygame.image.load('Sprites/Screen/spr_main_06.png'), pygame.image.load('Sprites/Screen/spr_main_07.png'), pygame.image.load('Sprites/Screen/spr_main_08.png'), pygame.image.load('Sprites/Screen/spr_main_09.png'), pygame.image.load('Sprites/Screen/spr_main_10.png'), pygame.image.load('Sprites/Screen/spr_main_11.png'), pygame.image.load('Sprites/Screen/spr_main_12.png'), pygame.image.load('Sprites/Screen/spr_main_13.png'), pygame.image.load('Sprites/Screen/spr_main_14.png'), pygame.image.load('Sprites/Screen/spr_main_15.png'), pygame.image.load('Sprites/Screen/spr_main_16.png'), pygame.image.load('Sprites/Screen/spr_main_17.png'), pygame.image.load('Sprites/Screen/spr_main_18.png'), pygame.image.load('Sprites/Screen/spr_main_19.png'), pygame.image.load('Sprites/Screen/spr_main_20.png'), pygame.image.load('Sprites/Screen/spr_main_21.png'), pygame.image.load('Sprites/Screen/spr_main_22.png'), pygame.image.load('Sprites/Screen/spr_main_23.png')]
main_count = 0
spr_end = [pygame.image.load('Sprites/Screen/spr_final_0.png'), pygame.image.load('Sprites/Screen/spr_final_1.png')]

spr_char = [pygame.image.load('Sprites/Player/spr_0.png'), pygame.image.load('Sprites/Player/spr_1.png'), pygame.image.load('Sprites/Player/spr_2.png'), pygame.image.load('Sprites/Player/spr_3.png'), pygame.image.load('Sprites/Player/spr_4.png'), pygame.image.load('Sprites/Player/spr_5.png'), pygame.image.load('Sprites/Player/spr_6.png'), pygame.image.load('Sprites/Player/spr_7.png')]
spr_num_max = len(spr_char)

spr_scared = pygame.image.load('Sprites/spr_0.png')
spr_inky = pygame.image.load('Sprites/spr_3.png')
spr_pinky = pygame.image.load('Sprites/spr_4.png')
spr_blinky = pygame.image.load('Sprites/spr_1.png')
spr_clyde = pygame.image.load('Sprites/spr_2.png')
g_sprite = {0:spr_scared, 1:spr_inky, 2:spr_pinky, 3:spr_blinky, 4:spr_clyde}

spr_wall = [pygame.image.load('Sprites/wall1.png'), pygame.image.load('Sprites/wall2.png')]
game_room = loadtxt('layout.txt', dtype = str)
rows, columns = game_room.shape

#Adding Music and Sound Effects
soundfx = [pygame.mixer.Sound('Sounds/06_2.wav'), pygame.mixer.Sound('Sounds/06_3.wav'), pygame.mixer.Sound('Sounds/04.wav'), pygame.mixer.Sound('Sounds/05.wav')]
fxcounter = 0
endmusic = [pygame.mixer.Sound('Sounds/end1.wav'), pygame.mixer.Sound('Sounds/end2.wav')]
bgmusic = pygame.mixer.music.load('Sounds/bgmusic.mp3')
scaremusic = pygame.mixer.Sound('Sounds/03.wav')
walkmusic = pygame.mixer.Sound('Sounds/02.wav')
walkmusic.play(-1)
walkmusic.set_volume(0)
pygame.mixer.music.play(-1)

#Clock Initialization
clock = pygame.time.Clock()
curtime = 0


class Player:
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.width = 32
		self.height = 32
		self.vel = 8
		self.dir = 'U'
		self.sprite_num = 0
		self.angle = 0
		self.flipped = False
		self.hitbox = (self.x, self.y, 32, 32)
		self.mvmt = [2, 2]
		self.lives = 3
	
	def draw(self, win):
		if self.sprite_num + 1 < spr_num_max:
			self.sprite_num += 1
		else:
			self.sprite_num=0
		win.blit(pygame.transform.flip(pygame.transform.rotate(spr_char[self.sprite_num], self.angle), False, self.flipped), (self.x,self.y))
		
	def player_movement(self, keys):
		if keys[pygame.K_LEFT]:
			self.dir = 'L'
		elif keys[pygame.K_RIGHT]:
			self.dir = 'R'
		elif keys[pygame.K_UP]:
			self.dir = 'U'
		elif keys[pygame.K_DOWN]:
			self.dir = 'D'
			
		self.hitbox = (self.x, self.y, 32, 32)
		
		canturn = True
		if self.dir == 'L' and self.x % grid_size == 0 and self.y % grid_size == 0:
			for wall in wall_list:
				if pygame.Rect(self.hitbox[0] - self.vel, self.hitbox[1], self.hitbox[2], self.hitbox[3]).colliderect(wall.hitbox):
					canturn = False
			if canturn == True:
				self.mvmt = [1, 0]
				self.angle = 180
				self.flipped = True
		if self.dir == 'R' and self.x % grid_size == 0 and self.y % grid_size == 0:
			for wall in wall_list:
				if pygame.Rect(self.hitbox[0] + self.vel, self.hitbox[1], self.hitbox[2], self.hitbox[3]).colliderect(wall.hitbox):
					canturn = False
			if canturn == True:
				self.mvmt = [0, 0]
				self.angle = 0
				self.flipped = False
		if self.dir == 'U' and self.x % grid_size == 0 and self.y % grid_size == 0:
			for wall in wall_list:
				if pygame.Rect(self.hitbox[0], self.hitbox[1] - self.vel, self.hitbox[2], self.hitbox[3]).colliderect(wall.hitbox):
					canturn = False
			if canturn == True:
				self.mvmt = [1, 1]
				self.angle = 270
				self.flipped = True
		if self.dir == 'D' and self.x % grid_size == 0 and self.y % grid_size == 0:
			for wall in wall_list:
				if pygame.Rect(self.hitbox[0], self.hitbox[1] + self.vel, self.hitbox[2], self.hitbox[3]).colliderect(wall.hitbox):
					canturn = False
			if canturn == True:
				self.mvmt = [0, 1]
				self.angle = 270
				self.flipped = False
		
		canmove = True
		if self.mvmt == [1, 0]:
			for wall in wall_list:
				if pygame.Rect(self.hitbox[0] - self.vel, self.hitbox[1], self.hitbox[2], self.hitbox[3]).colliderect(wall.hitbox) and wall.type == 0:
					canmove = False
			if canmove == True:
				self.x -= self.vel
		if self.mvmt == [0, 0]:
			for wall in wall_list:
				if pygame.Rect(self.hitbox[0] + self.vel, self.hitbox[1], self.hitbox[2], self.hitbox[3]).colliderect(wall.hitbox) and wall.type == 0:
					canmove = False
			if canmove == True:
				self.x += self.vel
		if self.mvmt == [1, 1]:
			for wall in wall_list:
				if pygame.Rect(self.hitbox[0], self.hitbox[1] - self.vel, self.hitbox[2], self.hitbox[3]).colliderect(wall.hitbox) and wall.type == 0:
					canmove = False
			if canmove == True:
				self.y -= self.vel
		if self.mvmt == [0,  1]:
			for wall in wall_list:
				if pygame.Rect(self.hitbox[0], self.hitbox[1] + self.vel, self.hitbox[2], self.hitbox[3]).colliderect(wall.hitbox) and wall.type == 0:
					canmove = False
			if canmove == True:
				self.y += self.vel
		
		dead = False
		for ghost in ghost_list:
			if pygame.Rect(self.hitbox).colliderect(ghost.hitbox):
				if ghost.state == 0:
					global points
					points += 200
					ghost_list.pop(ghost_list.index(ghost))
					ghost.dead()
				else:
					dead = True
		if dead == True:
			for ghost in ghost_list:
				ghost_list.pop(ghost_list.index(ghost))
			soundfx[2].play()
			pygame.time.delay(1000)
			self.lives -= 1
			reset()
		
		if self.x > screensize - self.vel:
			self.x = -1 * grid_size
		if self.x < -32:
			self.x = screensize
		
class Coins:
	def __init__(self,x,y,type):
		self.x = x - grid_size
		self.y = y
		self.type = type
		if type == 0:
			self.radius = 7
		else:
			self.radius = 3
	
	def draw(self,win):
		pygame.draw.circle(win, (255, 255, 255), (self.x, self.y), self.radius)
	
	def collision(self, obj_player):
		if self.y - self.radius < obj_player.hitbox[1] + obj_player.hitbox[3] and self.y + self.radius > obj_player.hitbox[1] and self.x - self.radius < obj_player.hitbox[0] + obj_player.hitbox[2] and self.x + self.radius > obj_player.hitbox[0]:
			global fxcounter
			soundfx[fxcounter%2].play()
			fxcounter+=1
			global points
			if self.type == 0:
				points += 50
				soundfx[3].play()
				for ghost in ghost_list:
					ghost.scared()
				coin_list.pop(coin_list.index(self))
			else:
				points += 10
				coin_list.pop(coin_list.index(self))
			
class Ghosts:
	def __init__(self,x,y,state):
		self.x = x
		self.y = y
		self.state = state
		self.prev_state = state
		self.scarecount = 0
		self.random_movement = 0
		self.vel = 8
		self.hitbox = (self.x, self.y, 32, 32)
		self.mvmt = [0, 0]
		self.move_var = 0
	
	def draw(self,win):
		win.blit(g_sprite[self.state], (self.x, self.y))
		
	def scared(self):
		self.state = 0
		scaremusic.play(-1)
		self.scarecount = 5 * 24
	
	def scaretimer(self):
		if self.scarecount == 0:
			self.state = self.prev_state
			scaremusic.stop()
			walkmusic.set_volume(1)
		else:
			self.scarecount-=1
	
	def movement(self):
		self.hitbox = (self.x, self.y, 32, 32)
		
		movelist = [1, 2, 3, 4]
		if self.x % grid_size == 0 and self.y % grid_size == 0:
			for wall in wall_list:
				if pygame.Rect(self.hitbox[0] - self.vel, self.hitbox[1], self.hitbox[2], self.hitbox[3]).colliderect(wall.hitbox) and wall.type == 0:
					if 1 in movelist:
						movelist.remove(1)
				if pygame.Rect(self.hitbox[0] + self.vel, self.hitbox[1], self.hitbox[2], self.hitbox[3]).colliderect(wall.hitbox) and wall.type == 0:
					if 2 in movelist:
						movelist.remove(2)
				if pygame.Rect(self.hitbox[0], self.hitbox[1] - self.vel, self.hitbox[2], self.hitbox[3]).colliderect(wall.hitbox) and wall.type == 0:
					if 3 in movelist:
						movelist.remove(3)
				if pygame.Rect(self.hitbox[0], self.hitbox[1] + self.vel, self.hitbox[2], self.hitbox[3]).colliderect(wall.hitbox) and wall.type == 0:
					if 4 in movelist:
						movelist.remove(4)
			if self.mvmt == [1, 0] and 1 in movelist:
				movelist = movelist + [1, 1, 1, 1]
			if self.mvmt == [0, 0] and 2 in movelist:
				movelist = movelist + [2, 2, 2, 2]
			if self.mvmt == [1, 1] and 3 in movelist:
				movelist = movelist + [3, 3, 3, 3]
			if self.mvmt == [0, 1] and 4 in movelist:
				movelist = movelist + [4, 4, 4, 4]
				
			self.move_var = random.choice(movelist)
			
		if self.move_var == 1:
			self.mvmt = [1, 0]
		elif self.move_var == 2:
			self.mvmt = [0, 0]
		elif self.move_var == 3:
			self.mvmt = [1, 1]
		elif self.move_var == 4:
			self.mvmt = [0, 1]
			
		if self.mvmt == [1, 0]:
			self.x -= self.vel
		if self.mvmt == [0, 0]:
			self.x += self.vel
		if self.mvmt == [1, 1]:
			self.y -= self.vel
		if self.mvmt == [0, 1]:
			self.y += self.vel
					
		if self.x > screensize - self.vel:
			self.x = -1 * grid_size
		if self.x < -32:
			self.x = screensize	
			
	def dead(self):
		self.x = 320
		self.y = 288
		ghost_list.append(self)
	
class Walls:
	def __init__(self, x, y, type):
		self.x = x - grid_size
		self.y = y - grid_size
		self.hitbox = (self.x, self.y, 32, 32)
		self.type = type
	
	def draw(self, win):		
		win.blit(spr_wall[self.type], (self.x, self.y))
		

#Redrawing Window		
def redraw_window():
	win.fill((0,0,0))
	for wall in wall_list:
		wall.draw(win)
	pointstr = newfont.render('Points: ' + str(points), False, (255, 255, 255))
	livestr = newfont.render('Lives: ', False, (255,255,255))
	timestr = newfont.render('Time: ' + str(curtime//24), False, (255, 255, 255))
	win.blit(pointstr, (25, 10))
	win.blit(livestr, (500, 10))
	win.blit(timestr, (256, 10))
	for coin in coin_list:
		coin.draw(win)
	for i in range(player.lives):
		win.blit(spr_char[5], (550 + (grid_size * i), 0))
	clyde.draw(win)
	inky.draw(win)
	pinky.draw(win)
	blinky.draw(win)
	player.draw(win)

#Resetting after death	
def reset():
	global player
	global inky
	global pinky
	global blinky
	global clyde
	player.x = 320
	player.y = 512
	player.mvmt = [2,2]
	inky = Ghosts(320, 320, 1)
	pinky = Ghosts(288, 320, 2)
	blinky = Ghosts(320, 288, 3)
	clyde = Ghosts(352, 320, 4)
	global ghost_list
	ghost_list = [inky, pinky, blinky, clyde]
	

#Variable Initialization	
run1 = True
run2 = True
run3 = True
run4 = True
player = Player(320, 512)
inky = Ghosts(320, 320, 1)
pinky = Ghosts(288, 320, 2)
blinky = Ghosts(320, 288, 3)
clyde = Ghosts(352, 320, 4)
ghost_list = [inky, pinky, blinky, clyde]
coin_list = []
wall_list = []
points = 0
for row in range(rows):
	for col in range(columns):
		val = game_room[col][row]
		if val == 'w':
			wall_list.append(Walls(row * grid_size, (col * grid_size) + 32, 0))
		if val == '-':
			wall_list.append(Walls(row * grid_size, (col * grid_size) + 32, 1))
		if val == '.':
			coin_list.append(Coins((row * grid_size) + 16, (col * grid_size) + 16, 1))
		if val == 'o':
			coin_list.append(Coins((row * grid_size) + 16, (col * grid_size) + 16, 0))

			
#Main Loops
#Starting Screen
while run1 == True:

	clock.tick(12)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run1 = False
			run2 = False
			run3 = False
			run4 = False
	if main_count < len(spr_home) - 1:
		main_count += 1
	else:
		main_count = 0
		
	if (230 <= pygame.mouse.get_pos()[0] <= 440) and (525 <= pygame.mouse.get_pos()[1] <= 595) and pygame.mouse.get_pressed() == (1, 0, 0):
		run1 = False
		
	win.fill((0,0,0))
	win.blit(spr_home[main_count], (0, 0))
	pygame.display.update()
	
#Game Part	
while run2 == True:

	walkmusic.set_volume(1)
	pygame.mixer.music.set_volume(0.5)
	clock.tick(24)
	curtime += 1
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run2 = False
			run3 = False
			run4 = False
			
	keys = pygame.key.get_pressed()
	player.player_movement(keys)
	
	for ghost in ghost_list:
		ghost.scaretimer()
		ghost.movement()
		
	for coin in coin_list:
		coin.collision(player)
	
	if player.lives == 0:
		pygame.time.delay(1000)
		run2 = False
		run3 = False
		
	if len(coin_list) == 0:
		pygame.time.delay(1000)
		run2 = False
		run4 = False
	
	redraw_window()
	pygame.display.update()

#Win Screen
while run3 == True:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run4 = False
			run3 = False
	
	pygame.mixer.music.stop()
	scaremusic.stop()
	walkmusic.stop()
	if endmusic[0].get_num_channels() <= 1:
		endmusic[0].play()
	
	win.fill((0,0,0))
	win.blit(spr_end[0], (0, 0))
	finalpointstr = newfont.render('Final Points: ' + str(points), False, (255, 255, 255))
	win.blit(finalpointstr, (240, 512))
	pygame.display.update()

#Lose screen	
while run4 == True:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run4 = False
	
	pygame.mixer.music.stop()
	scaremusic.stop()
	walkmusic.stop()
	if endmusic[1].get_num_channels() <= 1:
		endmusic[1].play()
	
	win.fill((0,0,0))
	win.blit(spr_end[1], (0, 0))
	finalpointstr = newfont.render('Final Points: ' + str(points), False, (255, 255, 255))
	win.blit(finalpointstr, (240, 512))
	pygame.display.update()
	
pygame.quit() #Ending Game