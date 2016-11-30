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
	global FPSCLOCK, mainWindow, basicFont, zombieImg, background, axeImage, zombies

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	mainWindow = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
	pygame.display.set_caption('Hack The Zombies!!')
	basicFont = pygame.font.Font('freesansbold.ttf', 32)

	zombies = []

	#Load images
	zombieImg = pygame.image.load('img/zombie.png')
	background = pygame.image.load('img/background.png')
	axeImage = pygame.image.load('img/axe.png')

	while True:
		runGame()

def runGame():
	gameOverMode = False

	#win screen when the player has killed all the zombies
	winSurf = basicFont.render('You have killed zombies!!!', True, WHITE)
	winRect = winSurf.get_rect()
	winRect.center = (HALF_WIDTH, HALF_HEIGHT)

	#stores player info
	playerObj = {'x':50,
				 'y':50,
				 'angle':0}

	moveLeft = False
	moveRight = False
	moveUp = False
	moveDown = False

	while True:
		#moving the zombies
		for zombie in zombies:
			zombie['x'] += zombie['movex']
			zombie['y'] += zombie['movey']

			#random change of direction
			if random.randint(0,99) < 2:
				zombie['movex'] = getRandomVelocity()
				zombie['movey'] = getRandomVelocity()

		#add more zombies
		while len(zombies) < 10:
			zombies.append(makeNewZombie())

		#draw the background
		mainWindow.blit(background, pygame.Rect(0, 0, 700, 500))

		#draw the other zombies
		for zombie in zombies:
			pass

		#draw the axe
		mainWindow.blit(axeImage, pygame.Rect())

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
				changeAngle()
			elif event.type == MOUSEBUTTONUP:
				checkFront()

		if not gameOverMode:
			if moveLeft:
				playerObj['x'] -= 3
			if moveRight:
				playerObj['x'] += 3
			if moveDown:
				playerObj['y'] -= 3
			if moveUp:
				playerObj['y'] += 3

			#Check if any collision with zombie
			for i in range(len(zombies)-1, -1, -1):
				zomb = zombies[i]
		else:
			mainWindow.blit(winSurf, winRect)

		pygame.display.update()
		FPSCLOCK.tick(FPS)

def changeAngle():
	pass

def checkFront():
	pass

def drawSonar():
	pass

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
	speed = random.randint(0,7)
	if random.randint(0,1) == 0:
		return speed
	else:
		return -speed

if __name__ == '__main__':
	main()