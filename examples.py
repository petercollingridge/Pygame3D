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

def testWireframeRotate():
    """" Creates a cuboid and rotates it about the x-axis. """
    
    cuboid = wf.getCuboid((100,100,10), (20,30,40))
    cuboid.output()
    cuboid.rotateX(0, 0, 0.2)
    cuboid.output()

def testWireframeGroup():
    """ Create a group of wireframes consisting of two cuboids. """

    g = wf.WireframeGroup()
    g.addWireframe('cube1', wf.getCuboid((100,100,10), (20,30,40)))
    g.addWireframe('cube2', wf.getCuboid(( 10,200,10), (10,40,20)))        
    g.output()

def testWireframeDisplay():
    """ Create display with two cuboids, a plane and spheroid """
    
    viewer = wd.WireframeViewer(600, 400)
    viewer.addWireframe('grid',  wf.getHorizontalGrid((20,400,0), (40,30), (14,20)))
    viewer.addWireframe('cube1', wf.getCuboid((200,100,400), (20,30,40)))
    viewer.addWireframe('cube2', wf.getCuboid((100,360, 20), (10,40,20)))
    viewer.addWireframe('sphere', wf.getSpheroid((250,300, 100), (20,30,40)))
    viewer.run()

#testWireframes()
#testWireframeRotate()
#testWireframeGroup()
testWireframeDisplay()