'''
CS 5100 Proj:   Battleship
Team:           BigLeg
Last Modified:  04/10/2014
TODO:           1. Find bitmap for ships (check)
                2. Hit/Miss animation
                3. Prevent player from clicking visited cells

'''

import copy
import random
import sys
import time
import pygame
import pygame.gfxdraw
from pygame.locals import *

from PAdLib import draw as pagl_draw
from pygbutton_src import pygbutton
from randomgen import assignailoc
# from battleship_ai import *
from linear_ai import *
from battleship_ai import init_human
from shared import *

## game parameters

FPS = 30
WINDOWWIDTH = 945
WINDOWHEIGHT = 600
CELLSIZE = 40
BOARDSIZE = 10  # 10x10 board for each side
MARGIN = 5
HUMAN_EDGE = 450
AI_EDGE = 495
SCOREBOARD_EDGE = 470
BOARD_LOWEREDGE = 450

SHIP_IMGS = {
    'Carrier':      './img/carrier_220x40.png',
    'Battleship':   './img/battleship_175x40.png',
    'Submarine':    './img/submarine_130x40.png',
    'Cruiser':      './img/cruiser_130x40.png',
    'Destroyer':    './img/destroyer_85x40.png'
}

SHIP_LIST = [
    ('Carrier',      5),
    ('Battleship',   4),
    ('Submarine',    3),
    ('Cruiser',      3),
    ('Destroyer',    2)
]

SHIP_LIST_BACKUP = [
    ('Carrier',      5),
    ('Battleship',   4),
    ('Submarine',    3),
    ('Cruiser',      3),
    ('Destroyer',    2)
]

BULLET_HOLE_PATH = './img/bullet_hole_40x40.gif'
BGIMAGE_PATH = './img/water_945x600.jpg'

##           define colors
#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = ( 0,   0,   0)
GRAY      = (128, 128,  128)
BLUE      = ( 0,   0,  255)
DARKGREEN = ( 0,  155,  0)
GREEN     = ( 0,  255,  0)
DARKGRAY  = ( 40,  40, 40)
LIGHTBLUE = (135, 206, 250)
NAVY      = ( 0,   0,  128)
YALEBLUE  = ( 9,   70, 145)
BABYBLUE  = (139, 205, 241)
TUFTSBLUE = (67,  130, 205)

BGI = pygame.image.load(BGIMAGE_PATH)
HIT_SOUND_PATH = './sound/hit.wav'
MISS_SOUND_PATH = './sound/miss.wav'
ARR_SOUND_PATH = './sound/arr.wav'

################################################################################

