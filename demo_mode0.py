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

# Initialize the world and the position of the points

world = calc3D.world(screen)
vecs = [calc3D.vec3d((-50,50,40)),calc3D.vec3d((50,50,40)),calc3D.vec3d((50,50,5)),calc3D.vec3d((-50,50,5)),
        calc3D.vec3d((-50,-50,40)),calc3D.vec3d((50,-50,40)),calc3D.vec3d((50,-50,5)),calc3D.vec3d((-50,-50,5))]
        

for v in vecs: world.addvec(v)

# Join the points and form a cube   
 
world.addpol([0,1,2,3])
world.addpol([4,5,6,7])
world.addpol([0,4,5,1])
world.addpol([2,6,7,3])

for i in range(4): world.col.append((200,40+30*i,100-10*i))

world.movepol(0,(0,0,160))
world.movepol(1,(0,0,160))


# set the rotation point

p = 185


debug = False


while True:
    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN: debug = True
        elif event.type == KEYUP: False
         
    #Rotate and move the cube
    world.polrotate(0,0.01,(0,0,p),0)
    world.polrotate(1,0.01,(0,0,p),0) 
    world.polrotate(0,0.01,(0,0,p),1)
    world.polrotate(1,0.01,(0,0,p),1) 
    world.polrotate(0,0.01,(0,0,p),2)
    world.polrotate(1,0.01,(0,0,p),2)
        
    #Draw the and update world  
    world.update()
    world.draw(0)
    
    fpsClock.tick(fps)
    pygame.display.flip()