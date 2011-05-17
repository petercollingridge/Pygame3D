import math
import wireframe as wf
import wireframeDisplay as wd

def testWireframes():
    """ Creates a triangle and cuboid wireframe. """
    
    triangle = wf.Wireframe()
    triangle.addNodes([[100,200,10], [200,200,10], [125,100,500]])
    triangle.addEdges([(0,1), (1,2), (2,0)])
    triangle.output()
    
    cuboid = wf.getCuboid((100,100,10), (20,30,40))
    cuboid.output()
    print cuboid.nodes

def testTranslate():
    """ Creates a cuboid and translates it by vector (4,3,1). """
    
    cuboid = wf.getCuboid((100,100,10), (20,30,40))
    cuboid.output()
    cuboid.translate(4, 3, 1)
    cuboid.output()
    
def testScale():
    """ Creates a cuboid and scales it by 2, centred on (100,150,200). """
    
    cuboid = wf.getCuboid((100,100,10), (20,30,40))
    cuboid.output()
    cuboid.scale(2, 100, 150, 200)
    cuboid.output()
    
def testRotate():
    """ Creates a cuboid and rotates about its centre by pi/2 radians. """
    
    cuboid = wf.getCuboid((100,100,10), (20,30,40))
    cuboid.output()
    (x,y,z) = cuboid.findCentre()
    cuboid.rotateX(y, z, math.pi/2)
    cuboid.output()

def testWireframeGroup():
    """ Create a group of wireframes consisting of two cuboids. """

    g = wf.WireframeGroup()
    g.addWireframe('cube1', wf.getCuboid((100,100,10), (20,30,40)))
    g.addWireframe('cube2', wf.getCuboid(( 10,200,10), (10,40,20)))        
    g.output()

def testWireframeDisplay():
    """ Create display with a cube """
    
    viewer = wd.WireframeViewer(600, 400)
    viewer.addWireframe('cube', wf.getCuboid((80,150,0), (200,200,200)))
    viewer.run()

def testWireframeDisplay2():
    """ Create display with two cuboids, a plane and spheroid """
    
    viewer = wd.WireframeViewer(600, 400)
    viewer.addWireframe('grid',  wf.getHorizontalGrid((20,400,0), (40,30), (14,20)))
    viewer.addWireframe('cube1', wf.getCuboid((200,100,400), (20,30,40)))
    viewer.addWireframe('cube2', wf.getCuboid((100,360, 20), (10,40,20)))
    viewer.addWireframe('sphere', wf.getSpheroid((250,300, 100), (20,30,40)))
    viewer.run()

#testWireframes()
#testScale()
#testRotate()
#testWireframeGroup()
testWireframeDisplay2()