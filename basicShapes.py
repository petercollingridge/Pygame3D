import numpy as np
import wireframe as wf

def Cuboid((x,y,z), (w,h,d)):
    """ Return a wireframe cuboid starting at (x,y,z)
        with width, w, height, h, and depth, d. """

    cuboid = wf.Wireframe()
    cuboid.addNodes(np.array([[nx,ny,nz] for nx in (x,x+w) for ny in (y,y+h) for nz in (z,z+d)]))
    cuboid.addFaces([(0,1,3,2), (4,5,7,6)])
    cuboid.addFaces([(0,1,5,4), (2,3,7,6)])
    cuboid.addFaces([(0,2,6,4), (1,3,7,5)])
    
    return cuboid
    
def Spheroid((x,y,z), (rx, ry, rz), resolution=10):
    """ Returns a wireframe spheroid centred on (x,y,z)
        with a radii of (rx,ry,rz) in the respective axes. """
    
    spheroid   = wf.Wireframe()
    latitudes  = [n*np.pi/resolution for n in range(1,resolution)]
    longitudes = [n*2*np.pi/resolution for n in range(resolution)]

    # Add nodes except for poles
    spheroid.addNodes([(x + rx*np.sin(n)*np.sin(m), y - ry*np.cos(m), z - rz*np.cos(n)*np.sin(m)) for m in latitudes for n in longitudes])

    # Add square faces to whole spheroid but poles
    num_nodes = resolution*(resolution-1)
    spheroid.addFaces([(m+n, m+(n+1)%resolution, (m+resolution)%resolution**2+(n+1)%resolution, (m+resolution)%num_nodes+n) for n in range(resolution) for m in range(0,num_nodes-resolution,resolution)])

    # Add poles and triangular faces around poles
    spheroid.addNodes([(x, y+ry, z),(x, y-ry, z)])
    spheroid.addFaces([(num_nodes+1, (n+1)%resolution, n) for n in range(resolution)])
    start_node = num_nodes-resolution
    spheroid.addFaces([(num_nodes, start_node+n, start_node+(n+1)%resolution) for n in range(resolution)])

    return spheroid
    
def HorizontalGrid((x,y,z), (dx,dz), (nx,nz)):
    """ Returns a nx by nz wireframe grid that starts at (x,y,z) with width dx.nx and depth dz.nz. """
    
    grid = wf.Wireframe()
    grid.addNodes([[x+n1*dx, y, z+n2*dz] for n1 in range(nx+1) for n2 in range(nz+1)])
    grid.addEdges([(n1*(nz+1)+n2,n1*(nz+1)+n2+1) for n1 in range(nx+1) for n2 in range(nz)])
    grid.addEdges([(n1*(nz+1)+n2,(n1+1)*(nz+1)+n2) for n1 in range(nx) for n2 in range(nz+1)])
    
    return grid
    
def FractalLandscape(origin=(0,0,0), dimensions=(400,400), iterations=4, height=40):
    import random
    
    def midpoint(nodes):
        m = 1.0/ len(nodes)
        x = m * sum(n[0] for n in nodes) 
        y = m * sum(n[1] for n in nodes) 
        z = m * sum(n[2] for n in nodes) 
        return [x,y,z]
    
    (x,y,z) = origin
    (dx,dz) = dimensions
    nodes = [[x, y, z], [x+dx, y, z], [x+dx, y, z+dz], [x, y, z+dz]]
    edges = [(0,1), (1,2), (2,3), (3,0)]
    size = 2

    for i in range(iterations):
        # Add nodes midway between each edge
        for (n1, n2) in edges:
            nodes.append(midpoint([nodes[n1], nodes[n2]]))

        # Add nodes to the centre of each square
        squares = [(x+y*size, x+y*size+1, x+(y+1)*size+1, x+(y+1)*size) for y in range(size-1) for x in range(size-1)]
        for (n1,n2,n3,n4) in squares:
            nodes.append(midpoint([nodes[n1], nodes[n2], nodes[n3], nodes[n4]]))
        
        # Sort in order of grid
        nodes.sort(key=lambda node: (node[2],node[0]))
        
        size = size*2-1
        # Horizontal edge
        edges = [(x+y*size, x+y*size+1) for y in range(size) for x in range(size-1)]
        # Vertical edges
        edges.extend([(x+y*size, x+(y+1)*size) for x in range(size) for y in range(size-1)])
        
        # Shift node heights
        scale = height/2**(i*0.8)
        for node in nodes:
            node[1] += (random.random()-0.5)*scale
    
    grid = wf.Wireframe(nodes)
    grid.addEdges(edges)
    
    return grid
    
if __name__ == '__main__':
    grid = FractalLandscape(origin = (0,400,0), iterations=1)
    grid.output()