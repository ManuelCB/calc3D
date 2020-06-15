import math
import pygame
import pygame.gfxdraw
import os
import sys
from pygame.locals import *
from .generals import *


#Transform float positions into simple integers to avoid Errors
def simplifypos(p): return (int(p[0]),int(p[1]))

def root(p):
    if p > 0:  return math.sqrt(p)
    elif p < 0: return math.sqrt(-p)
    else: return 0.1
   
#2d vectors are used for 3d representation, 3d vectors have a function witch turn them into representable 2d coordinates    
class vec2d(object):
    
    def __init__(self,pos):
        self.pos = pos 
        
    def pointatX(self,x):
        a = x/self.pos[0]
        b = self.pos[1]*a
        return (x,b)
        
    def pointatY(self,y):
        b = y/self.pos[1]
        a = self.pos[0]*b
        return (a,y)


#simple vector operations        
def addvec(v1,v2):
    ret = list(v1.pos)
    for i in range(len(ret)): ret[i] += v2.pos[i]
    v = vec2d(tuple(ret))
    return v

def addvec3d(v1,v2):
    ret = list(v1.pos)
    su = list(v2.pos)
    for i in range(len(ret)): ret[i] += su[i]
    v = vec3d(tuple(ret))
    return v

def subvec(v1,v2):
    ret = list(v1.pos)
    for i in range(len(ret)): ret[i] -= v2.pos[i]
    v = vec2d(tuple(ret))
    return v          

def subvec3d(v1,v2):
    ret = list(v1.pos)
    for i in range(len(ret)): ret[i] -= v2.pos[i]
    v = vec3d(tuple(ret))
    return v   

def mulvec(v1,n):
    ret = list(v1.pos)
    for i in range(len(ret)): ret[i] *= n
    v = vec2d(tuple(ret))
    return v 

def mulvec(v1,n):
    ret = list(v1.pos)
    for i in range(len(ret)): ret[i] *= n
    v = vec3d(tuple(ret))
    return v 

def divvec(v1,num):
    n = num
    if n == 0: n = -0.1
    ret = list(v1.pos)
    for i in range(len(ret)): ret[i] = int(ret[i]/n)
    v = vec2d(tuple(ret))
    return v 

def divvec3d(v1,num):
    n = num
    if n == 0: n = -0.1
    ret = list(v1.pos)
    for i in range(len(ret)): ret[i] = int(ret[i]/n)
    v = vec3d(tuple(ret))
    return v 
 
def absvec3d(v):
    ret = []
    for p in v.pos: ret.append(abs(p))
    return vec3d(tuple(ret))

#Using shapely to get if a 2d polygon is totally inside another one

def totally_inside(p1,p2):
    ret = True
    for p in p2:
        if not Polygon(p1).contains(Point(p)):
            ret = False
            break
    return ret

#Shitty texture loading

def texture(path): return pygame.image.load(os.path.join(os.getcwd(),'res','img',path))
    
#3d vectors to computate dimensions easily       
class vec3d(object):
    def __init__(self,pos):
        self.pos = pos
        
    def get2d(self):
        v = vec2d((self.pos[0],self.pos[1]))
        if self.pos[2] >= 0: v = divvec(mulvec(v,40),root(self.pos[2]))
        else: v = addvec(divvec(mulvec(v,40),root(0)),divvec(mulvec(v,20),root(0)))            
        return v

        p = list(pos)
        
        x,y,z = 0,0,0

    def rotate(self,val,p,axis):
        
        x = self.pos[0]
        y = self.pos[1]
        z = self.pos[2]
        
        if axis == 0:  
            x = p[0] + math.cos(val)*(self.pos[0] - p[0]) - math.sin(val)*(self.pos[2] - p[2])           
            z = p[2] + math.sin(val)*(self.pos[0] - p[0]) + math.cos(val)*(self.pos[2] - p[2])
                
        elif axis == 1:
            x = p[0] + math.cos(val)*(self.pos[0] - p[0]) - math.sin(val)*(self.pos[1] - p[1])           
            y = p[1] + math.sin(val)*(self.pos[0] - p[0]) + math.cos(val)*(self.pos[1] - p[1])
         
        elif axis == 2:      
            y = p[1] + math.sin(val)*(self.pos[2] - p[2]) + math.cos(val)*(self.pos[1] - p[1])
            z = p[2] + math.cos(val)*(self.pos[2] - p[2]) - math.sin(val)*(self.pos[1] - p[1])
        
        self.pos = (x,y,z)

   
    def getDistance(self,p):    
        ret = 0
        vec = subvec3d(self,vec3d(p))
        for v in vec.pos: ret += pow(v,2)
        ret = math.sqrt(ret)
        return ret
        
    def getAngles(self,p):
        
        vec = subvec3d(self,vec3d(p))
        
        angle_xz  = math.atan2(vec.pos[0],vec.pos[2])
        angle_xy = math.atan2(vec.pos[0],vec.pos[1])
        
        return angle_xz, angle_xy
        
        
        
        
        
        

 #objects based on 3d vectors
 
