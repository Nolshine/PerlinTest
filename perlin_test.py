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
	print "creating white noise"
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
	print "creating smooth noise, octave " + str(octave)
	width = len(baseNoise)
	height = len(baseNoise[0])

	smoothNoise = CreateEmptyGrid(width, height)

	samplePeriod = math.pow(2, octave)
	sampleFrequency = 1.0/samplePeriod

	for i in range(width):
		# calculate horizontal sampling indices
		sample_i0 = int(math.floor((i / samplePeriod))) * samplePeriod
		#print str(type(sample_i0))
		sample_i1 = int(math.floor(sample_i0 + samplePeriod)) % width #wrap around
		#print str(type(sample_i1))
		horizontal_blend = (i - sample_i0) * sampleFrequency

		for j in range(height):
			# calculate vertical sampling indices
			sample_j0 = int(math.floor(j / samplePeriod)) * samplePeriod
			#print str(type(sample_j0))
			sample_j1 = int(math.floor((sample_j0 + samplePeriod))) % height #wrap around
			#print str(type(sample_j1))
			vertical_blend = (j - sample_j0) * sampleFrequency

			#blend the top two corners
			top = Interpolate(baseNoise[int(sample_i0)][int(sample_j0)],
            baseNoise[int(sample_i1)][int(sample_j0)], horizontal_blend)

			#blend the bottom two corners
			bottom = Interpolate(baseNoise[int(sample_i0)][int(sample_j1)],
            baseNoise[int(sample_i1)][int(sample_j1)], horizontal_blend)

			#final blend
			smoothNoise[i][j] = Interpolate(top, bottom, vertical_blend)

	return smoothNoise

def GeneratePerlinNoise(baseNoise, octaveCount):
	print "making da perlinz..."

	width = len(baseNoise)
	height = len(baseNoise[0])

	smoothNoise = []

	persistance = 0.5

	# generate smooth noise
	for i in range(octaveCount):
		smoothNoise.append(GenerateSmoothNoise(baseNoise, i))

	perlinNoise = CreateEmptyGrid(width, height)
	amplitude = 1.0
	totalAmplitude = 0.0

	#for (int octave = octaveCount - 1; octave &gt;= 0; octave--)
	for octave in range(octaveCount-1, 0, -1):
		amplitude *= persistance
		totalAmplitude += amplitude

		for i in range(width):
			for j in range(height):
				perlinNoise[i][j] += smoothNoise[octave][i][j] * amplitude
	print "...done."

	# normalisation
	print "normalising noise..."
	for i in range(width):
		for j in range(height):
			perlinNoise[i][j] /= totalAmplitude
	print "...done."

	# complete
	return perlinNoise

if __name__ == "__main__":

	print "Creating base noise..."
	noise = GenerateWhiteNoise(500, 500, 0)
	print "...done."
	perlin = GeneratePerlinNoise(noise, 7)

	#let's attempt to visualize this.

	print "initializing pygame."
	pygame.init()

	screen = pygame.display.set_mode((520, 520))

	clock = pygame.time.Clock()

	# better pre-render the noise...
	print "rendering..."
	render = pygame.Surface((500, 500))
	for column in range(len(perlin)):
		for row in range(len(perlin[0])):
			val = perlin[column][row]*255
			color = (val, val, val)
			render.set_at((column, row), color)
	
	print "...done."
	running = True

	while running:
		
		#render portion for noise

		screen.fill((0,0,0))
		screen.blit(render, (10,10))

		pygame.display.update()

		#event handling portion
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False

pygame.quit()