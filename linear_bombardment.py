
import copy
import random
from battleship_ai import player
from shared import *

up      =   1
down    =   -1
left    =   2
right   =   -2

class Agent(Player):

    nextmoves = []
    hit_before = []
    streak = []
    last_hit = False
    hunt_mode = True

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def attack(self, enemy, (x,y)):

        if self.nextmoves:
            x = self.nextmoves[0][0]
            y = self.nextmoves[0][1]

        r = enemy.hit((x,y))
        result, sunk_ship = r['result'], r['sunk_ship']
        if result == 'H':
            self.last_hit = True
            self.hitlist.append((x,y))
        else:
            self.last_hit = False

        # mark coordinate as visited
        self.enemy_map.set((x,y), -2)
        if self.nextmoves:
            del self.nextmoves[0]
        return r

    def find_target(self):
        if self.hunt_mode:
            return self.hunt()
        else:
            return None

    def hunt(self):
        ''' Choose the coordinates of the target in the map with highest
            weightage val
        '''
        size = self.enemy_map.size
        m = self.enemy_map.m
        highest = m[0][0]
        candidates = [(0,0)]

        for i in range(0, size):
          for j in range(0, size):
             if m[i][j] == highest:
                candidates.append((i,j))
             elif m[i][j] > highest:
                highest = m[i][j]
                candidates = [(i,j)]

        return random.choice(candidates)

    def furthestfrom(self, target, array, amount):
        # return the furthest [amount] cells from target in given array

        result = []
        # x coordinate is different
        if (array[i][0] != target[0]):
            array = self.sortby(array, True)

            if (target[0]<array[0][0]):
                # start from end
                for i in range (0, amount):
                    result.append(array[array.length-1])
                    del array[array.length-1]

            else:
                # start from 0
                for i in range (0, amount):
                    result.append(array[0])
                    del array[0]

        # y coordinate is different
        else:
            array = self.sortby(array, False)

            if (target[1]<array[0][1]):
                # start from end
                for i in range (0, amount):
                    result.append(array[array.length-1])
                    del array[array.length-1]

            else:
                # start from 0
                for i in range (0, amount):
                    result.append(array[0])
                    del array[0]

        return result

    def sortby(self, array, x):
        # sort array of (x,y) by x or y.
        return sorted(array) if x else sorted(array, key=lambda x: x[1])

    def within_range(self, x, y):
        return True if ((x>0) and (x<10) and (y>0) and (y<10)) else False

    def explore(self, x, y, direction):
        # hit all cells from x,y in the given direction until miss, edge
        # of the map, or ship sunk
        result = 0
        finalcoord = (0,0)

        if (self.within_range(x,y)):
            self.nextmoves.append((x,y))

        if self.nextmoves:
            if nextmoves[0] != (x,y):
                if not self.last_hit:
                    # The result is a miss
                    return (1, finalcoord)
            else: # The result is a hit
                finalcoord = (x,y)
                hits.append((x,y))
                if (direction = up):
                    return self.explore (x, y-1, direction)
                if (direction = down):
                    return self.explore (x, y+1, direction)
                if (direction = left):
                    return self.explore (x-1, y, direction)
                if (direction = right):
                    return self.explore (x+1, y, direction)
        else:
            return (0, finalcoord, hits)

        return (result, finalcoord, hits)

    def linbombardment (self, (x,y), orientation):
        lengthofsunkship = 0
        linbombardmentcounter = 1
        hitcells = []

        # Horizontal orientation
        if (orientation == 1):
            # First, explore left
            explorevars = self.explore (x-1, y, left)

            # 0 if hit a wall, 1 if missed, other values
            # correspond to the length of the sunk ship
            explorevar = explorevars[0]

            # Coordinates of a cell which sunk the ship
            explorevar2 = explorevars[1]

            # List of coordinates hit by explore
            explorehitlist = explorevars[2]
            
            if (explorevar > 1):
                # Get length of the ship

                lengthofsunkship = lengthofsunkship + explorevar
                if (lengthofsunkship < linbombardmentcounter):
                    orientation = orientation * (-1)
                    furthests = self.furthestfrom(explorevar2, hitcells, (linbombardmentcounter-lengthofsunkship))
                    for i in range (0,(linbombardmentcounter - lengthofsunkship)):
                        self.linbombardment(furthest[i], orientation)

                hitcells = explorehitlist
                linbombardmentcounter = linbombardmentcounter + hitcells.length

            else:
                explorevars = self.explore (x+1, y, right)
                explorevar = explorevars[0]
                explorevar2 = explorevars[1]
                explorehitlist = explorevars[2]

                if (explorevar > 1):
                    # Get length of the ship
                    lengthofsunkship = lengthofsunkship + explorevar
                    if (lengthofsunkship < linbombardmentcounter):
                        orientation = orientation * (-1)
                        furthests = self.furthestfrom(explorevar2, hitcells, (linbombardmentcounter-lengthofsunkship))
                        for i in range (0,(linbombardmentcounter - lengthofsunkship)):
                            self.linbombardment(furthest[i], orientation)

                    hitcells = explorehitlist
                    linbombardmentcounter = linbombardmentcounter + hitcells.length
                    
                    else:
                        orientation = orientation * (-1)
                        furthests = self.furthestfrom(explorevar2, hitcells, (linbombardmentcounter-lengthofsunkship))
                        for i in range (0,(linbombardmentcounter - lengthofsunkship)):
                            self.linbombardment(furthest[i], orientation)

                    hitcells = explorehitlist
                    linbombardmentcounter = linbombardmentcounter + hitcells.length

        # Vertical orientation

        if (orientation == -1):
            explorevars = self.explore (x, y-1, up)
            explorevar = explorevars[0]
            explorevar2 = explorevars[1]
            if (explorevar > 1):
                # Get length of the ship
                lengthofsunkship = lengthofsunkship + explorevar
                if (lengthofsunkship < linbombardmentcounter):
                    furthests = self.furthestfrom(explorevar2, hitcells, (linbombardmentcounter-lengthofsunkship))
                        for i in range (0,(linbombardmentcounter - lengthofsunkship)):
                            self.linbombardment(furthest[i], orientation)
                hitcells = explorehitlist
                linbombardmentcounter = linbombardmentcounter + hitcells.length

            else:
                explorevars = self.explore (x, y+1, down)
                explorevar = explorevars[0]
                explorevar2 = explorevars[1]

                if (explorevar > 1):
                    # Get length of the ship
                    lengthofsunkship = lengthofsunkship + explorevar
                    if (lengthofsunkship < linbombardmentcounter):
                        orientation = orientation * (-1)
                        furthests = self.furthestfrom(explorevar2, hitcells, (linbombardmentcounter-lengthofsunkship))
                        for i in range (0,(linbombardmentcounter - lengthofsunkship)):
                            self.linbombardment(furthest[i], orientation)
                    hitcells = explorehitlist
                    linbombardmentcounter = linbombardmentcounter + hitcells.length
                                           
                    else:
                        orientation = orientation * (-1)
                        furthests = self.furthestfrom(explorevar2, hitcells, (linbombardmentcounter-lengthofsunkship))
                        for i in range (0,(linbombardmentcounter - lengthofsunkship)):
                            self.linbombardment(furthest[i], orientation)
                    hitcells = explorehitlist
                    linbombardmentcounter = linbombardmentcounter + hitcells.length