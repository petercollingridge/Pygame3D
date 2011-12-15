import math
import numpy as np
import wireframe as wf
import wireframeDisplay as wd
import basicShapes as shape

def testWireframe():
    """ Example of how to create wireframes node by node, and by using the basicShape module.
        Creates a triangle and cuboid wireframe and outputs their node, edge and face values. """
    
    # Create a triangle by explictly passing the nodes and edges
    print "\nTriangle"
    triangle = wf.Wireframe([[100,200,10], [200,200,10], [125,100,500]])
    triangle.addEdges([(0,1), (1,2), (2,0)])
    triangle.output()
    
    # Create a cuboid using the basicShape module
    print "\nCuboid"
    cuboid = shape.Cuboid((100,100,10), (20,30,40))
    cuboid.output()

def testTranslate():
    """ Example of how to translate a wireframe.
        Creates a cuboid and translates it by vector (4,3,1). """
    
    cuboid = shape.Cuboid((100,100,10), (20,30,40))
    cuboid.outputNodes()
    
    print "\n> Translate cuboid along vector [4 3 1]"
    cuboid.transform(wf.translationMatrix(4, 3, 1))
    cuboid.outputNodes()
    
def testScale():
    """ Example of how to scale a wireframe.
        Creates a cuboid and scales it by 2, centred on (100,150,200). """
    
    cuboid = shape.Cuboid((100,100,10), (20,30,40))
    cuboid.outputNodes()

    print "\n> Scale cuboid by 2, centred at (100,150,200)"
    cuboid.transform(wf.scaleMatrix(2, 100, 150, 200))
    cuboid.outputNodes()
    
def testRotate():
    """ Example of how to rotate a wireframe.
        Creates a cuboid and rotates about its centre by pi/2 radians. """
    
    cuboid = shape.Cuboid((100,100,10), (20,30,40))
    cuboid.outputNodes()
    
    # Find rotation matrix
    (x,y,z) = cuboid.findCentre()    
    translation_matrix = wf.translationMatrix(-x, -y, -z)
    rotation_matrix = np.dot(translation_matrix, wf.rotateXMatrix(math.pi/2))
    rotation_matrix = np.dot(rotation_matrix, -translation_matrix)
    
    print "\n> Rotate cuboid around its centre and the x-axis"
    cuboid.transform(rotation_matrix)
    cuboid.outputNodes()

def testWireframeGroup():
    """ Example of how to create a group of named wireframes. """

    g = wf.WireframeGroup()
    g.addWireframe('cube1', shape.Cuboid((100,100,10), (20,30,40)))
    g.addWireframe('cube2', shape.Cuboid(( 10,200,10), (10,40,20)))        
    g.output()

def testWireframeDisplay():
    """ Create and display a wireframe cube. """
    
    viewer = wd.WireframeViewer(600, 400)
    viewer.addWireframe('cube', shape.Cuboid((80,150,0), (200,200,200)))
    viewer.displayFaces = False
    viewer.run()

def testSurfaceDisplayWithCube():
    """ Create and display a cube with surfaces. """
    
    viewer = wd.WireframeViewer(600, 400)
    viewer.addWireframe('cube', shape.Cuboid((225,100,0), (200,200,200)))
    viewer.displayEdges = False
    viewer.run()
    
def testSurfaceDisplayWithSphere():
    """ Create and display a cube with surfaces. """
    
    resolution = 52
    viewer = wd.WireframeViewer(600, 400)
    viewer.addWireframe('sphere', shape.Spheroid((300,200, 20), (160,160,160), resolution=resolution))

    # Colour ball
    faces = viewer.wireframes['sphere'].faces
    for i in range(resolution/4):
        for j in range(resolution*2-4):
            f = i*(resolution*4-8) +j
            faces[f][1][1] = 0
            faces[f][1][2] = 0
        
    # Colour with lattitude
    #for (face, colour) in faces[::2]:
    #    colour[1] = 0
    #    colour[2] = 0
    
    print "Create a sphere with %d faces." % len(viewer.wireframes['sphere'].faces)
    viewer.displayEdges = False
    viewer.run()
    
def testWireframeDisplay3():
    """ Create display with two cuboids, a plane and spheroid. """
    
    viewer = wd.WireframeViewer(600, 400)
    viewer.addWireframe('grid',  shape.HorizontalGrid((20,400,0), (40,30), (14,20)))
    viewer.addWireframe('cube1', shape.Cuboid((200,100,400), (20,30,40)))
    viewer.addWireframe('cube2', shape.Cuboid((100,360, 20), (10,40,20)))
    viewer.addWireframe('sphere', shape.Spheroid((250,300, 100), (20,30,40)))
    viewer.run()

def chooseExample():
    examples = ['testWireframe',
                'testTranslate',
                'testScale',
                'testRotate',
                'testWireframeGroup',
                'testWireframeDisplay',
                'testSurfaceDisplayWithCube',
                'testSurfaceDisplayWithSphere',
                'exit']
        
    makingChoice = True    
    while makingChoice:
        print "\nOptions:"
        
        for i, e in enumerate(examples, 1):
            print " %d. %s" % (i, e)
        choice = input("\nChoose an option: ")
        
        if choice > len(examples)-1:
            print '> exit'
            makingChoice = False
        else:
            print "> %s" % examples[choice-1]
            exec("%s()" % examples[choice-1])
    
if __name__ == '__main__':
    chooseExample()
