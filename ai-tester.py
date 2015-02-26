
import copy
import sys
import random
import time

from randomgen import assignailoc
from shared import *

MAPSIZE = 10

# game data counters
ROUND = 0
AI1_WINS = 0
AI2_WINS = 0
AI1_MISS = 0
AI1_HIT = 0
AI2_MISS = 0
AI2_HIT = 0
AI1_TOTAL_WIN_STEPS = 0
AI2_TOTAL_WIN_STEPS = 0
AI1_TOTAL_STEPS = 0
AI2_TOTAL_STEPS = 0
AI1_TOTAL_THINKING_TIME = 0
AI2_TOTAL_THINKING_TIME = 0

def run(ai1, ai2):
    global  AI1_WINS,\
            AI2_WINS,\
            AI1_MISS,\
            AI1_HIT,\
            AI2_MISS,\
            AI2_HIT,\
            AI1_TOTAL_WIN_STEPS,\
            AI2_TOTAL_WIN_STEPS,\
            AI1_TOTAL_STEPS,\
            AI2_TOTAL_STEPS,\
            AI1_TOTAL_THINKING_TIME,\
            AI2_TOTAL_THINKING_TIME

    counter = 0
    elapsed = 0
    ai1_turn = random.choice([True, False])

    while True:
        if ai1.lose():
            AI2_WINS = AI2_WINS + 1
            AI2_TOTAL_WIN_STEPS = AI2_TOTAL_WIN_STEPS + counter
            break
        if ai2.lose():
            AI1_WINS = AI1_WINS + 1
            AI1_TOTAL_WIN_STEPS = AI1_TOTAL_WIN_STEPS + counter
            break

        if ai1_turn:
            start = time.clock()
            # evaluate decision time
            target = ai1.find_target()
            elapsed = (time.clock() - start)

            AI1_TOTAL_STEPS = AI1_TOTAL_STEPS + 1
            AI1_TOTAL_THINKING_TIME = AI1_TOTAL_THINKING_TIME + elapsed

            r = ai1.attack(ai2, target)
            result = r['result']
            if result == 'M':
                AI1_MISS = AI1_MISS + 1
                ai1_turn = not ai1_turn
            if result == 'H':
                AI1_HIT = AI1_HIT + 1
        else:
            start = time.clock()
            # evaluate decision time
            target = ai2.find_target()
            elapsed = (time.clock() - start)

            AI2_TOTAL_STEPS = AI2_TOTAL_STEPS + 1
            AI2_TOTAL_THINKING_TIME = AI2_TOTAL_THINKING_TIME + elapsed

            r = ai2.attack(ai1, target)
            result = r['result']
            if result == 'M':
                AI2_MISS = AI2_MISS + 1
                ai1_turn = not ai1_turn
            if result == 'H':
                AI2_HIT = AI2_HIT + 1

        counter = counter + 1

def summary():
    global  AI1_WINS,\
            AI2_WINS,\
            AI1_MISS,\
            AI1_HIT,\
            AI2_MISS,\
            AI2_HIT,\
            AI1_TOTAL_WIN_STEPS,\
            AI2_TOTAL_WIN_STEPS,\
            AI1_TOTAL_STEPS,\
            AI2_TOTAL_STEPS,\
            AI1_TOTAL_THINKING_TIME,\
            AI2_TOTAL_THINKING_TIME

    print '**********'
    print 'AI 1'
    print 'Winning Percentage:',            AI1_WINS * 100 / float(ROUND), '%'
    print 'Hits/Shots Fired Percentage:',   AI1_HIT * 100 / float(AI1_HIT + AI1_MISS), '%'
    print 'Avg Steps to Win:',              AI1_TOTAL_WIN_STEPS / float(ROUND)
    print 'Avg Thinking Time:',             AI1_TOTAL_THINKING_TIME * 1000 / float(AI1_TOTAL_STEPS)

    print '**********'
    print 'AI 2'
    print 'Winning Percentage:',            AI2_WINS * 100 / float(ROUND), '%'
    print 'Hits/Shots Fired Percentage:',   AI2_HIT * 100 / float(AI2_HIT + AI2_MISS), '%'
    print 'Avg Steps to Win:',              AI2_TOTAL_WIN_STEPS / float(ROUND)
    print 'Avg Thinking Time:',             AI2_TOTAL_THINKING_TIME * 1000 / float(AI2_TOTAL_STEPS)

def init_ai(ai_class):
    my_map = Map(size=MAPSIZE)
    fleet = assignailoc()
    my_map.generate_player_map(fleet_to_array(fleet))

    enemy_map = Map(size=MAPSIZE)
    enemy_map.generate_ai_enemy_map()

    return ai_class(my_map=my_map, 
        enemy_map=enemy_map, 
        fleet=fleet, 
        enemy_fleet=copy.deepcopy(ENEMY_FLEET),
        target_cache=[])

if __name__ == '__main__':
    # read args
    ai1_path, ai2_path, repeat = sys.argv[1], sys.argv[2], sys.argv[3]

    ROUND = int(repeat)

    # import AI class from file
    ai1_module = __import__(ai1_path)
    ai2_module = __import__(ai2_path)

    # from ai1_module import Agent as ai1
    # from ai2_module import Agent as ai2

    # run test
    for i in range(ROUND):
        # time.sleep(0.01)
        # init 2 AIs
        ai1_instance = init_ai(ai1_module.Agent)
        ai2_instance = init_ai(ai2_module.Agent)
        run(ai1_instance, ai2_instance)

    # see summary
    summary()