class Cube:
    """
    Represents a Rubik's cube state.
    cP: corner permutation (0-7)
    cO: corner orientation (0-2) - 0=good, 1=clockwise, 2=anti-clockwise
    eP: edge permutation (0-11)
    eO: edge orientation (0-1) - 0=good, 1=bad
    """
    def __init__(self):
        self.cP = [i for i in range(8)]  # Corner permutation
        self.cO = [0] * 8               # Corner orientation  
        self.eP = [i for i in range(12)]  # Edge permutation
        self.eO = [0] * 12              # Edge orientation
        self.move = ""                  # Last move
        self.move2 = ""                 # Move before last

    def copy(self):
        """Create a copy of this cube"""
        new_cube = Cube()
        new_cube.cP = self.cP.copy()
        new_cube.cO = self.cO.copy()
        new_cube.eP = self.eP.copy()
        new_cube.eO = self.eO.copy()
        new_cube.move = self.move
        new_cube.move2 = self.move2
        return new_cube
    
    def is_solved(self):
        """Returns true if this cube is solved"""
        # Check corner permutation
        for i in range(len(self.cP)):
            if self.cP[i] != i:
                return False
        
        # Check corner orientation
        for i in range(len(self.cO)):
            if self.cO[i] != 0:
                return False
        
        # Check edge permutation
        for i in range(len(self.eP)):
            if self.eP[i] != i:
                return False
        
        # Check edge orientation
        for i in range(len(self.eO)):
            if self.eO[i] != 0:
                return False
        
        return True

    def get_subgroup(self):
        """Returns the subgroup for this cube state"""
        # edges not oriented -> 0
        for i in range(len(self.eO)):
            if self.eO[i] != 0:
                return 0
        
        # corners not oriented -> 1
        for i in range(len(self.cO)):
            if self.cO[i] != 0:
                return 1
        
        # edges LR slice not in slice -> 1
        for i in range(8, 12):
            if self.eP[i] < 8:
                return 1
        
        # corners not in tetrads -> 2
        for i in range(0, 4):
            if self.cP[i] > 3:
                return 2
        
        for i in range(4, 8):
            if self.cP[i] < 4:
                return 2
        
        # edges FB slice not in slice -> 2
        for i in range(0, 4):
            if self.eP[i] > 3:
                return 2
        
        # edges UD slice not in slice -> 2
        for i in range(4, 8):
            if self.eP[i] < 4 or self.eP[i] > 7:
                return 2
        
        # corners parity odd -> 2
        parity = 0
        for i in range(len(self.cP)):
            if self.cP[i] == i:
                parity += 1
        
        if parity % 2 != 0:
            return 2
        
        # Not solved completely -> 3
        if not self.is_solved():
            return 3
        
        # Solved
        return 4