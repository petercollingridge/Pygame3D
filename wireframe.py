import numpy as np

class Wireframe:
    """ An array of 3D vectors and connecting edges """
    
    def __init__(self):
        self.nodes = np.zeros((0,3))
        self.edges = []

    def addNodes(self, node_array):
        self.nodes = np.vstack((self.nodes, node_array))
    
    def addEdges(self, edge_list):
        # Is it better to use a for loop or generate a long list then add it?
        # Should raise exception if edge value > len(self.nodes)
        self.edges += [edge for edge in edge_list if edge not in self.edges]
    
    def output(self):
        self.outputNodes()
        self.outputEdges()    
    
    def outputNodes(self):
        for i, node in enumerate(self.nodes):
            print "Node %d: (%d, %d, %d)" % (i, node[0], node[1], node[2])

    def outputEdges(self):
        for i, edge in enumerate(self.edges):
            print "Edge %d: %d -> %d" % (i, edge[0], edge[1])  
    
    def translate(self, v):
        """ Translate by vector, v. """
        self.nodes += v
    
    def scale(self, scale, x=0, y=0, z=0):
        """ Scale relative to the origin then translate to given point, (x,y,z). """
        
        self.nodes *= np.array([scale, scale, scale])
        self.translate(np.array([(1-scale)*x, (scale-1)*-y, (1-scale)*-z]))
    
    def findCentre(self):
        """ Find the spatial centre by finding the range of the x, y and z coordinates. """

        min_values = [self.nodes[:,n].min() for n in range(3)]
        max_values = [self.nodes[:,n].max() for n in range(3)]
        
        return [0.5*(min_values[n] + max_values[n]) for n in range(3)]

class WireframeGroup:
    """ A dictionary of wireframes and methods to manipulate them all together """
    
    def __init__(self):
        self.wireframes = {}
    
    def addWireframe(self, name, wireframe):
        self.wireframes[name] = wireframe
    
    def output(self):
        for name, wireframe in self.wireframes.items():
            print name
            wireframe.output()    
    
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

    def scale(self, scale, (x, y, z)):
        """ Scale wireframes in all directions from a given point, (x,y,z). """
        
        for wireframe in self.wireframes.values():
            wireframe.scale(scale, x, y, z)
    
    def findCentre(self):
        """ Find the central point of all the wireframes. """
        
        min_values = [min((wireframe.nodes[:,n].min() for wireframe in self.wireframes.values())) for n in range(3)]
        max_values = [max((wireframe.nodes[:,n].max() for wireframe in self.wireframes.values())) for n in range(3)]
        
        return [0.5*(min_values[n] + max_values[n]) for n in range(3)]
    
def getCuboid((x,y,z), (w,h,d)):
    """ Return a wireframe cuboid centred on (x,y,z)
        with width, w, height, h, and depth, d. """

    cuboid = Wireframe()
    cuboid.addNodes(np.array([[nx,ny,nz] for nx in (x-w,x+w) for ny in (y-h,y+h) for nz in (z-d,z+d)]))
    cuboid.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])
    
    return cuboid