from move import spin
from trim import trim
from utils import list_moves
from tables.tableG0 import binary_to_decimal
from tables.tableG1 import eP2index, cO2index
from tables.tableG2 import cP2index, eP2index8
from tables.tableG3 import ePindex_converter

# ANSI color codes for formatting output
RESET = "\033[0m"
BRIGHT = "\033[1m"

class RubikSolver:
    """A class to solve a Rubik's Cube using IDA* and pattern databases"""
    
    def __init__(self, tables):
        """Initialize the solver with precomputed tables"""
        self.tables = tables
    
    def in_path(self, node, path):
        """Returns true if given cube is already in the search path"""
        for cube in path:
            different = False
            
            # Check corner permutation
            for i in range(len(node.cP)):
                if node.cP[i] != cube.cP[i]:
                    different = True
                    break
            if different:
                continue
            
            # Check corner orientation
            for i in range(len(node.cO)):
                if node.cO[i] != cube.cO[i]:
                    different = True
                    break
            if different:
                continue
            
            # Check edge permutation
            for i in range(len(node.eP)):
                if node.eP[i] != cube.eP[i]:
                    different = True
                    break
            if different:
                continue
            
            # Check edge orientation
            for i in range(len(node.eO)):
                if node.eO[i] != cube.eO[i]:
                    different = True
                    break
            if different:
                continue
                
            # If we get here, all elements match
            return True
        
        return False

    def heuristic(self, cube, subgroup):
        """Returns pruning table depth for given cube and subgroup"""
        if subgroup == 0:
            return self.tables.G0[binary_to_decimal(cube.eO)]
        elif subgroup == 1:
            return self.tables.G1[eP2index(cube, self.tables)][cO2index(cube.cO)]
        elif subgroup == 2:
            return self.tables.G2[cP2index(cube)][eP2index8(cube, self.tables)]
        else:  # subgroup = 3
            idx_CP = self.tables.G3cPindex[cP2index(cube)]
            idx_EP = ePindex_converter(cube)
            return self.tables.G3[idx_CP][idx_EP[0]][idx_EP[1]][idx_EP[2]]

    def new_node(self, node, move):
        """Creates a new node with given move"""
        new_cube = node.copy()
        new_cube.move = move
        return new_cube

    def search(self, path, g, bound, subgroup, depth):
        """Recursively follows the pruning table heuristic until solved"""
        node = path[-1]
        f = g + self.heuristic(node, subgroup)
        
        if f > bound:
            return f, ""
        
        if self.heuristic(node, subgroup) == 0:
            solved_part = ""
            for i in range(1, len(path)):
                solved_part += path[i].move + " "
            return 255, solved_part
        
        moves = list_moves(node, subgroup)
        min_cost = 255  # infinity
        
        for move in moves:
            new = self.new_node(node, move)
            spin(move, new)
            
            if not self.in_path(new, path):
                path.append(new)
                cost, solution = self.search(path, g + self.heuristic(new, subgroup), 
                                       bound, subgroup, depth + 1)
                
                if cost == 255:
                    return 255, solution
                    
                if cost < min_cost:
                    min_cost = cost
                    
                path.pop()  # Remove the last element
        
        return min_cost, ""

    def ida_star(self, cube, subgroup):
        """Searches for a solution to the subgroup using IDA*"""
        bound = self.heuristic(cube, subgroup)
        path = [cube.copy()]
        
        while True:
            cost, solution = self.search(path, 0, bound, subgroup, 0)
            if cost == 255:
                return solution
            bound = cost

    def solve(self, cube, show_progress=True):
        """Calls IDA* search for each subgroup"""
        solution = ""
        subgroup = cube.get_subgroup()
        
        while subgroup < 4:
            cube.move = ""
            cube.move2 = ""
            
            solution_part = self.ida_star(cube, subgroup)
            spin(solution_part, cube)
            solution += solution_part
            
            subgroup += 1
        
        solution = trim(solution)
        return solution