class Board:
    fleet = []
    grid = []   # 20x10 grid

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def add_ship(self, ship):
        ''' Add a new ship to fleet and map grid.
        '''
        self.fleet.append(ship)
        for (x,y) in ship.coords:
            self.grid[x][y] = '1'

    def remove_ship(self, ship):
        ''' Remove a ship from fleet and map grid.
        '''
        self.fleet.remove(ship)
        for (x,y) in ship.coords:
            self.grid[x][y] = '0'

    def draw(self, surface):
        ''' Draw the current ship layout info onto surface.
        '''
        surface.blit(BGI, (0,0))
        grid = self.grid
        # draw grid
        self.draw_grid(surface)
        # draw ships
        for ship in self.fleet:
            self.draw_ship(surface, ship)
        # draw cells
        self.draw_cells(surface)

    def draw_grid(self, surface):
        grid = self.grid
        delta = 0

        for x in range(2 * BOARDSIZE):
            delta = CELLSIZE if BOARDSIZE <= x < 2 * BOARDSIZE else 0
            for y in range(BOARDSIZE):
                rect = [(MARGIN + CELLSIZE) * x + MARGIN + delta,
                        (MARGIN + CELLSIZE) * y + MARGIN,
                        CELLSIZE,
                        CELLSIZE]
                pagl_draw.rrect(surface, WHITE, rect, 5, 2)

    def draw_cells(self, surface):
        grid = self.grid
        delta = 0

        # draw left side
        for x in range(2 * BOARDSIZE):
            delta = CELLSIZE if BOARDSIZE <= x < 2 * BOARDSIZE else 0
            for y in range(BOARDSIZE):
                color = WHITE
                filled = False
                g = grid[x][y]

                rect = [(MARGIN + CELLSIZE) * x + MARGIN + delta,
                        (MARGIN + CELLSIZE) * y + MARGIN,
                        CELLSIZE,
                        CELLSIZE]

                if g == 'C':    # candidate
                    color = GREEN
                    filled = True
                # elif g == '1':  # selected
                #     color = GRAY
                #     filled = True
                elif g == 'M':  # miss
                    self.draw_miss(surface, (x,y), rect, delta)
                elif g == 'H':  # hit
                    self.draw_hit(surface, (x,y), delta)

                if filled:
                    pagl_draw.rrect(surface, color, rect, 5)


    def draw_hit(self, surface, (x,y), delta):
        x = (MARGIN + CELLSIZE) * x + MARGIN + CELLSIZE / 2 + delta
        y = (MARGIN + CELLSIZE) * y + MARGIN + CELLSIZE / 2
        # self.draw_occupied(surface, (x,y))
        # pygame.draw.circle(surface, BLACK, (x, y), 10)
        self.draw_bullet_hole(surface, (x,y))

    def draw_bullet_hole(self, surface, (x,y)):
        img = pygame.image.load(BULLET_HOLE_PATH)
        rect = img.get_rect()
        rect.center = (x,y)
        surface.blit(img, rect)

    def draw_miss(self, surface, (x,y), rect, delta):                
        # pagl_draw.rrect(surface, TUFTSBLUE, rect, 5)
        pagl_draw.rrect(surface, WHITE, rect, 5, 2)
        cx = (MARGIN + CELLSIZE) * x + MARGIN + CELLSIZE / 2 + delta
        cy = (MARGIN + CELLSIZE) * y + MARGIN + CELLSIZE / 2

        pygame.draw.circle(surface, WHITE, (cx,cy), 19, 2)
        pygame.draw.circle(surface, WHITE, (cx,cy), 12, 2)
        pygame.draw.circle(surface, WHITE, (cx,cy), 5, 2)

    def draw_occupied(self, surface, (x,y)):
        rect = [x-CELLSIZE/2, y-CELLSIZE/2, CELLSIZE, CELLSIZE]
        pagl_draw.rrect(surface, GRAY, rect, 5)
        pagl_draw.rrect(surface, WHITE, rect, 5, 2)

    def draw_ship(self, surface, ship):
        # find the start coordinate
        head = ship.find_head()
        x, y = coord_to_pos(head)
        x = x - CELLSIZE / 2
        y = y - CELLSIZE / 2
        img = pygame.image.load(SHIP_IMGS[ship.t])
        if not ship.horizontal:
            # rotate
            img = pygame.transform.rotate(img, 90)
        rect = img.get_rect()
        rect.topleft = (x,y)
        surface.blit(img, rect)

    def clear_candidates(self):
        ''' Reset candidates to empy cells.
        '''
        for x in range(BOARDSIZE):
            for y in range(BOARDSIZE):
                if self.grid[x][y] == 'C':
                    self.grid[x][y] = '0'

    def add_candidate(self, surface, (x,y), horizontal, shipname):
        ''' Add a candidate ship to map.
        '''
        coords = set([])
        occupied = False
        shiplen = [s[1] for s in SHIP_LIST if s[0] == shipname][0]
        coords.add((x,y))

        if horizontal:
            if x <= BOARDSIZE - shiplen:
                # has enough space to place horizontally
                [coords.add((i,y)) for i in range(x, x + shiplen)]
            else:
                # not enough horizontal space. align to right edge
                [coords.add((i,y)) for i in range(BOARDSIZE - shiplen, BOARDSIZE)]
        else:
            if y <= BOARDSIZE - shiplen:
                # has enough space to place vertically
                [coords.add((x,j)) for j in range(y, y + shiplen)]
            else:
                # not enough vertical space
                [coords.add((x,j)) for j in range(BOARDSIZE - shiplen, BOARDSIZE)]

        for (cx,cy) in coords:
            if self.grid[cx][cy] != '0':
                # occupied
                occupied = True

        if not occupied:
            # mark cells as candidates
            for (cx,cy) in coords:
                self.grid[cx][cy] = 'C'

        # draw_grid()
        # pygame.display.update()
        # FPSCLOCK.tick(FPS)

    def place_ship(self, (x,y), horizontal, shipname):
        ''' Add a ship to map.
        '''
        # look for candidates.
        coords = set([])
        for x in range(BOARDSIZE):
            for y in range(BOARDSIZE):
                if self.grid[x][y] == 'C':
                    self.grid[x][y] = '1'
                    coords.add((x,y))
        if coords:
            ship = Ship(coords=coords, t=shipname, horizontal=horizontal)
            self.fleet.append(ship)
            print 'ship added', ship.__dict__
            return True
        else:
            print 'add ship failed'
            return False

