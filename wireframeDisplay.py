import pygame, math
import numpy as np
import wireframe as wf

# Radian rotated by a key event
ROTATION_AMOUNT = np.pi/32
MOVEMENT_AMOUNT = 10

key_to_function = {
    pygame.K_LEFT:   (lambda x: x.transform(wf.translationMatrix(dx=-MOVEMENT_AMOUNT))),
    pygame.K_RIGHT:  (lambda x: x.transform(wf.translationMatrix(dx= MOVEMENT_AMOUNT))),
    pygame.K_UP:     (lambda x: x.transform(wf.translationMatrix(dy=-MOVEMENT_AMOUNT))),
    pygame.K_DOWN:   (lambda x: x.transform(wf.translationMatrix(dy= MOVEMENT_AMOUNT))),
    pygame.K_EQUALS: (lambda x: x.scale(1.25)),
    pygame.K_MINUS:  (lambda x: x.scale(0.8)),
    pygame.K_q:      (lambda x: x.rotate('x', ROTATION_AMOUNT)),
    pygame.K_w:      (lambda x: x.rotate('x',-ROTATION_AMOUNT)),
    pygame.K_a:      (lambda x: x.rotate('y', ROTATION_AMOUNT)),
    pygame.K_s:      (lambda x: x.rotate('y',-ROTATION_AMOUNT)),
    pygame.K_z:      (lambda x: x.rotate('z', ROTATION_AMOUNT)),
    pygame.K_x:      (lambda x: x.rotate('z',-ROTATION_AMOUNT))
    }

class WireframeViewer(wf.WireframeGroup):
    """ A group of wireframes which can be displayed on a Pygame screen """
    
    def __init__(self, width, height, name="Wireframe Viewer"):
        self.width = width
        self.height = height
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(name)
        
        self.wireframes = {}
        self.wireframe_colours = {}
        self.object_to_update = []
        
        self.displayNodes = False
        self.displayEdges = True
        
        self.perspective = 300.
        self.eyeX = self.width/2
        self.eyeY = 100
        
        self.background = (10,10,50)
        self.nodeColour = (250,250,250)
        self.nodeRadius = 4
    
    def addWireframe(self, name, wireframe):
        self.wireframes[name] = wireframe
        #   If colour is set to None, then wireframe is not displayed
        self.wireframe_colours[name] = (250,250,250)
    
    def addWireframeGroup(self, wireframe_group):
        # Potential danger of overwriting names
        for name, wireframe in wireframe_group.wireframes.items():
            self.addWireframe(name, wireframe)
    
    def scale(self, scale):
        """ Scale wireframes in all directions from the centre of the group. """
        
        scale_matrix = wf.scaleMatrix(scale, self.width/2, self.height/2, 0)
        self.transform(scale_matrix)

    def rotate(self, axis, amount):
        (x, y, z) = self.findCentre()
        translation_matrix1 = wf.translationMatrix(-x, -y, -z)
        translation_matrix2 = wf.translationMatrix(x, y, z)
        
        if axis == 'x':
            rotation_matrix = wf.rotateXMatrix(amount)
        elif axis == 'y':
            rotation_matrix = wf.rotateYMatrix(amount)
        elif axis == 'z':
            rotation_matrix = wf.rotateZMatrix(amount)
            
        rotation_matrix = np.dot(np.dot(translation_matrix1, rotation_matrix), translation_matrix2)
        self.transform(rotation_matrix)

    def display(self):
        self.screen.fill(self.background)
        
        for name, wireframe in self.wireframes.items():
            colour = self.wireframe_colours.get(name)
            if colour:
               for (n1, n2) in wireframe.edges:
                    if self.perspective:
                        if wireframe.nodes[n1][2] > -self.perspective and wireframe.nodes[n2][2] > -self.perspective:
                            z1 = self.perspective/ (self.perspective+wireframe.nodes[n1][2])
                            x1 = self.width/2  + z1*(wireframe.nodes[n1][0] - self.width/2)
                            y1 = self.height/2 + z1*(wireframe.nodes[n1][1] - self.height/2)
                
                            z2 = self.perspective/ (self.perspective+wireframe.nodes[n2][2])
                            x2 = self.width/2  + z2*(wireframe.nodes[n2][0] - self.width/2)
                            y2 = self.height/2 + z2*(wireframe.nodes[n2][1] - self.height/2)
                            
                            pygame.draw.aaline(self.screen, colour, (x1, y1), (x2, y2), 1)
                    else:
                        pygame.draw.aaline(self.screen, colour, (wireframe.nodes[n1][0], wireframe.nodes[n1][1]), (wireframe.nodes[n2][0], wireframe.nodes[n2][1]), 1)
            
            if self.displayNodes:
                for node in wireframe.nodes:
                    pygame.draw.circle(self.screen, colour, (int(node[0]), int(node[1])), self.nodeRadius, 0)
        
        pygame.display.flip()

    def keyEvent(self, key):
        if key in key_to_function:
            key_to_function[key](self)

    def run(self):
        """ Display wireframe on screen and respond to keydown events """
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.keyEvent(event.key)
            
            self.display()
            self.update()
            
        pygame.quit()