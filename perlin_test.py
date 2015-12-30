import math
import random

import pygame
import pygame.gfxdraw
from pygame.locals import *

print "initializing pygame..."
pygame.init()

def Interpolate(a, b, x):
    ft = x * 3.1415927
    f = (1 - math.cos(ft)) * .5

    return a*(1-f) + b*f

def Noise1(x):
    x = (x<<13) ^ x
    return ( 1.0 - ( (x * (x * x * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0);  

def SmoothedNoise(x):
    return Noise1(x)/2 + Noise1(x-1)/4 + Noise1(x+1)/4

def InterpolatedNoise_1(x):

    int_X = int(x)
    fractional_X = x - int_X

    v1 = SmoothedNoise(int_X)
    v2 = SmoothedNoise(int_X+1)

    return Interpolate(v1, v2, fractional_X)

def PerlinNoise_1D(x):
    
    total = 0
    p = 0.20
    n = 7

    for i in range(n):

        if i == 0:
            frequency = 1.0
            amplitude = 1.0
        else:
            frequency = 2*i
            amplitude = p*i

        total = total + InterpolatedNoise_1(x * frequency) * amplitude

    return total

def Noise2(x, y):
    n = x + y * 57
    n = (n<<13) ^ n
    return (1.0 - ( (n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0)

def SmoothNoise_2(x, y):
    corners = (Noise2(x-1, y-1)+Noise2(x+1, y-1)+Noise2(x-1, y+1)+Noise2(x+1, y+1) )/16
    sides = ( Noise2(x-1, y)+Noise2(x+1, y)+Noise2(x, y-1)+Noise2(x, y+1))/8
    centre = Noise2(x,y) / 4
    return corners + sides + centre

def InterpolatedNoise_2(x, y):

    int_X = int(x)
    fractional_X = x - int_X

    int_Y = int(y)
    fractional_Y = y - int_Y

    v1 = SmoothNoise_2(int_X, int_Y)
    v2 = SmoothNoise_2(int_X+1, int_Y)
    v3 = SmoothNoise_2(int_X, int_Y+1)
    v4 = SmoothNoise_2(int_X+1, int_Y+1)

    i1 = Interpolate(v1, v2, fractional_X)
    i2 = Interpolate(v3, v4, fractional_X)

    return Interpolate(i1, i2, fractional_Y)

def PerlinNoise_2D(x, y):
    total = 0
    p = 0.40
    n = 5

    for i in range(n):
        if i == 0:
            frequency = 1
            amplitude = 1
        else:
            frequency = 2*i
            amplitude = p*i

            total = total + InterpolatedNoise_2(x*frequency, y*frequency) * amplitude

    return total

print "initializing screen"
screen = pygame.display.set_mode((500,500))
print "initializing game clock"
clock = pygame.time.Clock()

print "rendering noise"
noise = pygame.surface.Surface((200,200))

###### 1D RENDERER #######
#for x in range(noise.get_width()):
#    val = (PerlinNoise_1D(float(x)/150))*10
#    y = 150+val
#    y = int(y)
#    pygame.gfxdraw.line(noise, x, y, x, 300, (255,255,255))
##########################

for x in range(noise.get_width()):
    for y in range(noise.get_height()):
        val = (PerlinNoise_2D(float(x)/80,float(y)/80))*10
        val_color = val*255
        if val_color < 0:
            val_color = 0
        elif val_color > 255:
            val_color = 255
        val_color = (val_color, val_color, val_color)
        pygame.gfxdraw.pixel(noise,x,y,val_color)

print "main loop"
run = True
while run:
    clock.tick(30)
    screen.fill((0,0,0))
    screen.blit(noise, ((500/2)-100,(500/2)-100))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

pygame.quit()