################################################################################

class Scoreboard:

    font = None


    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def reset(self, surface):
        # erase all previous messages
        rect = pygame.Rect(MARGIN, SCOREBOARD_EDGE, WINDOWWIDTH - 2 * MARGIN, 120)
        surface.fill(YALEBLUE, rect)
        pagl_draw.rrect(surface, WHITE, rect, 10, 2)

    def draw_arrangement_info(self, surface):
        base = SCOREBOARD_EDGE + 10
        draw_msg(surface, self.font, 'Please arrange your fleet', (2*MARGIN, base))
        draw_msg(surface, self.font, 'SPACE change direction', (2*MARGIN, base))
        for ship in SHIP_LIST:
            base = base + 16
            draw_msg(surface, self.font, ship[0], (2*MARGIN, base))

################################################################################

class Game:

    board = None
    scoreboard = None

    agent = None
    human = None

    surface = None
    font = None
    info = ''
    counter = 0

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def run(self):
        # main execution code.
        self.init()
        # self.welcome()
        self.arrange()
        self.game()

    def init(self):
        global FPSCLOCK
        # init pygame values/components.
        pygame.init()
        pygame.mixer.init()
        FPSCLOCK = pygame.time.Clock()
        self.surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        self.font = pygame.font.Font('freesansbold.ttf', 14)
        self.board = Board(grid=init_grid(), fleet=[])
        print self.board.fleet
        self.scoreboard = Scoreboard(font=self.font)
        pygame.display.set_caption('Battleship')

    def startmusic(self):
        pygame.mixer.music.load('bgm.mp3') # load the background music
        pygame.mixer.music.play(-1, 0.0)

    def stopmusic(self):
        pygame.mixer.music.stop

    def welcome(self):
        ''' Show animated welcome screen.
        '''
        titleFont = pygame.font.Font('freesansbold.ttf', 100)
        titleSurf1 = titleFont.render('Battleship!', True, WHITE, DARKGREEN)
        titleSurf2 = titleFont.render('Battleship!', True, GREEN)

        degrees1 = 0
        degrees2 = 0
        while True:
            SURFACE.fill(DARKGREEN)
            rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
            rotatedRect1 = rotatedSurf1.get_rect()
            rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
            SURFACE.blit(rotatedSurf1, rotatedRect1)

            rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
            rotatedRect2 = rotatedSurf2.get_rect()
            rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
            SURFACE.blit(rotatedSurf2, rotatedRect2)

            drawPressKeyMsg()

            if checkForKeyPress():
                pygame.event.get() 
                return
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            degrees1 += 0.5
            degrees2 += 1.5

    def drawPressKeyMsg(self):
        pressKeySurf = BASICFONT.render('Press any key to play.', True, DARKGRAY)
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
        SURFACE.blit(pressKeySurf, pressKeyRect)

    def checkForKeyPress(self):
        if len(pygame.event.get(QUIT)) > 0:
            terminate()

        keyUpEvents = pygame.event.get(KEYUP)
        if len(keyUpEvents) == 0:
            return None
        if keyUpEvents[0].key == K_ESCAPE:
            terminate()
        return keyUpEvents[0].key

    def arrange(self):
        ''' Let player arrange ships on board before game begins.
        '''
        self.board.draw(self.surface)
        horizontal = True
        pos = None

        while SHIP_LIST:
            shipname = SHIP_LIST[0][0]
            for event in pygame.event.get():
                if termination_detected(event):
                    terminate()

                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        # turn direction
                        horizontal = not horizontal
                        self.board.clear_candidates()
                        if in_player_map(pos):
                            self.board.add_candidate(self.surface, 
                                                    pos_to_coord(pos), 
                                                    horizontal, 
                                                    shipname)

                elif event.type == MOUSEMOTION:
                    self.board.clear_candidates()
                    pos = event.pos
                    if in_player_map(pos):
                        self.board.add_candidate(self.surface, 
                                                pos_to_coord(pos), 
                                                horizontal, 
                                                shipname)

                elif event.type == MOUSEBUTTONDOWN:
                    pos = event.pos
                    if in_player_map(pos):
                        if self.board.place_ship(pos_to_coord(pos), horizontal, shipname):
                            del SHIP_LIST[0]
                            play_arrangement_sound()

            self.surface.fill(YALEBLUE)
            self.board.draw(self.surface)
            self.scoreboard.reset(self.surface)
            self.scoreboard.draw_arrangement_info(self.surface)
            pygame.display.update()


    def game(self):
        human_turn = True
        alloc = assignailoc()
        self.human = init_human(BOARDSIZE, grid_to_array(self.board.grid), self.board.fleet)
        self.agent = init_agent(BOARDSIZE, fleet_to_array(alloc), alloc)
        x = 0
        y = 0
        finished = False

        while True:
            # determine if anyone won
            if self.human.lose():
                self.info = 'AI won'
                finished = True
            if self.agent.lose():
                self.info = 'You won'
                finished = True

            self.draw_info(self.human.getstringifiedfleet(), self.agent.getstringifiedfleet(), human_turn)
            pygame.display.update()

            if finished:
                break

            if human_turn:

                for event in pygame.event.get():
                    if termination_detected(event):
                        terminate()
                    elif event.type == MOUSEBUTTONDOWN:
                        x,y = pos_to_coord(event.pos)

                if x >= BOARDSIZE:
                    resp = self.human.attack(self.agent, (x - BOARDSIZE,y))
                    result, sunk_ship = resp['result'], resp['sunk_ship']
                    self.board.grid[x][y] = result

                    if result == 'M':
                        human_turn = not human_turn
                        play_miss_sound()
                    else:
                        play_hit_sound()

                    if sunk_ship:
                        self.info = 'Enemy\'s ' + sunk_ship + ' was destroyed!'

                    self.counter = self.counter + 1

                    self.board.draw(self.surface)
                    pygame.display.update()

                    x = 0
                    y = 0
            else:
                x, y = self.agent.find_target()
                resp = self.agent.attack(self.human, (x, y))
                result, sunk_ship = resp['result'], resp['sunk_ship']
                self.board.grid[x][y] = result

                if result == 'M':
                    human_turn = not human_turn

                if sunk_ship:
                        self.info = 'Your ' + sunk_ship + ' was destroyed!'

                self.counter = self.counter + 1

                self.board.draw(self.surface)
                pygame.display.update()

                x = 0
                y = 0

            # FPSCLOCK.tick(FPS)
        # reset game
        self.finish()


    def draw_info(self, human_fleet, ai_fleet, human_turn):
        # erase previous msgs
        self.scoreboard.reset(self.surface)

        # print human fleet
        draw_msglist(self.surface, self.font, 2*MARGIN, human_fleet)

        # print ai fleet
        draw_msglist(self.surface, self.font, WINDOWWIDTH - 105, ai_fleet)

        # print turn indicator
        turn = 'Your Turn' if human_turn else 'AI Turn'
        draw_msg(self.surface, self.font, turn, (WINDOWWIDTH / 2 - 40, WINDOWHEIGHT - 30))

        # print counter
        counter = 'Turn: ' + str(self.counter)
        draw_msg(self.surface, self.font, counter, (WINDOWWIDTH / 2 - 40, 470))

        # print game info
        draw_msg(self.surface, self.font, self.info, (WINDOWWIDTH / 2 - 60, 520))

    def finish(self):
        # show reset button
        print 'finish called'
        words = self.font.render('Reset', True, WHITE)
        rect = Rect(0, 0, 80, 20)
        rect.topleft = (WINDOWWIDTH / 2 - 40, 500)
        reset_btn = pygbutton.PygButton(rect, 'Reset')
        reset_btn.draw(self.surface)
        pygame.display.update()
        self.reset(reset_btn)

    def reset(self, reset_btn):
        print 'reset called'
        reset_clicked = False
        while True:
            if reset_clicked:
                break
            for event in pygame.event.get():
                if termination_detected(event):
                    terminate()

                elif 'click' in reset_btn.handleEvent(event):
                    self.human.reset()
                    self.agent.reset()
                    print 'game entities are reset'
                    reset_clicked = True
                    break

        self.reset_ingame_values()
        self.run()

    def reset_ingame_values(self):
        global SHIP_LIST, SHIP_LIST_BACKUP
        SHIP_LIST = copy.deepcopy(SHIP_LIST_BACKUP)
        self.counter = 0
        print 'ingame values are reset'

