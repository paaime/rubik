import os
import math
from cube import Cube
from tables.tables import new_node
from utils import list_moves, create_file, read_file
from move import spin

def cO2index(corner_orientation):
    """Converts corner orientation to index"""
    index = 0
    for i in range(7):
        index = index * 3 + corner_orientation[i]
    return index

def eP2Binary(cube):
    """Converts edge permutation to binary array"""
    binary = [False] * 11
    for i in range(11):
        if cube.eP[i] > 7:
            binary[i] = True
    return binary

def binaryBool2Decimal(binary):
    """Converts binary boolean array to decimal"""
    decimal = 0
    for i in range(11):
        if binary[i]:
            decimal += int(math.pow(2, 10-i))
    return decimal

def eP2index(cube, tables):
    """Converts edge permutation to index"""
    ep_binary = eP2Binary(cube)
    idx_EP = binaryBool2Decimal(ep_binary)
    return tables.G1ePindex[idx_EP]

def table_G1_IdxConv(tables):
    """Creates index conversion table for G1"""
    converted = 0
    for idx in range(2048):
        count = bin(idx).count("1")  # Count set bits
        if count == 4 or count == 3:
            tables.G1ePindex[idx] = converted
            converted += 1

def read_hex(char):
    """Converts hex char to int value"""
    if isinstance(char, int):
        char = chr(char)
    if char.isdigit():
        return int(char, 16)
    else:
        return int(char, 16)

def table_G1(tables):
    """Generates the G1 pruning table"""
    print("\nG1 is generating", end="")
    parents = [Cube()]
    depth = 0
    
    while depth < 8:
        depth += 1
        children = []
        
        for parent in parents:
            for move in list_moves(parent, 1):
                child = new_node(parent, move)
                spin(move, child)
                
                idx_CO = cO2index(child.cO)
                idx_EP = eP2index(child, tables)
                
                if tables.G1[idx_EP][idx_CO] == 0 and not (idx_EP == 0 and idx_CO == 0):
                    tables.G1[idx_EP][idx_CO] = depth
                
                children.append(child)
        
        parents = children
    
    # Fill remaining entries with max depth
    for ep_idx in range(495):
        for co_idx in range(2187):
            if tables.G1[ep_idx][co_idx] == 0 and not (ep_idx == 0 and co_idx == 0):
                tables.G1[ep_idx][co_idx] = 9

def make_table_G1(tables):
    """Creates or reads the G1 table from file"""
    table_G1_IdxConv(tables)
    
    if not os.path.exists("tables/G1.txt"):
        table_G1(tables)
        
        with create_file("tables/G1.txt") as file:
            for ep_idx in range(495):
                for co_idx in range(2187):
                    file.write(f"{tables.G1[ep_idx][co_idx]:x}")
    else:
        file_content = read_file("tables/G1.txt")
        ep_idx = 0
        co_idx = 0
        
        for depth in file_content:
            tables.G1[ep_idx][co_idx] = read_hex(depth)
            co_idx += 1
            
            if co_idx >= 2187:
                co_idx = 0
                ep_idx += 1