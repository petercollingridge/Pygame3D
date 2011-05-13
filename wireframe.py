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
    
    def rotateX(self, y, z, radians):
        """ Rotate wireframe about the x-axis by 'radians' radians """
        
        # Combine translation and rotation with 4D array
        # Used np.matrix instead of np.array?
        
        # Translate to y, z
        self.translate([0, -y, -z])
        
        # Rotate about x
        rotation_matrix = np.array([[1, 0,               0               ],
                                    [0, np.cos(radians), -np.sin(radians)],
                                    [0, np.sin(radians),  np.cos(radians)]])
        self.nodes = np.dot(self.nodes, rotation_matrix)
        
        # Translate back
        self.translate([0, y, z])
        
    def rotateY(self, x, z, radians):
        """ Rotate wireframe about the y-axis by 'radians' radians """
        
        self.translate([-x, 0, -z])
        rotation_matrix = np.array([[np.cos(radians),  0, np.sin(radians)],
                                    [0,                1, 0              ],
                                    [-np.sin(radians), 0, np.cos(radians)]])
        self.nodes = np.dot(self.nodes, rotation_matrix)
        self.translate([x, 0, z])
        
    def rotateZ(self, x, y, radians):
        """ Rotate wireframe about the z-axis by 'radians' radians """
        
        self.translate([-x, -y, 0])
        rotation_matrix = np.array([[np.cos(radians), -np.sin(radians), 0],
                                    [np.sin(radians),  np.cos(radians), 0],
                                    [0,                0,               1]])
        self.nodes = np.dot(self.nodes, rotation_matrix)
        self.translate([x, y, 0])
    
    def findCentre(self):
        """ Find the spatial centre by finding the range of the x, y and z coordinates. """

        min_values = self.nodes.min(axis=0)
        max_values = self.nodes.max(axis=0)

        return 0.5*(min_values[n] + max_values[n])
    
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
    
    def translate(self, v):
        """ Translate each node of each wireframe by a vector, v. """
        
        for wireframe in self.wireframes.values():
            wireframe.translate(v)

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
        min_values = np.array([wireframe.nodes.min(axis=0) for wireframe in self.wireframes.values()]).min(axis=0)
        max_values = np.array([wireframe.nodes.max(axis=0) for wireframe in self.wireframes.values()]).max(axis=0)

        return [0.5*(min_values[n] + max_values[n]) for n in range(3)]
    
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