class triangle(object): 
    def  __init__(self,w,poss,col): 
        self.points = [poss[0],poss[1],poss[2]]
        po = []
        for p in self.points:
            po.append(w.vcount)
            w.addvec(vec3d(p))
        w.addpol(po) 
        self.pol_ID = w.pcount-1
        self.world = w
        self.col = col
        w.col.append(col)
        self.center = vec3d(((poss[0][0] + poss[1][0] + poss[2][0])/3,(poss[0][1] + poss[1][1] + poss[2][1])/3,(poss[0][2] + poss[1][2] + poss[2][2])/3))
        
    def move(self,pos): 
        self.world.movepol(self.pol_ID,pos)
        self.center = addvec3d(self.center,vec3d(pos))
        
    def rotate(self,val,pos,axis): 
        self.world.polrotate(self.pol_ID,val,pos,axis)
        self.center.rotate(val,pos,axis)

        
class rect(object):
    def __init__(self,w,p,dim,col):
        self.triangles = []
        self.world = w
        pos = vec3d(p)
        self.col = col
        
        tr = [
            [
                pos,
                addvec3d(pos,vec3d((dim[0],0,0))),
                addvec3d(pos,vec3d((0,dim[1],0))),
                addvec3d(pos,vec3d((dim[0],dim[1],0)))
            ],
            [
                pos,
                addvec3d(pos,vec3d((0,0,dim[2]))),
                addvec3d(pos,vec3d((0,dim[1],0))),
                addvec3d(pos,vec3d((0,dim[1],dim[2])))
            ],
            [
                addvec3d(pos,vec3d((0,0,dim[2]))),
                addvec3d(pos,vec3d((dim[0],0,dim[2]))),
                addvec3d(pos,vec3d((0,dim[1],dim[2]))),
                addvec3d(pos,vec3d((dim[0],dim[1],dim[2])))
            ],
            [
                addvec3d(pos,vec3d((dim[0],0,0))),
                addvec3d(pos,vec3d((dim[0],0,dim[2]))),
                addvec3d(pos,vec3d((dim[0],dim[1],0))),
                addvec3d(pos,vec3d((dim[0],dim[1],dim[2])))
            ],
            [
                pos,
                addvec3d(pos,vec3d((0,0,dim[2]))),
                addvec3d(pos,vec3d((dim[0],0,0))), 
                addvec3d(pos,vec3d((dim[0],0,dim[2])))                             
            ],
            [
                addvec3d(pos,vec3d((0,dim[1],0))),
                addvec3d(pos,vec3d((0,dim[1],dim[2]))),
                addvec3d(pos,vec3d((dim[0],dim[1],0))),
                addvec3d(pos,vec3d((dim[0],dim[1],dim[2])))                   
            ]
        ]
        
        for q in tr:
            self.triangles.append(triangle(self.world,(q[0].pos,q[1].pos,q[2].pos),col))
            self.triangles.append(triangle(self.world,(q[3].pos,q[1].pos,q[2].pos),col))
            
        self.center = vec3d((p[0]+dim[0]/2,p[1]+dim[1]/2,p[2]+dim[2]/2))
        
    def move(self,pos):
        for t in self.triangles: t.move(pos)
        self.center = addvec3d(self.center,vec3d(pos))
        
    def rotate(self,val,pos,axis):
        for t in self.triangles: t.rotate(val,pos,axis)
        
        
