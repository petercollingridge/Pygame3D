import wireframe as wf
import wireframeDisplay as wd

def testWireframes():
    """ Creates a triangle and cuboid wireframe """
    
    triangle = wf.Wireframe()
    triangle.addNodes([[100,200,10], [200,200,10], [125,100,500]])
    triangle.addEdges([(0,1), (1,2), (2,0)])
    triangle.output()
    
    cuboid = wf.getCuboid((100,100,10), (20,30,40))
    cuboid.output()

def testWireframeGroup():
    """ Create a group of wireframes consisting of two cuboids """

    g = wf.WireframeGroup()
    g.addWireframe('cube1', wf.getCuboid((100,100,10), (20,30,40)))
    g.addWireframe('cube2', wf.getCuboid(( 10,200,10), (10,40,20)))        
    g.output()

def testWireframeDisplay():
    viewer = wd.WireframeViewer(600, 400)
    viewer.addWireframe('cube1',  wf.getCuboid((100,100,10), (20,30,40)))
    viewer.addWireframe('cube2',  wf.getCuboid(( 10,200,10), (10,40,20)))
    viewer.run()

testWireframes()
testWireframeGroup()
testWireframeDisplay()
