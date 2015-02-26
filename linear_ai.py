
import copy
import random
from shared import *
from battleship_ai import Player


def init_agent(mapsize, arrangement, fleet):
    ''' Init agent.
    '''
    my_map = Map(size=mapsize)
    my_map.generate_player_map(arrangement)
    enemy_map = Map(size=mapsize)
    enemy_map.generate_ai_enemy_map()
    return Agent(my_map=my_map, enemy_map=enemy_map, fleet=copy.deepcopy(fleet),
        enemy_fleet=copy.deepcopy(ENEMY_FLEET))

class Agent(Player):

    visited = []
    linear_hit = []
    hunt_mode = True
    enemy_fleet = []
    candidates = []
    base = None
    current = None
    orientation = None  # -1 vertical 1 horizontal
    direction = None    # -1 up/left 1 right/down

    d_switched = False

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

        self.to_hunt_mode()

    def find_target(self):
        if self.hunt_mode:
            print 'hunt mode'
            return self.hunt()
        else:
            print '[lin]'
            print '[lin][candidates]', self.candidates
            print '[lin][base]', self.base
            print '[lin][orientation]', self.orientation
            print '[lin][direction]', self.direction
            print '[lin][linear_hit]', self.linear_hit
            return self.linear()

    def attack(self, enemy, (x,y)):
        ''' Attack an enemy coordinate.
        '''
        r = enemy.hit((x,y))

        self.current = (x,y)
        self.visited.append((x,y))

        result, sunk_ship = r['result'], r['sunk_ship']
        if result == HIT:

            print 'ai hit', (x,y)
            self.linear_hit.append((x,y))

            if self.hunt_mode and sunk_ship:
                # 1 in 1000 years opportunity!
                # do nothing
                pass

            elif self.hunt_mode:
                # hunt mode & hit:
                # enter linear mode
                self.candidates = [((x,y), random.choice([-1,1]))]
                self.to_linear_mode()

            elif sunk_ship:
                # linear mode & sunk ship:
                # determine the delta between sunk ship length / streak length.
                # if equals, return to hunt mode.
                # else, add the streak[:delta] as candidates
                # clear streak, and do linear mode on them with another orientation.

                print 'ai sunk a', sunk_ship
                self.enemy_fleet.remove(sunk_ship)
                
                delta = self.get_delta(SHIP_HEALTH[sunk_ship])
                print 'delta:', delta
                if delta:
                    new_candidates = [(d, -self.orientation) for d in delta]
                    self.candidates.extend(new_candidates)
                    self.linear_hit = []
                    self.to_linear_mode()
                else:
                    if len(self.linear_hit) != SHIP_HEALTH[sunk_ship] and self.candidates:
                        # continue linear mode
                        self.linear_hit = []
                        self.to_linear_mode()
                    else:
                        # return to hunt mode
                        self.to_hunt_mode()

            elif self.reached_edge((x,y)):
                # linear mode + no sunk ship + reached edge
                # if hasn't switched direction yet: switch direction.
                # else, add streak to candidates, clear streak, and do linear mode
                if not self.d_switched:
                    self.switch_direction()
                else:
                    new_candidates = [(d, -self.orientation) for d in self.linear_hit]
                    self.candidates.extend(new_candidates)
                    self.linear_hit = []
                    self.to_linear_mode()

            else:
                # linear mode, no sunk ship, no reach edge
                # continue
                pass

        else:

            print 'ai miss', (x,y)
            if not self.hunt_mode:
                # two scenarios:
                # 1. not switched direction yet - switch direction.
                # 2. switched direction - do linear mode on streaks.
                if not self.d_switched:
                    self.switch_direction()
                else:
                    new_candidates = [(d, -self.orientation) for d in self.linear_hit]
                    self.candidates.extend(new_candidates)
                    self.linear_hit = []
                    self.to_linear_mode()

        # mark coordinate as visited
        self.enemy_map.set((x,y), -2)
        return r

    def to_hunt_mode(self):
        self.linear_hit = []
        self.hunt_mode = True
        self.candidates = []
        self.orientation = None
        self.direction = None
        self.d_switched = False
        self.base = None
        self.current = None

    def to_linear_mode(self):
        # pick the first from self.candidates, 
        # init a new environment for linear mode.
        if self.candidates:
            candidate = self.candidates[0]
            del self.candidates[0]

            self.base = candidate[0]
            self.orientation = candidate[1]
            self.direction = random.choice([-1,1])

            self.hunt_mode = False
            self.d_switched = False
        else:
            print '[to_linear_mode][no_candidates]'
            self.to_hunt_mode()

    def switch_direction(self):
        print '[switch_direction]'
        self.direction = -self.direction
        self.d_switched = True

    def get_delta(self, shiplen):
        streaklen = len(self.linear_hit)
        print '[get_delta][streaklen]', streaklen
        print '[get_delta][shiplen]', shiplen
        if shiplen >= streaklen:
            return None
        else:
            delta = self.linear_hit[:(streaklen - shiplen)]
            return delta

    def hunt(self):
        return self.choose_highest()

    def linear(self):
        # get next one in current orientation + direction which is next to base.
        # (1) if next one is None, change direction.
        # (2) if (1) + direction has been changed, pursue next candidate.
        if not self.hunt_mode:
            next = self.get_next()
            if not next:
                if not self.d_switched:
                    self.switch_direction()
                    return self.linear()
                else:
                    print '[linear][get_next() returned None]'
                    self.to_linear_mode()
                    return self.linear()
            print '[linear][next]', next
            return next
        else:
            print '[hunt]'
            return self.hunt()

    def get_next(self):
        # get the closest unvisited cell near self.current based on orientation/direction.
        o = self.orientation
        d = self.direction

        if o == -1 and d == -1:
            # vertical, up
            return self.seeker(0, -1)
        elif o == -1 and d == 1:
            # vertical, down
            return self.seeker(0, 1)
        elif o == 1 and d == -1:
            # horizontal, left
            return self.seeker(-1, 0)
        elif o == 1 and d == 1:
            # horizontal, right
            return self.seeker(1, 0)
        print '[get_next][invalid o/d]'
        return None

    def seeker(self, dx, dy):
        cx, cy = self.base
        while True:
            cx = cx + dx
            cy = cy + dy
            if self.exceeded_edge((cx, cy)):
                print '[seeker][exceeded edge]', (cx,cy)
                break
            elif (cx,cy) in self.linear_hit:
                continue
            # elif (cx,cy) in self.visited:
            #     # visited and not in this linear_hit
            #     print '[seeker][visited and not in linear_hit]', (cx,cy)
            #     break
            else:
                print '[seeker] return', (cx,cy)
                return (cx,cy)
        return None


    def reached_edge(self, (x,y)):
        ''' Tell if the current direction reaches the map edge.
        '''
        o = self.orientation
        d = self.direction

        if o == -1 and d == -1 and y <= 0:
            # vertical, up, y <= 0
            return True
        elif o == -1 and d == 1 and y >= MAPSIZE - 1:
            # vertical, down, y >= 9
            return True
        elif o == 1 and d == -1 and x <= 0:
            # horizontal, left, x == 0
            return True
        elif o == 1 and d == 1 and x >= MAPSIZE - 1:
            # horizontal, right, x >= 9
            return True
        return False

    def exceeded_edge(self, (x,y)):
        if (0 <= x < MAPSIZE) and (0 <= y < MAPSIZE):
            return False
        return True

    def choose_highest(self):
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


    def reset(self):
        ''' Store player's game habits, then reset all in-game values.
        '''
        pass