class body(object):
    def __init__(self,w,p,points,col):
    
        self.triangles = []
        self.world = w
        self.col = col
        
        self.origin = vec3d(p)
        
        i = 0
        
        while (i+2) < len(points):
            self.triangles.append(triangle(self.world,(points[i],points[i+1],points[i+2]),self.col))
            i += 1
            
        self.triangles.append(triangle(self.world,(points[i],points[i+1],points[0]),self.col)) 
        self.triangles.append(triangle(self.world,(points[i+1],points[0],points[1]),self.col))
        
        self.move(p)
        
    def move(self,pos):
        for t in self.triangles: t.move(pos)
        
    def rotate(self,val,pos,axis):
        for t in self.triangles: t.rotate(val,pos,axis)            
        
       

        
class world(object):

    def __init__(self,s):
        self.vec = []
        self.vec2 = []
        self.pol = []
        self.col = []
        self.fpoint = (s.get_size()[0]/2,s.get_size()[1]/2)
        self.disp = s
        self.vcount = 0
        self.pcount = 0
        self.disp_polygon = [[0,0],[0,self.disp.get_size()[0],0],self.disp.get_size(),[0,self.disp.get_size()[1]]]
        self.background = None
    
    def addvec(self,v):
        self.vec.append(v)
        self.vec2.append(v.get2d())
        self.vcount += 1
        
    def addpol(self,l): 
        self.pol.append(l)
        self.pcount += 1
    
    def movevec(self,v,val): self.vec[v] = addvec3d(self.vec[v],vec3d(val))
    
    def setvec(self,v,val): self.vec[v] = vec3d(val)
        
    def movepol(self,ID,val):
        for v in self.pol[ID]: self.vec[v] = addvec3d(self.vec[v],vec3d(val))
        
    def polrotate(self,ID,val,pos,axis):       
        for v in self.pol[ID]:   self.vec[v].rotate(val,pos,axis)
         
        
    def sortpol(self,p,c): 
        unsorted_z = []
        sorted_z = []
        sorted_col = []
        ret = []
        
        for p0 in p:
            a = 0
            b = 0
            for n in p0:
                a += self.vec[n].pos[2]
                b += 1
            unsorted_z.append(round(a/b,3))
            sorted_z.append(round(a/b,3))
        
        
        sorted_z.sort()
        
        takensorts = []
        
        for u in unsorted_z:
            i = 0
            for s in sorted_z: 
                taken = False
                if u == s:
                    if len(takensorts) > 0:
                        taken = False
                        for t in takensorts:
                            if i == t:
                                taken = True
                                break
                    if not taken:
                        ret.append(self.pol[i])
                        sorted_col.append(self.col[i])
                        takensorts.append(i)                   
                i += 1
        
        ret.reverse()
        sorted_col.reverse()
        
        return ret, sorted_col


        
    def update(self):
        i = 0
        while i < len(self.vec):
            self.vec2[i] = self.vec[i].get2d()
            i += 1
        
        
    def draw(self,mode): 
        
        #draw background if exists
        
        if type(self.background) is pygame.Surface: 
            self.disp.blit(self.background,(0,0))
        elif type(self.background) is tuple: self.disp.fill(self.background)
        else: self.disp.fill((0,0,0))
        
        pl,c = self.sortpol(self.pol, self.col)
        
        j = 0
        for p in pl:
            p2 = []
            p3 = []
            p1 = []
            neg = True
            
            for i in p:  
                p2.append(addvec(self.vec2[i],vec2d(self.fpoint)).pos)
                if self.vec[i].pos[2] >  0:  neg = False
                
            try: 
                for i in pl[j+1]: p3.append(addvec(self.vec2[i],vec2d(self.fpoint)).pos)
            except IndexError: pass

            try: 
                for i in pl[j-1]: p1.append(addvec(self.vec2[i],vec2d(self.fpoint)).pos)
            except IndexError: pass
            
            if not neg: 
                if mode == 0: pygame.draw.lines(self.disp,(255,255,255),True,p2)  
                elif mode == 1:                
                    if type(c[j]) is tuple: pygame.draw.polygon(self.disp,c[j],p2)
                    elif type(c[j]) is pygame.Surface: pygame.gfxdraw.textured_polygon(self.disp,p2,c[j],0,0)
                    
            j += 1
            
class win(object):

    def __init__(self,dim):
        self.display = pygame.display.set_mode(dim)
        self.clock = pygame.time.Clock()
        self.fps = 60
        
    def update(self,func):
    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
        func(pygame.key.get_pressed())
        
        self.clock.tick(self.fps)
        pygame.display.flip()
