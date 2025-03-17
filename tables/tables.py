from cube import Cube

def read_hex(char):
    """Converts hex char to int value"""
    if char < 97:
        return char - 48
    return char - 87

class Tables:
    """Contains pruning tables and index converters for all 4 subgroups"""
    def __init__(self):
        self.G0 = [0] * 2048
        self.G1 = [[0] * 2187 for _ in range(495)]
        self.G1ePindex = [0] * 4096
        self.G2 = [[0] * 70 for _ in range(40320)]
        self.G2ePindex = [0] * 255
        self.G3 = [[[[0] * 24 for _ in range(24)] for _ in range(24)] for _ in range(96)]
        self.G3cPindex = [0] * 40320

def new_node(parent, move):
    """Creates a new node (cube) with the same state as parent"""
    new_cube = Cube()
    new_cube.cP = parent.cP.copy()
    new_cube.cO = parent.cO.copy()
    new_cube.eP = parent.eP.copy()
    new_cube.eO = parent.eO.copy()
    new_cube.move = move
    new_cube.move2 = parent.move2
    return new_cube

def make_tables():
    """Initializes tables and creates or reads tables from file"""
    from tables.tableG0 import make_table_G0
    from tables.tableG1 import make_table_G1
    from tables.tableG2 import make_table_G2
    from tables.tableG3 import make_table_G3
    
    tables = Tables()
    make_table_G0(tables)
    make_table_G1(tables)
    make_table_G2(tables)
    make_table_G3(tables)
    return tables