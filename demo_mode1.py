import sys
import calc3D
from generals import *
import pygame
from pygame.locals import *
import math

pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

# Initialize the world and the objects within

world = calc3D.world(screen)
rect = calc3D.rect(world,(-50,-50,100),(100,100,100),(255,0,0))
rect2 = calc3D.rect(world,(-20,-20,300),(20,20,20),(0,255,0))

rect.move((0,0,300))
rect2.move((0,0,300))

while True:
    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN: debug = True
        elif event.type == KEYUP: False
     
    
    rect.rotate(0.01,rect.center.pos,0)
    rect2.rotate(0.01,rect.center.pos,0)
    rect.rotate(0.01,rect.center.pos,1)

     
    #Draw the and update world  
    world.update()
    world.draw(1)
    world.draw(0)
    
    fpsClock.tick(fps)
    pygame.display.flip()