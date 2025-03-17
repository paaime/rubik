import sys
from utils import modulo3

def spin_U(cube):
    """U move (up face clockwise)"""
    # corner permutation
    tmp = cube.cP[0]
    cube.cP[0] = cube.cP[4]
    cube.cP[4] = cube.cP[3]
    cube.cP[3] = cube.cP[7]
    cube.cP[7] = tmp
    
    # edge permutation
    tmp = cube.eP[0]
    cube.eP[0] = cube.eP[8]
    cube.eP[8] = cube.eP[3]
    cube.eP[3] = cube.eP[11]
    cube.eP[11] = tmp
    
    # corner orientation
    cube.cO[cube.cP[0]] = modulo3(cube.cO[cube.cP[0]] - 1)
    cube.cO[cube.cP[3]] = modulo3(cube.cO[cube.cP[3]] - 1)
    cube.cO[cube.cP[4]] = modulo3(cube.cO[cube.cP[4]] + 1)
    cube.cO[cube.cP[7]] = modulo3(cube.cO[cube.cP[7]] + 1)
    
    # edge orientation
    cube.eO[cube.eP[0]] = (cube.eO[cube.eP[0]] + 1) % 2
    cube.eO[cube.eP[3]] = (cube.eO[cube.eP[3]] + 1) % 2
    cube.eO[cube.eP[8]] = (cube.eO[cube.eP[8]] + 1) % 2
    cube.eO[cube.eP[11]] = (cube.eO[cube.eP[11]] + 1) % 2

def spin_D(cube):
    """D move (down face clockwise)"""
    # corner permutation
    tmp = cube.cP[1]
    cube.cP[1] = cube.cP[5]
    cube.cP[5] = cube.cP[2]
    cube.cP[2] = cube.cP[6]
    cube.cP[6] = tmp
    
    # edge permutation
    tmp = cube.eP[1]
    cube.eP[1] = cube.eP[10]
    cube.eP[10] = cube.eP[2]
    cube.eP[2] = cube.eP[9]
    cube.eP[9] = tmp
    
    # corner orientation
    cube.cO[cube.cP[1]] = modulo3(cube.cO[cube.cP[1]] - 1)
    cube.cO[cube.cP[2]] = modulo3(cube.cO[cube.cP[2]] - 1)
    cube.cO[cube.cP[5]] = modulo3(cube.cO[cube.cP[5]] + 1)
    cube.cO[cube.cP[6]] = modulo3(cube.cO[cube.cP[6]] + 1)
    
    # edge orientation
    cube.eO[cube.eP[1]] = (cube.eO[cube.eP[1]] + 1) % 2
    cube.eO[cube.eP[10]] = (cube.eO[cube.eP[10]] + 1) % 2
    cube.eO[cube.eP[2]] = (cube.eO[cube.eP[2]] + 1) % 2
    cube.eO[cube.eP[9]] = (cube.eO[cube.eP[9]] + 1) % 2

def spin_F(cube):
    """F move (front face clockwise)"""
    # corner permutation
    tmp = cube.cP[4]
    cube.cP[4] = cube.cP[1]
    cube.cP[1] = cube.cP[6]
    cube.cP[6] = cube.cP[3]
    cube.cP[3] = tmp
    
    # edge permutation
    tmp = cube.eP[5]
    cube.eP[5] = cube.eP[9]
    cube.eP[9] = cube.eP[6]
    cube.eP[6] = cube.eP[8]
    cube.eP[8] = tmp
    
    # corner orientation
    cube.cO[cube.cP[1]] = modulo3(cube.cO[cube.cP[1]] + 1)
    cube.cO[cube.cP[3]] = modulo3(cube.cO[cube.cP[3]] + 1)
    cube.cO[cube.cP[4]] = modulo3(cube.cO[cube.cP[4]] - 1)
    cube.cO[cube.cP[6]] = modulo3(cube.cO[cube.cP[6]] - 1)

