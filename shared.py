MAPSIZE = 10
EXPLORED = ' '
UNEXPLORED = '-'
OCCUPIED = 'X'
HIT = 'H'
MISS = 'M'
ENEMY_FLEET = ['Carrier', 'Battleship', 'Submarine', 'Cruiser',
                'Destroyer']

SHIP_HEALTH = {
    'Carrier':      5,
    'Battleship':   4,
    'Submarine':    3,
    'Cruiser':      3,
    'Destroyer':    2
    }

class Map:

    m = None
    size = 0

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def generate_player_map(self, occupied):
        ''' Generate player map for human or agent.
            Take a list of ship arrangement as input
            and mark them as occupied.
        '''
        map_range = range(0, self.size)
        row = [EXPLORED for i in map_range]
        self.m = [row[:] for i in map_range]
        for (x,y) in occupied:
            self.m[x][y] = OCCUPIED

    def generate_ai_enemy_map(self):
        ''' Generate enemy map for agent.
        '''
        map_range = range(0, self.size)
        row = [0 for i in map_range]
        self.m = [row[:] for i in map_range]
        # Encourage Hunt-and-Target - make even
        # cells a slightly higher priority
        even = False
        for i in map_range:
            for j in map_range:
                if even:
                    self.m[i][j] = 1
                even = not even
            even = not even

    def generate_human_enemy_map(self):
        ''' Generate enemy map for human.
        '''
        map_range = range(0, self.size)
        row = [UNEXPLORED for i in map_range]
        self.m = [row[:] for i in map_range]

    def print_map(self):
        ''' Prints the map in readable form.
        '''
        for i in range(0, self.size):
            for j in range(0, self.size):
                print self.m[i][j],
            print ''

    def mark_adjacent_coords(self, (x,y), score):
        ''' Hunt-and-Target
            For agent enemy map: find unexplored adjacent coordinates
            and mark them with the given score.
        '''
        for (ax,ay) in self.find_adjacent_by_xy((x,y)):
            if self.m[ax][ay] > -2:
                self.m[ax][ay] = score

    def find_adjacent_by_xy(self, (x,y)):
        ''' Find adjacent neighbors of a given coordinate.
        '''
        nbs = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        return [nb for nb in nbs if self.in_range(nb)]

    def in_range(self, (x,y)):
        ''' Tell if a coordinate is in map range
        '''
        if (0 <= x < self.size) and (0 <= y < self.size):
            return True
        else:
            return False

    def get(self, (x,y)):
        ''' getter of (x,y) coordinate
        '''
        return self.m[x][y]

    def set(self, (x,y), val):
        ''' setter of (x,y) coordinate
        '''
        self.m[x][y] = val

    def apply_deltas(self, deltas):
        for d in deltas.keys():
            self.m[x][y] = self.m[x][y] + deltas[d]

class Ship:

    coords = []
    t = None
    horizontal = None
    head = None

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def length(self):
        return len(self.coords)

    def find_head(self):
        if not self.head:
            # find head first
            self.head = list(self.coords)[0]
            xory = 0 if self.horizontal else 1
            for c in self.coords:
                if c[xory] < self.head[xory]:
                    self.head = c
        return self.head


def grid_to_array(grid):
    array = []
    for i in range(0, MAPSIZE):
        for j in range(0, MAPSIZE):
            if grid[i][j] == '1':
                array.append((i,j))
    return array

def fleet_to_array(fleet):
    ''' Convert a list of ships into array.
    '''
    result = []
    [result.extend(s.coords) for s in fleet]
    return result