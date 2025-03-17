import random
import time
import os
import sys
from cube import Cube

def half_turn_metric(sequence):
    """Returns word count for given solution (Half Turn Metric)"""
    return len(sequence.split())

def string_in_slice(a, list_items):
    """Check if a string exists in a list"""
    for b in list_items:
        if b == a:
            return True
    return False

def random_mix(length):
    """Returns a random don't repeat yourself mix of given length (default 18-30)"""
    spin = [
        "U",
        "U'",
        "U2",
        "D",
        "D'",
        "D2",
        "R",
        "R'",
        "R2",
        "L",
        "L'",
        "L2",
        "F",
        "F'",
        "F2",
        "B",
        "B'",
        "B2"
    ]
    
    dry = spin.copy()
    mix = ""
    
    # Seed random number generator
    random.seed(time.time_ns())
    
    n = length
    if n == -1:
        n = random.randint(8, 10)  # randint is inclusive, so 18-29 gives range 18-30
        
    for i in range(n):
        move = dry[random.randint(0, len(dry) - 1)]
        mix += move
        
        if move in ["U", "U'", "U2"]:
            if string_in_slice("D", dry):
                dry = spin[3:]
            else:
                dry = spin[6:]
        elif move in ["D", "D'", "D2"]:
            if string_in_slice("U", dry):
                dry = spin[:3] + spin[6:]
            else:
                dry = spin[6:]
        elif move in ["R", "R'", "R2"]:
            dry = spin[:6]
            if string_in_slice("L", dry):
                dry = dry + spin[9:]
            else:
                dry = dry + spin[12:]
        elif move in ["L", "L'", "L2"]:
            if string_in_slice("R", dry):
                dry = spin[:9]
            else:
                dry = spin[:6]
            dry = dry + spin[12:]
        elif move in ["F", "F'", "F2"]:
            dry = spin[:12]
            if string_in_slice("B", dry):
                dry = dry + spin[15:]
        elif move in ["B", "B'", "B2"]:
            if string_in_slice("F", dry):
                dry = spin[:15]
            else:
                dry = spin[:12]
                
        if i != n - 1:  # In Python, last index is n-1
            mix += " "
            
    print(f"Random Mix generated : \n{mix}\n")
    return mix

def list_moves(cube, subgroup):
    """Returns all possible moves for given cube in subgroup"""
    moves = []
    
    if subgroup == 0:
        moves = [
            "U", "U'", "U2",
            "D", "D'", "D2",
            "R", "R'", "R2",
            "L", "L'", "L2",
            "F", "F'", "F2",
            "B", "B'", "B2"
        ]
    elif subgroup == 1:
        moves = [
            "U2", "D2",
            "R", "R'", "R2",
            "L", "L'", "L2",
            "F", "F'", "F2",
            "B", "B'", "B2"
        ]
    elif subgroup == 2:
        moves = [
            "U2", "D2",
            "R", "R'", "R2",
            "L", "L'", "L2",
            "F2", "B2"
        ]
    else:  # subgroup == 3
        moves = [
            "U2", "D2",
            "R2", "L2",
            "F2", "B2"
        ]
    
    # Filter moves based on last and second-to-last moves
    if cube.move != "":
        filtered_moves = []
        for move in moves:
            if move[0] != cube.move[0]:
                if cube.move2 != "":
                    if move[0] != cube.move2[0]:
                        filtered_moves.append(move)
                else:
                    filtered_moves.append(move)
        moves = filtered_moves
        
    return moves

def modulo3(n):
    """Return n modulo 3, handling special -1 case"""
    if n == -1:
        return 2
    else:
        return n % 3
    
def create_file(filepath):
    """Creates a file and returns file handle"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        return open(filepath, 'w')
    except:
        print("Error when creating file")
        sys.exit(1)
        return None

def read_file(filepath):
    """Reads file contents into a byte array"""
    try:
        with open(filepath, 'rb') as f:
            return f.read()
    except:
        print("Error when reading pruning table file")
        sys.exit(1)
        return None

def mix_is_valid(mix):
    """Returns True if mix only contains valid moves"""
    cube = Cube()
    all_moves = list_moves(cube, 0)
    mix_list = mix.split()
    for mix_move in mix_list:
        if mix_move not in all_moves:
            return False
    return True

def make_mix(mix, length):
    """Checks mix validity, creates random mix, or reads mix file"""
    if mix_is_valid(mix):
        return mix
        
    if mix == "-r" or mix == "--random":
        return random_mix(length)
    
    return ""