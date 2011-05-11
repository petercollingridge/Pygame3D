import wireframe as wf
import wireframeDisplay as wd
import pygame

width, height = 600, 400
viewer = wd.WireframeViewer(width, height)

viewer.addWireframe('floor',   wf.getHorizontalGrid((0,400,0), (40,40), (10,10)))
viewer.addWireframe('ceiling', wf.getHorizontalGrid((0,250,0), (40,40), (10,10)))
viewer.addWireframe('back wall',  wf.getCuboid((-10,250,400), (420,150, 10)))
viewer.addWireframe('left wall',  wf.getCuboid((-10,250,  0), ( 10,150,400)))
viewer.addWireframe('right wall', wf.getCuboid((400,250,  0), ( 10,150,400)))
viewer.addWireframe('back block', wf.getCuboid((125,250,200), (150,150,200)))

# Move so that eye at (200,150,40) is at (0,400,0)
viewer.translate([200,-150,-50])

# Change depending on screen size
field_of_view = 0.25
viewer.scale(1/field_of_view)

# Override keyboard controls
wd.key_to_function[pygame.K_UP]    = (lambda x: x.translate([0, 0, -40]))
wd.key_to_function[pygame.K_DOWN]  = (lambda x: x.translate([0, 0,  40]))
wd.key_to_function[pygame.K_LEFT]  = (lambda x: x.rotateY(-wd.rotation_amount, (width/2,0)))
wd.key_to_function[pygame.K_RIGHT] = (lambda x: x.rotateY( wd.rotation_amount, (width/2,0)))
wd.key_to_function[pygame.K_q] = (lambda x: x.rotateX(-wd.rotation_amount, (height/2+50,0)))
wd.key_to_function[pygame.K_w] = (lambda x: x.rotateX( wd.rotation_amount, (height/2+50,0)))

viewer.run()