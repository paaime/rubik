import os
import math
from cube import Cube
from tables.tables import new_node
from utils import list_moves, create_file, read_file
from move import spin
from tables.tables import read_hex

def cP2index(cube):
    """Converts corner permutation to index"""
    n = 8
    index = 0
    for i in range(n):
        index = index * (n - i)
        for j in range(i + 1, n):
            if cube.cP[i] > cube.cP[j]:
                index += 1
    return index

def eP2Binary8(cube):
    """Converts edge permutation (first 8) to binary array"""
    binary = [False] * 8
    for i in range(8):
        if cube.eP[i] > 3:
            binary[i] = True
    return binary

def binaryBool2Decimal8(binary):
    """Converts binary boolean array to decimal"""
    decimal = 0
    for i in range(8):
        if binary[i]:
            decimal += int(math.pow(2, 7-i))
    return decimal

def eP2index8(cube, tables):
    """Converts edge permutation to index (for G2)"""
    ep_binary = eP2Binary8(cube)
    idx_EP = binaryBool2Decimal8(ep_binary)
    return tables.G2ePindex[idx_EP]

def table_G2_IdxConv(tables):
    """Creates index conversion table for G2"""
    converted = 0
    for idx in range(255):
        count = bin(idx).count("1")  # Count set bits
        if count == 4:
            tables.G2ePindex[idx] = converted
            converted += 1

def corners_in_orbit(cube):
    """Returns true if corners 0-3 are in position 0-3, and 4-7 in 4-7"""
    for i in range(4):
        if cube.cP[i] > 3:
            return False
    return True

def cP_in_list(cube, initial_list):
    """Returns true if given cube corner permutation is in list of initial cubes"""
    cube_idx = cP2index(cube)
    for permutation in initial_list:
        if cube_idx == cP2index(permutation):
            return True
    return False

def initial_96_cubes():
    """Returns the 96 cubes with corners in orbit"""
    initial = [Cube()]
    parents = [Cube()]
    
    for depth in range(4):
        children = []
        
        for parent in parents:
            for move in list_moves(parent, 2):
                child = new_node(parent, move)
                spin(move, child)
                
                if corners_in_orbit(child) and not cP_in_list(child, initial):
                    initial.append(child)
                
                children.append(child)
        
        parents = children
    
    return initial

def table_G2(tables):
    """Generates the G2 pruning table"""
    print("\nG2 is generating", end="")
    parents = initial_96_cubes()
    depth = 0
    
    while depth < 13:
        depth += 1
        children = []
        
        for parent in parents:
            for move in list_moves(parent, 2):
                child = new_node(parent, move)
                spin(move, child)
                
                idx_CP = cP2index(child)
                idx_EP = eP2index8(child, tables)
                
                if tables.G2[idx_CP][idx_EP] == 0 and not (idx_CP == 0 and idx_EP == 0):
                    tables.G2[idx_CP][idx_EP] = depth
                    children.append(child)
        
        parents = children

def make_table_G2(tables):
    """Creates or reads the G2 table from file"""
    table_G2_IdxConv(tables)
    
    if not os.path.exists("tables/G2.txt"):
        table_G2(tables)
        
        with create_file("tables/G2.txt") as file:
            for cp_idx in range(40320):
                for ep_idx in range(70):
                    file.write(f"{tables.G2[cp_idx][ep_idx]:x}")
    else:
        file_content = read_file("tables/G2.txt")
        cp_idx = 0
        ep_idx = 0
        
        for depth in file_content:
            tables.G2[cp_idx][ep_idx] = read_hex(depth)
            ep_idx += 1
            
            if ep_idx >= 70:
                ep_idx = 0
                cp_idx += 1