def spin_B(cube):
    """B move (back face clockwise)"""
    # corner permutation
    tmp = cube.cP[7]
    cube.cP[7] = cube.cP[2]
    cube.cP[2] = cube.cP[5]
    cube.cP[5] = cube.cP[0]
    cube.cP[0] = tmp
    
    # edge permutation
    tmp = cube.eP[7]
    cube.eP[7] = cube.eP[10]
    cube.eP[10] = cube.eP[4]
    cube.eP[4] = cube.eP[11]
    cube.eP[11] = tmp
    
    # corner orientation
    cube.cO[cube.cP[0]] = modulo3(cube.cO[cube.cP[0]] + 1)
    cube.cO[cube.cP[2]] = modulo3(cube.cO[cube.cP[2]] + 1)
    cube.cO[cube.cP[5]] = modulo3(cube.cO[cube.cP[5]] - 1)
    cube.cO[cube.cP[7]] = modulo3(cube.cO[cube.cP[7]] - 1)

def spin_L(cube):
    """L move (left face clockwise)"""
    # corner permutation
    tmp = cube.cP[0]
    cube.cP[0] = cube.cP[5]
    cube.cP[5] = cube.cP[1]
    cube.cP[1] = cube.cP[4]
    cube.cP[4] = tmp
    
    # edge permutation
    tmp = cube.eP[4]
    cube.eP[4] = cube.eP[1]
    cube.eP[1] = cube.eP[5]
    cube.eP[5] = cube.eP[0]
    cube.eP[0] = tmp

def spin_R(cube):
    """R move (right face clockwise)"""
    # corner permutation
    tmp = cube.cP[3]
    cube.cP[3] = cube.cP[6]
    cube.cP[6] = cube.cP[2]
    cube.cP[2] = cube.cP[7]
    cube.cP[7] = tmp
    
    # edge permutation
    tmp = cube.eP[6]
    cube.eP[6] = cube.eP[2]
    cube.eP[2] = cube.eP[7]
    cube.eP[7] = cube.eP[3]
    cube.eP[3] = tmp

def move_2nul(move, move2):
    """Returns move before last if last move opposite face, else nul"""
    if move and move2:
        if ((move[0] == 'U' and move2[0] != 'D') or
            (move[0] == 'D' and move2[0] != 'U') or
            (move[0] == 'F' and move2[0] != 'B') or
            (move[0] == 'B' and move2[0] != 'F') or
            (move[0] == 'L' and move2[0] != 'R') or
            (move[0] == 'R' and move2[0] != 'L')):
            return ""
    return move2

def update_move(cube, move):
    """Records the last move, avoiding repetition with move2nul"""
    cube.move2 = cube.move
    cube.move = move
    cube.move2 = move_2nul(cube.move, cube.move2)

def spin(mix_string, cube):
    """Executes given sequence of spins on cube"""
    sequence = mix_string.split()
    for move in sequence:
        if move == "U":
            spin_U(cube)
            update_move(cube, "U")
        elif move == "U'":
            for _ in range(3):
                spin_U(cube)
            update_move(cube, "U'")
        elif move == "U2":
            for _ in range(2):
                spin_U(cube)
            update_move(cube, "U2")
        elif move == "D":
            spin_D(cube)
            update_move(cube, "D")
        elif move == "D'":
            for _ in range(3):
                spin_D(cube)
            update_move(cube, "D'")
        elif move == "D2":
            for _ in range(2):
                spin_D(cube)
            update_move(cube, "D2")
        elif move == "R":
            spin_R(cube)
            update_move(cube, "R")
        elif move == "R'":
            for _ in range(3):
                spin_R(cube)
            update_move(cube, "R'")
        elif move == "R2":
            for _ in range(2):
                spin_R(cube)
            update_move(cube, "R2")
        elif move == "L":
            spin_L(cube)
            update_move(cube, "L")
        elif move == "L'":
            for _ in range(3):
                spin_L(cube)
            update_move(cube, "L'")
        elif move == "L2":
            for _ in range(2):
                spin_L(cube)
            update_move(cube, "L2")
        elif move == "F":
            spin_F(cube)
            update_move(cube, "F")
        elif move == "F'":
            for _ in range(3):
                spin_F(cube)
            update_move(cube, "F'")
        elif move == "F2":
            for _ in range(2):
                spin_F(cube)
            update_move(cube, "F2")
        elif move == "B":
            spin_B(cube)
            update_move(cube, "B")
        elif move == "B'":
            for _ in range(3):
                spin_B(cube)
            update_move(cube, "B'")
        elif move == "B2":
            for _ in range(2):
                spin_B(cube)
            update_move(cube, "B2")
        else:
            # Import inside the function to avoid circular imports
            print("Wrong move: ", move)
            sys.exit(1)