#TODO
#Incorporate Stalling
#Add smoke/damage to planes after they're damaged
#Add scoreboard to track wins/losses
#improve hitbox

import pygame
import math
import random


#initiate the game instance
pygame.init()
pygame.mixer.init()
epic1 = pygame.mixer.music.load('epic1.mp3')
crash_sound = pygame.mixer.Sound("crash.wav")
bullet_sound = pygame.mixer.Sound("bullet.wav")
hit_sound = pygame.mixer.Sound("hit.wav")
down_sound = pygame.mixer.Sound("down.wav")
#display dimensions
display_width = 800
display_height = 600
#create the game display
gameDisplay = pygame.display.set_mode((display_width, display_height))
#set game display title
pygame.display.set_caption("Dogfight: By Chris Dugan")
#inititate the game clock
clock = pygame.time.Clock()
#game icon
gameIcon = pygame.image.load('redPlane.png')
pygame.display.set_icon(gameIcon)
#define colors
health_green = (0, 150, 0)
heatlh_orange = (255, 165, 0)
health_red = (150, 0, 0)
red = (200, 0, 0)
bright_red = (255,0,0)
green = (0, 200, 0)
bright_green = (0,255,0)
black = (0,0,0)
white = (255, 255, 255)
gray = (100, 100, 100)
blue = (0, 0, 255)
endBlue = (0,0,200)
yellow = (200, 200, 0)
#load in plane image
planeImg = pygame.image.load('redPlane.png')
#Plane Class
class Plane(object):
	imgName = '' #plane image name to load
	x = 0 #plane 
	y = 0
	deg = 0
	x_change = 0
	y_change = 0
	speed = 3
	accel = 0
	upKey = ''
	downKey = ''
	shootKey = '' 

	def __init__(self, player='', imgName='redPlane.png', x=0, y=0, health=3, shotTime = 0,
	 deg=0, speed=3, accel=0, upKey='', downKey='', shootKey='', width = 30, height=15, degchg = 0,
	 instructions='', color=''):
		self.player = player #string: player name
		self.imgName = imgName #name of image to use for the plane
		self.x = x #int: x location (center of image)
		self.y = y #int: y location (center of image)
		self.health = health #int: health of this plane
		self.shotTime = shotTime #int: shot timer to prevent bullet spamming
		self.deg = deg #int: degree the plane is facing
		self.speed = speed #int: magnitude of speed of plane
		self.accel = accel #int: magnitude of acceleration of plane
		self.upKey = upKey #string corresponding to the tilt up key
		self.downKey = downKey #string corresponding to the tilt down key
		self.shootKey = shootKey #string corresponding to the shoot key
		self.width = width #int: width of this plane
		self.height = height #int: height of this plane
		self.img = pygame.image.load(imgName) #loaded image of plane
		self.degchg = degchg # int: current change in degrees (instantaneous)
		self.instructions = instructions #string with key mapping (upshootdown)
		self.color = color #tuple RBG: plane color
		self.hitbox = [0,0]

	#place the plane on the board
	def placePlane(self):
		img = self.img
		img = pygame.transform.rotate(img, self.deg)
		gameDisplay.blit(img, (self.x, self.y))
		#pygame.draw.circle(gameDisplay, black, [int(self.x), int(self.y)], 1) #for debugging plane x,y
		self.hitbox = [int(self.x + self.width/2), int(self.y + self.height/2)] 
		#pygame.draw.circle(gameDisplay, blue, self.hitbox, int(self.width/2), 2) #for debugging hitbox

#Bullet Class
class Bullet(object):
	player = '' #plane it belongs to 
	# x and y coords
	x = 0
	y = 0
	#direction of travel
	deg = 0
	#speed of travel
	speed = 0
	#constructor
	def __init__(self, player, x, y, deg, speed):
		self.player = player #player the bullet belongs to 
		self.x = x #x location of center of bullet
		self.y = y #y location of center of bullet
		self.deg = deg #direction of bullet travel in degrees
		self.speed = speed #speed of bullet
	#method draws bullet
	def placeBullet(self):
		#draws the bullet
		pygame.draw.circle(gameDisplay, black, [int(self.x),int(self.y)], 3)
