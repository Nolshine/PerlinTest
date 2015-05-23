"""
Test project to attempt to implement some perlin noise in python.
"""

import math
import random
import pygame
from pygame.locals import *

def CreateEmptyGrid(width, height):
	grid = []
	for i in range(width):
		grid.append([])
		for n in range(height):
			grid[i].append(0.000)

	return grid

def GenerateWhiteNoise(width, height, seed):
	local_generator = random.Random()
	local_generator.seed(seed)
	noise = CreateEmptyGrid(width, height)

	for col in range(len(noise)):
		for row in range(len(noise[col])):
			noise[col][row] = local_generator.random()

	return noise

def Interpolate(x0, x1, alpha):
	return x0 * (1 - alpha) + alpha * x1

def GenerateSmoothNoise(baseNoise, octave):
	width = len(baseNoise)
	height = len(baseNoise[0])

	smoothNoise = CreateEmptyGrid(width, height)

	samplePeriod = math.pow(2, octave)
	sampleFrequency = 1.0/samplePeriod

	for i in range(width):
		# calculate horizontal sampling indices
		sample_i0 = int(math.floor((i / samplePeriod) * samplePeriod))
		#print str(type(sample_i0))
		sample_i1 = int(math.floor((sample_i0 + samplePeriod) % width)) #wrap around
		#print str(type(sample_i1))
		horizontal_blend = (i - sample_i0) * sampleFrequency

		for j in range(height):
			# calculate vertical sampling indices
			sample_j0 = int(math.floor((j / samplePeriod) * samplePeriod))
			#print str(type(sample_j0))
			sample_j1 = int(math.floor((sample_j0 + samplePeriod) % height)) #wrap around
			#print str(type(sample_j1))
			vertical_blend = (j - sample_j0) * sampleFrequency

			#blend the top two corners
			top = Interpolate(baseNoise[sample_i0][sample_j0],
            baseNoise[sample_i1][sample_j0], horizontal_blend)

			#blend the bottom two corners
			bottom = Interpolate(baseNoise[sample_i0][sample_j1],
            baseNoise[sample_i1][sample_j1], horizontal_blend)

			#final blend
			smoothNoise[i][j] = Interpolate(top, bottom, vertical_blend)

	return smoothNoise

if __name__ == "__main__":
	noise = []
	noise.append(GenerateWhiteNoise(50, 50, 0))  # seed 0 for testing

	for i in range(20): #8 octaves
		noise.append(GenerateSmoothNoise(noise[0], i))


	#let's attempt to visualize this.

	pygame.init()

	screen = pygame.display.set_mode((300, 300))
	draw = pygame.Surface((70, 70))

	clock = pygame.time.Clock()

	state = 0
	running = True

	while running:
		
		#render portion for noise
		noiseReference = noise[state]

		draw.fill((0,0,0))
		for column in range(len(noiseReference)):
			for row in range(len(noiseReference[column])):
				val = int(noiseReference[column][row]*255)
				x = column+10
				y = row+10
				color = (val, val, val)
				draw.set_at((x, y), color)

		screen.blit(pygame.transform.smoothscale(draw, (300, 300)), (0, 0))

		pygame.display.update()

		#event handling portion
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			if (event.type == KEYDOWN):
				if event.key == K_SPACE:
					state += 1
					if state == len(noise):
						state = 0
					print "Noise number... " + str(state)

pygame.quit()