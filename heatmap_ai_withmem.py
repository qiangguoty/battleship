# experimental AIs.

import copy
import random
from battleship_ai import Player
from shared import *

class Agent(Player):
    '''
    An AI using weightage to find the next attack target.

    Hunt mode:
    TODO Parity.
    weightage: based on ships left

    Target mode:
    Quit until sunk a ship.
    TODO Parity.
    Use remained ships passing through [hit] area. If passable, neighbor score + 1
    '''
    enemy_fleet = []
    hunt_mode = True
    target_cache = []
    hits = []
    history = {}

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def reset(self):
        # record history.
        self.store_history()
        if not self.history:
            self.history = {}
        for h in self.hits:
            if h not in self.history.keys():
                self.history[h] = 1
            else:
                self.history[h] = self.history[h] + 1

        # reset all vals.
        self.my_map = None
        self.enemy_map = None
        self.fleet = []

        self.enemy_fleet = []
        self.hunt_mode = True
        self.target_cache = []

        self.hits = []

    def store_history(self):
        pass

    def attack(self, enemy, coord):
        r = enemy.hit(coord)
        result, sunk_ship = r['result'], r['sunk_ship']
        self.enemy_map.set(coord, -2)

        if result == 'H':
            self.hits.append(coord)
            # hit
            if self.hunt_mode and sunk_ship:
                # hunt mode, sunk ship
                # best luck - continue hunt mode
                pass

            elif self.hunt_mode:
                # hunt mode, hit ship
                # enter target mode
                self.add_target_cache(coord)
                self.to_target_mode()

            elif sunk_ship:
                # target mode, sunk ship
                # enter hunt mode
                self.remove_ship(sunk_ship)
                self.clear_target_cache()
                self.to_hunt_mode()
            else:
                # target mode, no sunk ship
                # continue
                self.add_target_cache(coord)

        else:
            # miss
            pass

        return r


    def find_target(self):
        if self.hunt_mode:
            return self.hunt()
        else:
            return self.target()

    def remove_ship(self, sunk_ship):
        self.enemy_fleet.remove(sunk_ship)

    def add_target_cache(self, coord):
        self.target_cache.append(coord)

    def clear_target_cache(self):
        self.target_cache = []

    def to_hunt_mode(self):
        self.hunt_mode = True

    def to_target_mode(self):
        self.hunt_mode = False

    def getmax(self):
        ''' Find the coord with maximum value on enemy map.
        '''
        maximum = -1000
        candidates = [(0,0)]
        for i in range(0, MAPSIZE):
            for j in range(0, MAPSIZE):
                if self.enemy_map.m[i][j] > maximum:
                    maximum = self.enemy_map.m[i][j]
                    candidates = [(i,j)]
                elif self.enemy_map.m[i][j] == maximum:
                    candidates.append((i,j))
        return random.choice(candidates)

    def hunt(self):
        self.reset_enemy_map()
        self.apply_history()

        for shipname in self.enemy_fleet:
            shiplen = SHIP_HEALTH[shipname]
            self.hunt_scan(shiplen)

        # print 'heatmap - hunt mode'
        # self.enemy_map.print_map()
        return self.getmax()

    def reset_enemy_map(self):
        # reset all unvisited squares to 0
        for x in range(0, MAPSIZE):
            for y in range(0, MAPSIZE):
                if self.enemy_map.m[x][y] > -2:
                    self.enemy_map.m[x][y] = 0


    def apply_history(self):
        for k, v in self.history.items():
            x, y = k
            if self.enemy_map.m[x][y] == 0: # unvisited
                self.enemy_map.m[x][y] = self.enemy_map.m[x][y] + v

    def hunt_scan(self, shiplen):
        # scan map using remained ships and mark score.

        # vertical
        for x in range(0, MAPSIZE):
            for y in range(0, MAPSIZE - shiplen):
                # get a list of candidates [shiplen]
                candidates = [(x,j) for j in range(y, y + shiplen)]
                # if all > -2, add 1.
                unvisited = [(cx,cy) for (cx,cy) in candidates if self.enemy_map.m[cx][cy] > -2]
                if len(candidates) == len(unvisited):
                    # passed test, add 1.
                    for (cx,cy) in candidates:
                        self.enemy_map.m[cx][cy] = self.enemy_map.m[cx][cy] + 1

        # horizontal
        for y in range(0, MAPSIZE):
            for x in range(0, MAPSIZE - shiplen):
                candidates = [(i,y) for i in range(x, x + shiplen)]
                # if all > -2, add 1.
                unvisited = [(cx,cy) for (cx,cy) in candidates if self.enemy_map.m[cx][cy] > -2]
                if len(candidates) == len(unvisited):
                    # passed test, add 1.
                    for (cx,cy) in candidates:
                        self.enemy_map.m[cx][cy] = self.enemy_map.m[cx][cy] + 1

    def target(self):
        self.reset_enemy_map()

        for shipname in self.enemy_fleet:
            shiplen = SHIP_HEALTH[shipname]
            self.target_scan(shiplen)

        # print 'heatmap - target mode'
        # self.enemy_map.print_map()
        return self.getmax()

    def target_scan(self, shiplen):
        # scan cache area using shiplen
        for tc in self.target_cache:
            for c in self.get_target_candidates(tc, shiplen):
                # validate: contains only unvisited squares + cache squares
                if self.is_valid_target_candidate(c):
                    # passed test. add 1.
                    for (cx,cy) in c:
                        if (cx,cy) not in self.target_cache:
                            self.enemy_map.m[cx][cy] = self.enemy_map.m[cx][cy] + 1


    def get_target_candidates(self, (x,y), shiplen):
        # get a list of candidates passing through coord in MAPSIZE range.
        result = []

        ## vertical

        # build 1st candidate
        cx, cy = x, y
        candidate_v = []
        for i in range(shiplen):
            candidate_v.append((cx, cy))
            cy = cy + 1

        # verify range
        if self.in_range(candidate_v):
            result.append(candidate_v)

        # build the rest candidates
        mover = copy.deepcopy(candidate_v)
        for i in range(shiplen - 1):
            new_candidate_v = self.move_back(mover, False)
            if self.in_range(new_candidate_v):
                result.append(new_candidate_v)
                # move on
            mover = copy.deepcopy(new_candidate_v)

        ## horizontal

        # build 1st candidate
        cx, cy = x, y
        candidate_h = []
        for i in range(shiplen):
            candidate_h.append((cx, cy))
            cx = cx + 1

        # verify range
        if self.in_range(candidate_h):
            result.append(candidate_h)

        # build the rest candidates
        mover = copy.deepcopy(candidate_h)
        for i in range(shiplen - 1):
            new_candidate_h = self.move_back(mover, True)
            if self.in_range(new_candidate_h):
                result.append(new_candidate_h)
                # move on
            mover = copy.deepcopy(new_candidate_h)

        return result

    def in_range(self, coords):
        # ensure the coords list are in map range.
        for (x,y) in coords:
            if (x < 0) or (x >= MAPSIZE) or (y < 0) or (y >= MAPSIZE):
                return False
        return True

    def move_back(self, coords, h):
        # reduce the x or y coord of given coords by 1
        if h:
            # horizontal - reduce x
            return [(x-1, y) for (x,y) in coords]
        else:
            # vertical - reduce y
            return [(x, y-1) for (x,y) in coords]


    def is_valid_target_candidate(self, candidate):
        # contains only unvisited squares + cached squares
        # exclude those who have visited squares and not cached
        for (x,y) in candidate:
            if self.enemy_map.m[x][y] <= -2:
                if (x,y) not in self.target_cache:
                    # fail
                    return False
        return True
        

        