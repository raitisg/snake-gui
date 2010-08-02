#!/usr/bin/python

import curses, sys, random, pygame
from time import sleep

# snake's directions (this snake lives in 2D world, so...)
DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3

# redraw and refresh entire screen
def redraw():
	screen.blit(background, background_rect)
	drawFood()
	drawSnake()
	pygame.display.flip()

# draw snake
def drawSnake():
	global snake_head
	global snake_tail
	n = 0
	for pos in snake:
		if n == 0:
			screen.blit(snake_head, [pos[0]*10, pos[1]*10])
		else:
			screen.blit(snake_tail, [pos[0]*10, pos[1]*10])
		n += 1


# draw all the food
def drawFood():
	for pos in food:
		screen.blit(snake_food, [pos[0]*10, pos[1]*10])

# check if snake has just eaten the food
def isFoodCollision():
	for pos in food:
		if pos == snake[0]:
			food.remove(pos)
			return True
	return False

# check if snake has just commited suicide
def isSuicide():
	for i in xrange(0, len(snake)):
		if i > 0 and snake[i] == snake[0]:
			return True
	return False

# move snake one step forward
def moveSnake():
	global snake
	global grow_snake
	global cols, rows

	# get head
	head = snake[0]

	# remove tail
	if (grow_snake == False):
		snake.pop()
	else:
		grow_snake = False

	# calculate where head will be
	if (dir == DIR_UP):
		head = [head[0], head[1]-1]
		if head[1] == -1:
			head[1] = rows
	elif (dir == DIR_RIGHT):
		head = [head[0]+1, head[1]]
		if head[0] == cols:
			head[0] = 0
	elif (dir == DIR_DOWN):
		head = [head[0], head[1]+1]
		if head[1] == rows:
			head[1] = 0
	elif (dir == DIR_LEFT):
		head = [head[0]-1, head[1]]
		if head[0] == -1:
			head[0] = cols-1

	# insert new head
	snake.insert(0, head)

	if isSuicide():
		gameOver()

# drop new food, but not on snake or on another food
def dropFood():
	x = random.randint(0, cols-1)
	y = random.randint(0, rows-1)
	for pos in food:
		if pos == [x,y]:
			dropFood()
			return

	for pos in snake:
		if pos == [x,y]:
			dropFood()
			return

	food.append([x,y])

# stop all the action and print the sad news
def gameOver():
	global is_game_over
	global snake
	is_game_over = True


# init -------------------------------------------------------------------------

field = []
snake = [[10,5], [9,5], [8,5], [7,5]]
dir = DIR_RIGHT;
food = []
grow_snake = False
is_game_over = False

# start in non paused mode
paused = False

rows = 23
cols = 23


pygame.init()

size = width, height = 230, 230

screen = pygame.display.set_mode(size)

background = pygame.image.load("background.png")
background_rect = background.get_rect()

snake_head = pygame.image.load("head.png")
snake_tail = pygame.image.load("tail.png")
snake_food = pygame.image.load("food.png")


# start -------------------------------------------------------------------------

dropFood()
redraw()

while 1:

	sleep(0.1)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if (event.key == pygame.K_UP):
				if dir != DIR_DOWN:
					dir = DIR_UP
			elif (event.key == pygame.K_RIGHT):
				if dir != DIR_LEFT:
					dir = DIR_RIGHT
			elif (event.key == pygame.K_DOWN):
				if dir != DIR_UP:
					dir = DIR_DOWN
			elif (event.key == pygame.K_LEFT):
				if dir != DIR_RIGHT:
					dir = DIR_LEFT
			elif (event.key == pygame.K_SPACE):
				paused = not paused
				redraw()
			elif (event.key == pygame.K_q):
				sys.exit()

	if (is_game_over == False and paused == False):
		redraw()
		moveSnake()

		if (isFoodCollision()):
			dropFood()
			grow_snake = True