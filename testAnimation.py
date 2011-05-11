import wireframe as wf
import wireframeDisplay as wd

class AnimatedWireframe(wf.Wireframe):
    def update(self):
        self.translate([0,1,0])

ball = wf.getSpheroid((200,200,300), (30,30,30), 16)
animated_ball = AnimatedWireframe()
animated_ball.nodes = ball.nodes
animated_ball.edges = ball.edges

width, height = 600, 400
viewer = wd.WireframeViewer(width, height)
viewer.addWireframe('floor', wf.getHorizontalGrid((0,height,0), (50,50), (12,12)))
viewer.addWireframe('ball', animated_ball)

# Eye starts at (width/2, height/2, 0). Move to (width/2, height-50, 0)
viewer.translate([0,-150,0])

# Change depending on screen size and now much the eye can fit in view
field_of_view = 0.25
viewer.scale(1/field_of_view)

#viewer.perspective = False

viewer.run()