#cloud class
class Cloud:
	color = gray
	x = display_width/2
	y = display_height/2
	speed = 0.0001
	width = 70
	height = 40

	def __init__(self, color=gray, x=0, y=100, speed=random.randint(-10,10), width=70, height=40):
		self.color = color #color of cloud
		self.x = x #x location of top left corner of cloud
		self.y = y #y location of top right corner of cloud
		self.speed = speed #speed of cloud
		self.width = width #width of cloud
		self.height = height #height of cloud
	def placeCloud(self):
		#draw the cloud
		pygame.Surface.fill(gameDisplay, self.color, rect=[self.x, self.y, 
			self.width, self.height])

#display instructions
def display_instructions(start=pygame.K_SPACE):
	#create instruction text
	text, rect = create_text('Space to Start!', 80, black, (display_width/2, display_height/5))
	gameDisplay.blit(text, rect)
	pause = True
	#game paused until user presses appropriate key
	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: #if user quits
				crashed = True
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == start:
					pause = False
		pygame.display.update()
		clock.tick(15)
def game_loop(num_players):
	#initialize players
	#HOW TO REPLACE 15 WITH SELF.HEIGHT?
	playerOne = Plane(player='1', x=display_width/2, y=15, imgName='redPlane.png', upKey=pygame.K_LEFT, downKey=pygame.K_RIGHT, shootKey=pygame.K_DOWN, instructions='left down right', color=red)
	playerTwo = Plane(player='2', x=display_width/2, y=display_height/5*2, imgName='bluePlane.png', upKey=pygame.K_a, downKey=pygame.K_d, shootKey= pygame.K_s, instructions='a s d', color=blue)
	playerThree = Plane(player='3', x=display_width/2, y=display_height/5*3, imgName='yellowPlane.png', upKey=pygame.K_j, downKey=pygame.K_l, shootKey= pygame.K_k, instructions='j k l', color=yellow)
	playerFour = Plane(player='4', x=display_width/2, y=display_height/5*4, imgName='blackPlane.png', upKey=pygame.K_v, downKey=pygame.K_n, shootKey=pygame.K_b, instructions= 'v b n', color=black)
	#initialize list of all bullets
	bullet_list = []
	#initalize list of all players
	plane_list = [playerOne, playerTwo, playerThree, playerFour]
	plane_list = plane_list[:num_players]

	#initialize list of all clouds
	cloud_list = []
	#initialize cloud Timer for creating clouds
	cloudTimer = 3600
	instruction_timer = 0
	#begin loop
	crashed = False

	while not crashed: #continue until crashed
		#must fill with white before drawing anything
		gameDisplay.fill(white)

		#instructionsfor first 2 seconds
		if instruction_timer < 120:
			for plane in plane_list:
				text, rect = create_text(plane.instructions, 30, plane.color, (plane.x, plane.y + plane.height * 3))
				gameDisplay.blit(text, rect)
			instruction_timer += 1


		#event loop
		for event in pygame.event.get():
			if event.type == pygame.QUIT:#if user quits
				crashed = True
				pygame.quit()
				quit()
				 #quit game
			#if user presses a key
			if event.type == pygame.KEYDOWN:
				#iterate through planes
				for plane in plane_list:
					if event.key == plane.upKey:
						plane.degchg = 5 #plane will turn up 5 degrees every frame while key is pressed
					elif event.key == plane.downKey:
						plane.degchg = -5 #plane will turn down 5 degrees every frame while key is pressed
					if event.key == plane.shootKey:
						if plane.shotTime == 0: #check if shot recently
							#create bullet and add to list
							pygame.mixer.Sound.play(bullet_sound)
							pewpew = Bullet(plane.player, plane.hitbox[0], plane.hitbox[1], plane.deg, plane.speed + 2)
							bullet_list.append(pewpew)
							plane.shotTime = 60 #reset shot timer
			#check if key is unpressed
			if event.type == pygame.KEYUP:
				#iterate through planes
				for plane in plane_list:	
					#reset plane degree change
					if event.key == plane.upKey or event.key == plane.downKey:
						plane.degchg = 0

		for plane in plane_list:
			#update each plane's direction
			plane.deg += plane.degchg
			
		
		#iterate through planes
		for plane in plane_list:
			#create rectangle
			#increment shot timer
			if plane.shotTime > 0:
				plane.shotTime -= 1
			#check if hit
			hit = False
			#check if distance from bullet to hitbox center is less than plane.width
			for bullet in bullet_list:
				#if bullet is in plane hitbox and it doesn't belong to that player
				dist = math.sqrt((plane.x - bullet.x) **2 + (plane.y - bullet.y)**2)
				if dist < plane.width/2 and plane.player != bullet.player:
					hit = True
					#remove the bullet from the list
					bullet_list.remove(bullet)
			if hit:
				#update player health
				#pygame.mixer.Sound.play(hit_sound)
				plane.health -= 1
				if plane.health <= 0:
					#player loses if 
					plane_list.remove(plane)
					pygame.mixer.Sound.play(down_sound)
			# if angle is severe, plane accelerates
			plane.accel = 0
			if abs(math.sin(plane.deg / 180 * math.pi))  > 0.5:
				plane.accel = 0.01 * -math.sin(plane.deg / 180 * math.pi)
			plane.speed += plane.accel

			#plane speed cannot be negative
			if plane.speed < 0:
				plane.speed = 0
			#set max speed of 10
			if plane.speed > 6:
				plane.speed = 6
			x_speed = math.cos(plane.deg / 180 * math.pi) * plane.speed
			y_speed = -math.sin(plane.deg / 180 * math.pi) * plane.speed
		#if angle is severe, gravity affects
		# if abs(math.sin(deg / 180 *math.pi)) > 0.3:
		# 	accel = 0.01 * -math.sin(deg / 180 * math.pi)
		# speed += accel
		#speed can never be negative
		# if speed < 0:
		# 	speed = 0
			#Boundaries
			#plane can move through right and left boundaries
			if plane.x > display_width - plane.width:
				plane.x -= display_width
			if plane.x < 0:
				plane.x += display_width
			if plane.y < 0:
				plane.y = 0
			if plane.y > display_height - plane.height:
				plane_list.remove(plane)
				pygame.mixer.Sound.play(down_sound)
		#update position
			plane.x += x_speed
			plane.y += y_speed
			#draw plane
			plane.placePlane()

		
		#draw plane #plane(x,y, deg)
		#update bullets position

		#draw bullets
		for pew in bullet_list:
			#update bullet position
			if pew.x > display_width or pew.x < 0 or pew.y > display_height or pew.y < 0 :
				bullet_list.remove(pew)
			pew.x += pew.speed * math.cos(pew.deg / 180 * math.pi)
			pew.y += pew.speed * -math.sin(pew.deg / 180 * math.pi)
			pew.placeBullet()

		#display health
		for plane in plane_list:
			if plane.health == 3:
				health_color = health_green
			elif plane.health == 2:
				health_color = heatlh_orange
			elif plane.health == 1:
				health_color = health_red
			pygame.draw.rect(gameDisplay, health_color, (plane.x, plane.y + 15, 20,5))
		#display accel
		# for plane in plane_list:
		# 	#accel triangle points in direction of travel
		# 	if plane.accel != 0:
		# 		pygame.draw.polygon(gameDisplay, blue,
		# 		 [(plane.x + 5*math.cos((plane.deg + 90)/ 180 * math.pi), plane.y - 5*math.sin((plane.deg + 90) / 180 * math.pi)),
		# 		  (plane.x + plane.accel*1000*math.cos(plane.deg/ 180 * math.pi), plane.y - plane.accel*1000*math.sin(plane.deg / 180 * math.pi)),
		# 		  (plane.x + 5*math.cos((plane.deg - 90)/ 180 * math.pi), plane.y - 5*math.sin((plane.deg - 90) / 180 * math.pi))] )

		#create cloud every 1000 frames
		cloudTimer +=1
		if cloudTimer > 1000:
			cloudTimer = 0
			cloud = Cloud(width=random.randint(100,150), height=random.randint(60,120), y=random.randint(0,400),
				speed=random.choice(range(-11,11,2)) * 0.05)
			if cloud.speed < 0:
				cloud.x = display_width
			cloud_list.append(cloud)
		#move and display clouds
		for cloud in cloud_list:
			if cloud.x > display_width or cloud.x < 0:
				cloud_list.remove(cloud)
			cloud.x += cloud.speed
			cloud.placeCloud()

		#check Win:
		if len(plane_list) == 1:
			#display winner box
			colors = [red, blue, yellow, black]
			#pick color corresponding to winning player
			win_color = colors[int(plane_list[0].player) - 1]
			#outside border rectangle
			rec1 = (display_width /2 - 250, display_height/2 - 200, 500, 400)
			pygame.draw.rect(gameDisplay, black, rec1)
			#inside fill rectangle
			rec2 = (display_width /2 - 240, display_height/2 - 190, 480, 380)
			pygame.draw.rect(gameDisplay, win_color, rec2)
			# player win text
			text, rect = create_text('Player ' + str(plane_list[0].player) + ' Wins!',
			 70, white, (display_width/2, display_height/2) )
			
			gameDisplay.blit(text, (display_width/2 - 200, display_height/2 - 50))
			pressed = button("Play again?", display_width/2 - 200/2, display_height/2 + 50,
				200, 50, green, bright_green)
			if pressed:
				crashed = True
		if instruction_timer == 1:
			display_instructions()
		pygame.display.update() #update the screen

		clock.tick(60) #60 fps

