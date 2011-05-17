import numpy as np

class Wireframe:
    """ An array of 3D vectors and connecting edges """
    
    def __init__(self):
        self.nodes = np.zeros((0,4))
        self.edges = []

    def addNodes(self, node_array):
        """ Append 1s to a list of 3-tuples and add to self.nodes """
        ones_added = np.hstack((node_array, np.ones((len(node_array),1))))
        self.nodes = np.vstack((self.nodes, ones_added))
    
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
    
    def transform(self, transformation_matrix):
        """ Apply a transformation defined by a transformation matrix """
        self.nodes = np.dot(self.nodes, transformation_matrix)
    
    def translate(self, dx=0, dy=0, dz=0):
        """ Translate by vector [dx, dy, dz] """
        self.nodes = np.dot(self.nodes, np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[dx,dy,dz,1]]))
    
    def scale(self, s, cx=0, cy=0, cz=0):
        """ Scale equally along all axes centred on the point (cx,cy,cz). """
        self.nodes = np.dot(self.nodes, np.array([[s, 0, 0, 0],
                                                  [0, s, 0, 0],
                                                  [0, 0, s, 0],
                                                  [cx*(1-s), cy*(1-s), cz*(1-s), 1]]))
    
    def rotateX(self, y, z, radians):
        """ Rotate wireframe about the x-axis by 'radians' radians """
        
        c = np.cos(radians)
        s = np.sin(radians)
        self.nodes = np.dot(self.nodes, np.array([[1, 0, 0, 0],
                                                 [0, c,-s, 0],
                                                 [0, s, c, 0],
                                                 [0, -y*c-z*s+y, y*s-z*c+z, 1]]))
        
    def rotateY(self, x, z, radians):
        """ Rotate wireframe about the y-axis by 'radians' radians """
        
        c = np.cos(radians)
        s = np.sin(radians)
        self.nodes = np.dot(self.nodes, np.array([[ c, 0, s, 0],
                                                  [ 0, 1, 0, 0],
                                                  [-s, 0, c, 0],
                                                  [ z*s-x*c+x, 0, -z*c-x*s+z, 1]]))
        
    def rotateZ(self, x, y, radians):
        """ Rotate wireframe about the z-axis by 'radians' radians """
        
        c = np.cos(radians)
        s = np.sin(radians)
        rotation_matrix = np.array([[c,-s, 0, 0],
                                    [s, c, 0, 0],
                                    [0, 0, 1, 0],
                                    [-x*c-y*s+x, x*s-c*y+y, 0, 1]])
        self.nodes = np.dot(self.nodes, rotation_matrix)
    
    def findCentre(self):
        """ Find the spatial centre by finding the range of the x, y and z coordinates. """

        min_values = self.nodes[:,:-1].min(axis=0)
        max_values = self.nodes[:,:-1].max(axis=0)
        return 0.5*(min_values + max_values)
    
    def update(self):
        """ Override this function to control wireframe behaviour """
        pass

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
    
    def translate(self, dx=0, dy=0, dz=0):
        """ Translate by vector [dx, dy, dz] """
        
        for wireframe in self.wireframes.values():
            wireframe.translate(dx, dy, dz)

    def scale(self, scale, (x, y, z)):
        """ Scale wireframes in all directions from a given point, (x,y,z). """
        
        for wireframe in self.wireframes.values():
            wireframe.scale(scale, x, y, z)
    
    def rotateX(self, radians, centre = None):
        """ Rotate wireframes by 'radians' radians
            about a vector parallel to x-axis and passing through the centre of the wireframes """
        
        if not centre:
            (cx, cy, cz) = self.findCentre()
        else:
            (cy, cz) = centre
        
        for wireframe in self.wireframes.values():
            wireframe.rotateX(cy, cz, radians)
        
    def rotateY(self, radians, centre = None):
        """ Rotate wireframes by 'radians' radians
            about a vector parallel to y-axis and passing through the centre of the wireframes """
        
        if not centre:
            (cx, cy, cz) = self.findCentre()
        else:
            (cx, cz) = centre
        
        for wireframe in self.wireframes.values():
            wireframe.rotateY(cx, cz, radians)
        
    def rotateZ(self, radians, centre = None):
        """ Rotate wireframes by 'radians' radians
            about a vector parallel to y-axis and passing through the centre of the wireframes """
        
        if not centre:
            (cx, cy, cz) = self.findCentre()
        else:
            (cx, cy) = centre
        
        for wireframe in self.wireframes.values():
            wireframe.rotateZ(cx, cy, radians)
    
    def findCentre(self):
        """ Find the central point of all the wireframes. """
        
        # There may be a more efficient way to find the minimums for a group of wireframes
        min_values = np.array([wireframe.nodes[:,:-1].min(axis=0) for wireframe in self.wireframes.values()]).min(axis=0)
        max_values = np.array([wireframe.nodes[:,:-1].max(axis=0) for wireframe in self.wireframes.values()]).max(axis=0)
        return 0.5*(min_values + max_values)
    
    def update(self):
        for wireframe in self.wireframes.values():
            wireframe.update()
    
def getCuboid((x,y,z), (w,h,d)):
    """ Return a wireframe cuboid starting at (x,y,z)
        with width, w, height, h, and depth, d. """

    cuboid = Wireframe()
    cuboid.addNodes(np.array([[nx,ny,nz] for nx in (x,x+w) for ny in (y,y+h) for nz in (z,z+d)]))
    cuboid.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])
    
    return cuboid

def getSpheroid((x,y,z), (rx, ry, rz), resolution=10):
    """ Returns a wireframe spheroid centred on (x,y,z)
        with a radius of (rx,ry,rz) in the respective axes. """
    
    spheriod = Wireframe()
    latitudes  = [n*np.pi/resolution for n in range(1,resolution)]
    longitudes = [n*2*np.pi/resolution for n in range(resolution)]

    # Add nodes except for poles
    spheriod.addNodes([(x + rx*np.sin(n)*np.sin(m), y - ry*np.cos(m), z - rz*np.cos(n)*np.sin(m)) for m in latitudes for n in longitudes])

    # Add lines of latitudes
    spheriod.addEdges([(n*resolution+m, n*resolution+(m+1)%resolution) for n in range(resolution-1) for m in range(resolution)])
    
    # Add lines of longitude (don't reach poles)
    spheriod.addEdges([(n*resolution+m, (n+1)*resolution+m) for n in range(resolution-2) for m in range(resolution)])

    # Add poles and joining edges
    spheriod.addNodes([(x, y+ry, z),(x, y-ry, z)])
    spheriod.addEdges([(len(spheriod.nodes)-1, n) for n in range(resolution)])
    spheriod.addEdges([(len(spheriod.nodes)-2, len(spheriod.nodes)-3-n) for n in range(resolution)])

    return spheriod

def getHorizontalGrid((x,y,z), (dx,dz), (nx,nz)):
    """ Returns a nx by nz wireframe grid that starts at (x,y,z) with width dx.nx and depth dz.nz. """
    
    grid = Wireframe()
    grid.addNodes(np.array([[x+n1*dx, y, z+n2*dz] for n1 in range(nx+1) for n2 in range(nz+1)]))
    grid.addEdges([(n1*(nz+1)+n2,n1*(nz+1)+n2+1) for n1 in range(nx+1) for n2 in range(nz)])
    grid.addEdges([(n1*(nz+1)+n2,(n1+1)*(nz+1)+n2) for n1 in range(nx) for n2 in range(nz+1)])
    
    return grid