################################################################################

def pos_to_coord((x,y)):
    ''' Convert a position on screen to grid coordinate.
    '''
    cx = 0
    cy = 0
    if MARGIN < y < BOARD_LOWEREDGE:
        if MARGIN < x <= HUMAN_EDGE:
            # left side
            cx = x // (CELLSIZE + MARGIN)
            cy = y // (CELLSIZE + MARGIN)
        elif AI_EDGE <= x < WINDOWWIDTH - MARGIN:
            # right side
            cx = (x - CELLSIZE) // (CELLSIZE + MARGIN)
            cy = y // (CELLSIZE + MARGIN)
    return (cx,cy)

def coord_to_pos((x,y)):
    ''' Convert a grid coordinate to a position on screen.
    '''
    px = 0
    py = 0
    if 0 <= x < 2 * BOARDSIZE:
        py = (y + 1) * (CELLSIZE + MARGIN) - CELLSIZE / 2
        if x < BOARDSIZE:
            # left side
            px = (x + 1) * (CELLSIZE + MARGIN) - CELLSIZE / 2
        else:
            # right side
            px = (x + 2) * (CELLSIZE + MARGIN) - CELLSIZE / 2
    return (px,py)


def init_grid():
    ''' Init a 20x10 grid array.
    '''
    return [['0' for y in range(BOARDSIZE)] for x in range(BOARDSIZE * 2)]

