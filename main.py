from lib import calc3D


window = calc3D.win((800,600))
world = calc3D.world(window.display)
world.background = calc3D.texture("sky.jpg")
house = calc3D.rect(world,(-50,-50,100),(100,100,100),calc3D.texture("sample2.png"))
floor = calc3D.rect(world,(-100,50,300),(300,50,300),calc3D.texture("grass.jpg"))
roof = calc3D.body(world,(0,-75,150),
        [
            [0,0,0],
            [-50,25,50],
            [-50,25,-50],
            [0,0,0],
            [-50,25,-50],
            [50,25,-50],
            [0,0,0],
            [50,25,50],
            [50,25,-50],
            [0,0,0],
            [-50,25,50],
            [50,25,50]
        ]
        ,calc3D.texture("sample.jpg"))

house.move((0,0,300))
roof.move((0,0,300))


def loop(key): 
    house.rotate(0.01,floor.center.pos,0)
    roof.rotate(0.01,floor.center.pos,0)
    floor.rotate(0.01,floor.center.pos,0)
    world.update()
    world.draw(1)    

while True: window.update(loop)    
