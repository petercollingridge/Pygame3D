import numpy as np

class Edge:
    def __init__(self, start, stop):
        self.start = start
        self.stop  = stop

class Wireframe:
    def __init__(self):
        self.nodes = np.zeros((0,3))
        self.edges = []

    def addNodes(self, node_array):
        self.nodes = np.vstack((self.nodes, node_array))
    
    def addEdges(self, edgeList):
        for (start, stop) in edgeList:
            self.edges.append(Edge(self.nodes[start], self.nodes[stop]))
    
    def outputNodes(self):
        for i, node in enumerate(self.nodes):
            print "Node %d: (%d, %d, %d)" % (i, node[0], node[1], node[2])
            
    def outputEdges(self):
        for i, edge in enumerate(self.edges):
            print "Edge %d: (%d, %d, %d)" % (i, edge.start[0], edge.start[1], edge.start[2]),
            print "to (%d, %d, %d)" % (edge.stop[0],  edge.stop[1],  edge.stop[2])    
    
    def translate(self, v):
        self.nodes -= v
    
    def scale(self, scale, cx=0, cy=0, cz=0):
        self.nodes *= np.array([scale, scale, scale])

class WireframeGroup:
    def __init__(self):
        self.wireframes = {}
    
    def addWireframe(self, name, wireframe):
        self.wireframes[name] = wireframe
    
    def outputNodes(self):
        for name, wireframe in self.wireframes.items():
            print name
            wireframe.outputNodes()
    
    def outputEdges(self):
        for name, wireframe in self.wireframes.items():
            print name
            wireframe.outputEdges()
    
    def translate(self, v):
        """ Translate each node of each wireframe by a vector, v. """
        
        for wireframe in self.wireframes.values():
            wireframe.translate(v)

def getCuboid(x,y,z,w,h,d):
    """ Return a wireframe cuboid centred on (x,y,z)
        with width, w, height, h, and depth, d. """

    cuboid = Wireframe()
    cuboid.addNodes(np.array([[nx,ny,nz] for nx in (x-w,x+w) for ny in (y-h,y+h) for nz in (z-d,z+d)]))
    cuboid.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])
    

    return cuboid
if __name__ == '__main__':
    cube = getCuboid(100,100,10,20,30,40)
    cube.translate(np.array([10,2,0]))
    
    cube.outputNodes()
    cube.outputEdges()