def in_player_map((x,y)):
    ''' Tell if (x, y) falls in player's map range.
    '''
    x = x // (CELLSIZE + MARGIN)
    y = y // (CELLSIZE + MARGIN)
    if 0 <= x < BOARDSIZE and 0 <= y < BOARDSIZE:
        return True
    return False

def draw_msg(surface, font, msg, (x,y)):
    words = font.render(msg, True, WHITE)
    rect = words.get_rect()
    rect.topleft = (x,y)
    # clear that area first
    surface.fill(YALEBLUE, rect)
    surface.blit(words, rect)

def termination_detected(event):
    if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
        return True
    return False

def terminate():
    pygame.quit()
    sys.exit(0)

def draw_msglist(surface, font, left, msgs):
    # TODO
    base = SCOREBOARD_EDGE + 10
    for msg in msgs:
        base = base + 16
        draw_msg(surface, font, msg, (left, base))

def play_hit_sound():
    hit = pygame.mixer.Sound(HIT_SOUND_PATH)
    hit.play(maxtime=1500)

def play_miss_sound():
    miss = pygame.mixer.Sound(MISS_SOUND_PATH)
    miss.play(maxtime=1500)

def play_arrangement_sound():
    arr = pygame.mixer.Sound(ARR_SOUND_PATH)
    arr.play()

################################################################################

if __name__ == '__main__':
    game = Game()
    game.run()
