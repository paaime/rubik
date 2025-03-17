import os
import math
from cube import Cube
from tables.tables import new_node
from utils import list_moves, create_file, read_file
from move import spin

def binary_to_decimal(binary):
    """Converts binary array to decimal"""
    decimal = 0
    for i in range(11):
        decimal += binary[i] * int(math.pow(2, 10-i))
    return decimal

def table_G0():
    """Generates the G0 pruning table"""
    print("\nG0 is generating...", end="")
    table = [0] * 2048
    parents = [Cube()]
    depth = 0
    
    while depth < 6:
        children = []
        depth += 1
        
        for parent in parents:
            for move in list_moves(parent, 0):
                child = new_node(parent, move)
                spin(move, child)
                index = binary_to_decimal(child.eO)
                if index != 0 and table[index] == 0:
                    table[index] = depth
                
                children.append(child)
        
        parents = children
    
    # Fill remaining entries with max depth
    for i in range(len(table)):
        if i > 0 and table[i] == 0:
            table[i] = 7
    
    return table

def make_table_G0(tables):
    """Creates or reads the G0 table from file"""
    if not os.path.exists("tables/G0.txt"):
        tables.G0 = table_G0()
        
        with create_file("tables/G0.txt") as file:
            for depth in tables.G0:
                file.write(f"{depth}")
    else:
        file_content = read_file("tables/G0.txt")
        for i, depth in enumerate(file_content):
            tables.G0[i] = depth - 48  # Convert ASCII to integer