import os
from cube import Cube
from tables.tables import new_node
from utils import list_moves, create_file, read_file
from tables.tableG2 import cP2index, corners_in_orbit, cP_in_list
from move import spin
from tables.tables import read_hex

def ePindex_slice(cube, slice_num):
    """Computes permutation index for a slice of edge pieces"""
    slice4 = slice_num * 4
    
    # Check all 24 possible permutations
    if cube.eP[0 + slice4] == 0 + slice4:
        if cube.eP[1 + slice4] == 1 + slice4:
            if cube.eP[2 + slice4] == 2 + slice4:
                return 0        # 0123
            else:
                return 1        # 0132
        elif cube.eP[1 + slice4] == 2 + slice4:
            if cube.eP[2 + slice4] == 1 + slice4:
                return 2        # 0213
            else:
                return 3        # 0231
        else:
            if cube.eP[2 + slice4] == 1 + slice4:
                return 4        # 0312
            else:
                return 5        # 0321
    elif cube.eP[0 + slice4] == 1 + slice4:
        if cube.eP[1 + slice4] == 0 + slice4:
            if cube.eP[2 + slice4] == 2 + slice4:
                return 6        # 1023
            else:
                return 7        # 1032
        elif cube.eP[1 + slice4] == 2 + slice4:
            if cube.eP[2 + slice4] == 0 + slice4:
                return 8        # 1203
            else:
                return 9        # 1230
        else:
            if cube.eP[2 + slice4] == 0 + slice4:
                return 10       # 1302
            else:
                return 11       # 1320
    elif cube.eP[0 + slice4] == 2 + slice4:
        if cube.eP[1 + slice4] == 0 + slice4:
            if cube.eP[2 + slice4] == 1 + slice4:
                return 12       # 2013
            else:
                return 13       # 2031
        elif cube.eP[1 + slice4] == 1 + slice4:
            if cube.eP[2 + slice4] == 0 + slice4:
                return 14       # 2103
            else:
                return 15       # 2130
        else:
            if cube.eP[2 + slice4] == 0 + slice4:
                return 16       # 2301
            else:
                return 17       # 2310
    else:  # cube.eP[0 + slice4] == 3 + slice4
        if cube.eP[1 + slice4] == 0 + slice4:
            if cube.eP[2 + slice4] == 1 + slice4:
                return 18       # 3012
            else:
                return 19       # 3021
        elif cube.eP[1 + slice4] == 1 + slice4:
            if cube.eP[2 + slice4] == 0 + slice4:
                return 20       # 3102
            else:
                return 21       # 3120
        else:
            if cube.eP[2 + slice4] == 0 + slice4:
                return 22       # 3201
            else:
                return 23       # 3210

def ePindex_converter(cube):
    """Converts edge permutation to multi-dimensional index"""
    slice_index = [0] * 3
    for slice_num in range(3):
        slice_index[slice_num] = ePindex_slice(cube, slice_num)
    return slice_index

def cP_table_index(tables):
    """Creates corner permutation index table"""
    initial = [Cube()]
    parents = [Cube()]
    converted = 1
    
    for depth in range(4):
        children = []
        
        for parent in parents:
            for move in list_moves(parent, 2):
                child = new_node(parent, move)
                spin(move, child)
                
                if corners_in_orbit(child) and not cP_in_list(child, initial):
                    initial.append(child)
                    tables.G3cPindex[cP2index(child)] = converted
                    converted += 1
                
                children.append(child)
        
        parents = children

def table_G3(tables):
    """Generates the G3 pruning table"""
    print("\nG3 is generating", end="")
    parents = [Cube()]
    depth = 0
    
    while depth < 15:
        depth += 1
        children = []
        
        for parent in parents:
            for move in list_moves(parent, 3):
                child = new_node(parent, move)
                spin(move, child)
                
                idx_CP = tables.G3cPindex[cP2index(child)]
                idx_EP = ePindex_converter(child)
                
                if tables.G3[idx_CP][idx_EP[0]][idx_EP[1]][idx_EP[2]] == 0:
                    tables.G3[idx_CP][idx_EP[0]][idx_EP[1]][idx_EP[2]] = depth
                    children.append(child)
        
        parents = children

def make_table_G3(tables):
    """Creates or reads the G3 table from file"""
    cP_table_index(tables)
    
    if not os.path.exists("tables/G3.txt"):
        table_G3(tables)
        
        with create_file("tables/G3.txt") as file:
            for cp_idx in range(96):
                for ep_idx0 in range(24):
                    for ep_idx1 in range(24):
                        for ep_idx2 in range(24):
                            file.write(f"{tables.G3[cp_idx][ep_idx0][ep_idx1][ep_idx2]:x}")
    else:
        file_content = read_file("tables/G3.txt")
        cp_idx = 0
        ep_idx0 = 0
        ep_idx1 = 0
        ep_idx2 = 0
        
        for depth in file_content:
            tables.G3[cp_idx][ep_idx0][ep_idx1][ep_idx2] = read_hex(depth)
            ep_idx2 += 1
            
            if ep_idx2 >= 24:
                ep_idx2 = 0
                ep_idx1 += 1
                
                if ep_idx1 >= 24:
                    ep_idx1 = 0
                    ep_idx0 += 1
                    
                    if ep_idx0 >= 24:
                        ep_idx0 = 0
                        cp_idx += 1