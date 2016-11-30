import pygame, sys, random, time, math
from pygame.locals import *

FPS = 30
WINWIDTH = 700
WINHEIGHT = 500
HALF_WIDTH = int(WINWIDTH/2)
HALF_HEIGHT = int(WINHEIGHT/2)

GREEN = (24, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

#Make the main Window
mainWindow = pygame.display.set_mode((WINWIDTH,WINHEIGHT))
pygame.display.set_caption('Hack the zombies!!')

pygame.draw.rect(mainWindow,RED, (200,150, 100, 50))

def main():
	global FPSCLOCK, mainWindow, basicFont, sonarImage, zombieImg, background, axeImage, zombies, playerObj

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	mainWindow = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
	pygame.display.set_caption('Hack The Zombies!!')
	basicFont = pygame.font.Font('freesansbold.ttf', 32)

	zombies = []
	playerObj = {'x':50,
				 'y':50,
				 'angle':0,
				 'score':0}

	#Load images
	zombieImg = pygame.image.load('img/zombie.png')
	background = pygame.image.load('img/background.png')
	axeImage = pygame.image.load('img/axe.png')
	sonarImage = pygame.image.load('img/sonar.png')

	while True:
		runGame()

def runGame():
	gameOverMode = False

	#win screen when the player has killed all the zombies
	winSurf = basicFont.render('You have killed zombies!!!', True, WHITE)
	winRect = winSurf.get_rect()
	winRect.center = (HALF_WIDTH, HALF_HEIGHT)

	moveLeft = False
	moveRight = False
	moveUp = False
	moveDown = False
	turnLeft = False
	turnRight = False

	while True:
		#moving the zombies
		for zombie in zombies:
			zombie['x'] += zombie['movex']
			zombie['y'] += zombie['movey']
			if zombie['x'] < 0:
				zombie['x'] = 0
			if zombie['x'] > 100:
				zombie['x'] = 100
			if zombie['y'] < 0:
				zombie['y'] = 0
			if zombie['y'] > 100:
				zombie['y'] = 100

			#random change of direction
			if random.randint(0,99) < 2:
				zombie['movex'] = getRandomVelocity()
				zombie['movey'] = getRandomVelocity()

		#add more zombies
		while len(zombies) < 100:
			zombies.append(makeNewZombie())

		#draw the background
		mainWindow.blit(background, pygame.Rect(0, 0, 700, 500))

		#draw the other zombies
		for zombie in zombies:
			x, y = getTrueCoord(zombie['x'], zombie['y'])
			if y > 0 and x > -25 and x < 25:
				dist = int(math.sqrt((x*x) + (y*y)))
				mainWindow.blit(pygame.transform.scale(zombie['surface'], (zombie['width'], zombie['height'])), pygame.Rect(250 + x*10, 250 + y*10, x+25, 350))
				pass
			pass

		#draw the axe
		mainWindow.blit(pygame.transform.scale(axeImage, (140, 100)), pygame.Rect(550, 380, 140, 100))

		#draw the view at bottom
		drawSonar()

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key in (K_UP, K_w):
					moveDown = False
					moveUp = True
				elif event.key in (K_DOWN, K_s):
					moveUp = False
					moveDown = True
				elif event.key in (K_LEFT, K_a):
					moveRight = False
					moveLeft = True
				elif event.key in (K_RIGHT, K_d):
					moveLeft = False
					moveRight = True
			elif event.type == KEYUP:
				if event.key in (K_LEFT, K_a):
					moveLeft = False
				elif event.key in (K_RIGHT, K_d):
					moveRight = False
				elif event.key in (K_UP, K_w):
					moveUp = False
				elif event.key in (K_DOWN, K_s):
					moveDown = False
				elif event.key == K_SPACE:
					checkFront()
				elif event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
			elif event.type == MOUSEMOTION:
				turnLeft, turnRight = changeAngle(event)
			elif event.type == MOUSEBUTTONUP:
				checkFront()

		if not gameOverMode:
			if moveLeft:
				playerObj['x'] = max(playerObj['x'] - 3, 0)
			if moveRight:
				playerObj['x'] = min(playerObj['x'] + 3, 100)
			if moveDown:
				playerObj['y'] = max(playerObj['y'] - 3, 0)
			if moveUp:
				playerObj['y'] = min(playerObj['y'] + 3, 100)
			if turnRight:
				playerObj['angle'] -= 1
			if turnLeft:
				playerObj['angle'] += 1
			if playerObj['angle'] < 0:
				playerObj['angle'] += 360
			elif playerObj['angle'] > 360:
				playerObj['angle'] -= 360

			#Check if any collision with zombie
			for i in range(len(zombies)-1, -1, -1):
				zomb = zombies[i]
		else:
			mainWindow.blit(winSurf, winRect)

		pygame.display.update()
		FPSCLOCK.tick(FPS)

def changeAngle(movement):
	mousePos = movement.pos
	if mousePos[0] <= 150:
		return True, False
	elif mousePos[0] < 350:
		return False, False
	else:
		return False, True

def checkFront():
	pass

def drawSonar():
	mainWindow.blit(pygame.transform.scale(sonarImage, (150, 150)), pygame.Rect(5, 345, 150, 150))
	for zombie in zombies:
		x, y = getTrueCoord(zombie['x'], zombie['y'])
		sonarX = int(x*3)
		sonarY = int(y*3)
		if sonarX > -75 and sonarX < 75 and sonarY > -75 and sonarY < 75:
			pygame.draw.circle(mainWindow, GREEN, (5 + 75 + sonarX, 345 + 75 + sonarY), 5, 0)

def getTrueCoord(x, y):
	x -= playerObj['x']
	y -= playerObj['y']
	newX = (x * math.cos(math.radians(playerObj['angle']))) + (y * math.sin(math.radians(playerObj['angle'])))
	newY = (-x * math.sin(math.radians(playerObj['angle']))) + (y * math.cos(math.radians(playerObj['angle'])))
	return newX, newY

def getRandomPos():
	x = random.randint(0, 100)
	y = random.randint(0, 100)
	return x, y

def makeNewZombie():
	zomb={}
	generalSize = random.randint(5, 25)
	multiplier = random.randint(1, 3)
	zomb['width'] = (generalSize + random.randint(0, 10)) * multiplier
	zomb['height'] = (generalSize + random.randint(0, 10)) * multiplier
	zomb['x'], zomb['y'] = getRandomPos()
	zomb['movex'] = getRandomVelocity()
	zomb['movey'] = getRandomVelocity()
	zomb['surface'] = pygame.transform.scale(zombieImg, (zomb['width'], zomb['height']))
	return zomb

def getRandomVelocity():
	speed = random.randint(0,1)
	if random.randint(0,1) == 0:
		return speed
	else:
		return -speed

if __name__ == '__main__':
	main()