def quit_game():
	pygame.quit()
	quit()

def button(msg, x, y, w, h, ic, ac, action=None, action_args=None):

	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if x < mouse[0] < x + w and y < mouse[1] < y + h:
		pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
		if click[0] == 1 and action != None:
			if action_args != None:
				action(action_args)
			elif action_args == None:
				action()
		if click[0] == 1 and action == None:
			return True
	else:
		pygame.draw.rect(gameDisplay, ic, (x,y,w,h))
	text, rect = create_text(msg, 40, black, (x + w/2, y + h/2))
	gameDisplay.blit(text, (rect))
def game_intro():

	intro = True
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		gameDisplay.fill(white)
		#Title
		text, rect = create_text("Dogfight", 100, black, (display_width/2, display_height/3))
		gameDisplay.blit(text, rect)
		text2, rect2 = create_text("Players:", 80, black, (display_width/4, display_height/2))
		gameDisplay.blit(text2, rect2)
		

		mouse = pygame.mouse.get_pos()
		button("2", display_width/2 - 50, display_height/2 - 50/2, 50, 50, green, bright_green, game_loop, 2)
		button("3", display_width/2 + 50, display_height/2 - 50/2, 50, 50, green, bright_green, game_loop, 3)
		button("4", display_width/2 + 150, display_height/2 - 50/2, 50, 50, green, bright_green, game_loop, 4)
		button("Quit", display_width/2 - 100/2, 450, 100, 50, red, bright_red, quit_game)
		pygame.display.update()
		clock.tick(15)

def create_text(msg, size, color=black, center=(0,0)):
	font = pygame.font.SysFont(None, size)
	text = font.render(msg, True, color)
	rect = text.get_rect()
	rect.center = center
	return text, rect

game_intro()

pygame.quit()
quit()


"""
Additions:
indicator of if plane is accelerating or decelerating (variable indicator based on severity)
incorporate stalling: if speed too low, plane spins to ground and accelerates,
if speed high enough, can turn out
takeoff
Random birds
message for crashing
max acceleration
# colored acceleration vectors (use sound?) (use color)
fix hitbox
on-screen instructions: (instructions only in first play?)
	player controls
	don't crash
	acceleration mechanics
	3 shots to death
	during beginning of game?
	instructions menu?
#add music/sounds

"""
