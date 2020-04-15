import math
import pygame
from pygame.locals import *
from generals import *
import os

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
    for i in range(len(ret)): ret[i] += v2.pos[i]
    v = vec3d(tuple(ret))
    return v

def subvec(v1,v2):
    ret = list(v1.pos)
    for i in range(len(ret)): ret[i] -= v2.pos[i]
    v = vec2d(tuple(ret))
    return v          

def mulvec(v1,n):
    ret = list(v1.pos)
    for i in range(len(ret)): ret[i] *= n
    v = vec2d(tuple(ret))
    return v 

def divvec(v1,num):
    n = num
    if n == 0: n = -0.1
    ret = list(v1.pos)
    for i in range(len(ret)): ret[i] = int(ret[i]/n)
    v = vec2d(tuple(ret))
    return v 

 
#3d vectors to computate dimensions easily       
class vec3d(object):
    def __init__(self,pos):
        self.pos = pos
        
    def get2d(self,fpos):
        v = vec2d((self.pos[0],self.pos[1]))
        if self.pos[2] >= 0: v = divvec(mulvec(v,40),root(self.pos[2]))
        else: v = addvec(divvec(mulvec(v,40),root(0)),divvec(mulvec(v,20),root(0)))            
        return v

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
        
    def move(self,pos): self.world.movepol(self.pol_ID,pos)
    def rotate(self,val,pos,axis): self.world.polrotate(self.pol_ID,val,pos,axis)
        
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
    
    def addvec(self,v):
        self.vec.append(v)
        self.vec2.append(v.get2d(self.fpoint))
        self.vcount += 1
        
    def addpol(self,l): 
        self.pol.append(l)
        self.pcount += 1
    
    def movevec(self,v,val): self.vec[v] = addvec3d(self.vec[v],vec3d(val))
    
    def setvec(self,v,val): self.vec[v] = vec3d(val)
        
    def movepol(self,ID,val):
        for v in self.pol[ID]: self.vec[v] = addvec3d(self.vec[v],vec3d(val))
        
    def polrotate(self,ID,val,pos,axis):
        p = list(pos)
        
        x,y,z = 0,0,0

        
        if axis == 0:
            for v in self.pol[ID]:    
                x = p[0] + math.cos(val)*(self.vec[v].pos[0] - p[0]) - math.sin(val)*(self.vec[v].pos[2] - p[2])           
                z = p[2] + math.sin(val)*(self.vec[v].pos[0] - p[0]) + math.cos(val)*(self.vec[v].pos[2] - p[2])
                y = self.vec[v].pos[1] 
                self.vec[v].pos = (x,y,z) 
                
        elif axis == 1:
            for v in self.pol[ID]:
                x = p[0] + math.cos(val)*(self.vec[v].pos[0] - p[0]) - math.sin(val)*(self.vec[v].pos[1] - p[1])           
                y = p[1] + math.sin(val)*(self.vec[v].pos[0] - p[0]) + math.cos(val)*(self.vec[v].pos[1] - p[1])
                z = self.vec[v].pos[2]
                self.vec[v].pos = (x,y,z)
         
        elif axis == 2:
            for v in self.pol[ID]:
                x = self.vec[v].pos[0]           
                y = p[1] + math.sin(val)*(self.vec[v].pos[2] - p[2]) + math.cos(val)*(self.vec[v].pos[1] - p[1])
                z = p[2] + math.cos(val)*(self.vec[v].pos[2] - p[2]) - math.sin(val)*(self.vec[v].pos[1] - p[1])
                self.vec[v].pos = (x,y,z)
         
        
    def sortpol(self,p,c): 
        unsorted_z = []
        sorted_z = []
        sorted_col = []
        ret = []
        
        for p in p:
            a = 0
            b = 0
            for n in p:
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
            self.vec2[i] = self.vec[i].get2d(self.fpoint)
            i += 1
        
        
    def draw(self,mode):  
        pl,c = self.sortpol(self.pol, self.col)
        
        j = 0
        for p in pl:
            p2 = []
            neg = True
            for i in p:  
                p2.append(addvec(self.vec2[i],vec2d(self.fpoint)).pos)
                if self.vec[i].pos[2] >  0:  neg = False
            if not neg: 
                if mode == 0: pygame.draw.lines(self.disp,(255,255,255),True,p2)  
                elif mode == 1: pygame.draw.polygon(self.disp,c[j],p2)  
            j += 1

           

