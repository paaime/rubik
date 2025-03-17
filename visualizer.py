from vpython import *
import time

class CubeVisualizer:
    def __init__(self):
        # Create canvas with better lighting
        scene = canvas(width=800, height=600, center=vector(0,0,0))
        scene.background = color.gray(0.8)
        scene.range = 4

         # Add multiple light sources for better visibility of all faces
        distant_light(direction=vector(0,-1,0), color=color.white)  # Light from below
        distant_light(direction=vector(0,1,0), color=color.white)   # Light from above
        distant_light(direction=vector(1,0,0), color=color.white)   # Light from right
        
        # Set up camera controls
        scene.userpan = True
        scene.userspin = True
        scene.userzoom = True
        
        # Colors for the cube faces
        self.colors = {
            'white': color.white,
            'yellow': color.yellow,
            'red': color.red,
            'orange': vector(1, 0.5, 0),  # Proper orange color
            'blue': color.blue,
            'green': color.green,
            'black': color.gray(0.2)  # Dark gray instead of pure black for better visibility
        }
        
        # Create cubelets with proper faces
        self.cubelets = []
        self.cube_obj = {}  # Store cubelet and its faces
        self.create_cube()
        
    def create_cube(self):
        # Create 27 small cubes (3x3x3)
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                for z in [-1, 0, 1]:
                    # Create compound object for each cubelet
                    pieces = []
                    
                    # Core cubelet
                    core = box(pos=vector(x,y,z), size=vector(0.9,0.9,0.9), 
                              color=self.colors['black'])
                    pieces.append(core)
                    
                    # Add colored stickers to the cubelet
                    # Right face (x=1) - Red
                    if x == 1:
                        sticker = box(pos=vector(x+0.45,y,z), size=vector(0.05,0.8,0.8),
                                     color=self.colors['red'])
                        pieces.append(sticker)
                    
                    # Left face (x=-1) - Orange
                    if x == -1:
                        sticker = box(pos=vector(x-0.45,y,z), size=vector(0.05,0.8,0.8),
                                     color=self.colors['orange'])
                        pieces.append(sticker)
                    
                    # Top face (y=1) - White
                    if y == 1:
                        sticker = box(pos=vector(x,y+0.45,z), size=vector(0.8,0.05,0.8),
                                     color=self.colors['white'])
                        pieces.append(sticker)
                    
                    # Bottom face (y=-1) - Yellow
                    if y == -1:
                        sticker = box(pos=vector(x,y-0.45,z), size=vector(0.8,0.05,0.8),
                                     color=self.colors['yellow'])
                        pieces.append(sticker)
                    
                    # Front face (z=1) - Green
                    if z == 1:
                        sticker = box(pos=vector(x,y,z+0.45), size=vector(0.8,0.8,0.05),
                                     color=self.colors['green'])
                        pieces.append(sticker)
                    
                    # Back face (z=-1) - Blue
                    if z == -1:
                        sticker = box(pos=vector(x,y,z-0.45), size=vector(0.8,0.8,0.05),
                                     color=self.colors['blue'])
                        pieces.append(sticker)
                    
                    # Create compound object from all pieces
                    cubelet = compound(pieces, pos=vector(x,y,z))
                    self.cubelets.append(cubelet)
    
    def apply_move(self, move, cube_state=None):
        # Add a text display of the current move
        move_text = label(pos=vector(0, 3, 0), text=f"Move: {move}", height=16, color=color.black)
        
        # Define rotation parameters
        angle = 0
        axis = vector(0,0,0)
        face_selector = lambda c: False  # Will be replaced based on move
        
        # Set up parameters based on the move
        if move == 'R':
            angle = -pi/2
            axis = vector(1,0,0)
            face_selector = lambda c: c.pos.x > 0.5
        elif move == "R'":
            angle = pi/2
            axis = vector(1,0,0)
            face_selector = lambda c: c.pos.x > 0.5
        elif move == 'R2':
            angle = pi
            axis = vector(1,0,0)
            face_selector = lambda c: c.pos.x > 0.5
        elif move == 'L':
            angle = pi/2
            axis = vector(1,0,0)
            face_selector = lambda c: c.pos.x < -0.5
        elif move == "L'":
            angle = -pi/2
            axis = vector(1,0,0)
            face_selector = lambda c: c.pos.x < -0.5
        elif move == 'L2':
            angle = pi
            axis = vector(1,0,0)
            face_selector = lambda c: c.pos.x < -0.5
        elif move == 'U':
            angle = -pi/2
            axis = vector(0,1,0)
            face_selector = lambda c: c.pos.y > 0.5
        elif move == "U'":
            angle = pi/2
            axis = vector(0,1,0)
            face_selector = lambda c: c.pos.y > 0.5
        elif move == 'U2':
            angle = pi
            axis = vector(0,1,0)
            face_selector = lambda c: c.pos.y > 0.5
        elif move == 'D':
            angle = pi/2
            axis = vector(0,1,0)
            face_selector = lambda c: c.pos.y < -0.5
        elif move == "D'":
            angle = -pi/2
            axis = vector(0,1,0)
            face_selector = lambda c: c.pos.y < -0.5
        elif move == 'D2':
            angle = pi
            axis = vector(0,1,0)
            face_selector = lambda c: c.pos.y < -0.5
        elif move == 'F':
            angle = -pi/2
            axis = vector(0,0,1)
            face_selector = lambda c: c.pos.z > 0.5
        elif move == "F'":
            angle = pi/2
            axis = vector(0,0,1)
            face_selector = lambda c: c.pos.z > 0.5
        elif move == 'F2':
            angle = pi
            axis = vector(0,0,1)
            face_selector = lambda c: c.pos.z > 0.5
        elif move == 'B':
            angle = pi/2
            axis = vector(0,0,1)
            face_selector = lambda c: c.pos.z < -0.5
        elif move == "B'":
            angle = -pi/2
            axis = vector(0,0,1)
            face_selector = lambda c: c.pos.z < -0.5
        elif move == 'B2':
            angle = pi
            axis = vector(0,0,1)
            face_selector = lambda c: c.pos.z < -0.5
        
        # Animate the move
        moving_cubelets = [c for c in self.cubelets if face_selector(c)]
        
        # Perform animation
        steps = 10
        for i in range(steps):
            rate(20)  # Controls animation speed
            for cubelet in moving_cubelets:
                cubelet.rotate(angle=angle/steps, axis=axis, origin=vector(0,0,0))
        
        # Wait a bit for visibility
        time.sleep(0.2)
        
        # Remove the move label after animation
        move_text.visible = False