import copy
import random
from shared import Ship

available = [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (0,8), (0,9), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (1,8), (1,9),(2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (2,8), (2,9),(3,0), (3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (3,7), (3,8), (3,9),(4,0), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (4,7), (4,8), (4,9),(5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7), (5,8), (5,9),(6,0), (6,1), (6,2), (6,3), (6,4), (6,5), (6,6), (6,7), (6,8), (6,9),(7,0), (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), (7,7), (7,8), (7,9),(8,0), (8,1), (8,2), (8,3), (8,4), (8,5), (8,6), (8,7), (8,8), (8,9),(9,0), (9,1), (9,2), (9,3), (9,4), (9,5), (9,6), (9,7), (9,8), (9,9)]

available_bk = [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (0,8), (0,9), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (1,8), (1,9),(2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (2,8), (2,9),(3,0), (3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (3,7), (3,8), (3,9),(4,0), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (4,7), (4,8), (4,9),(5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7), (5,8), (5,9),(6,0), (6,1), (6,2), (6,3), (6,4), (6,5), (6,6), (6,7), (6,8), (6,9),(7,0), (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), (7,7), (7,8), (7,9),(8,0), (8,1), (8,2), (8,3), (8,4), (8,5), (8,6), (8,7), (8,8), (8,9),(9,0), (9,1), (9,2), (9,3), (9,4), (9,5), (9,6), (9,7), (9,8), (9,9)]

def assignship(length, dir):
    global available

    startav = [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (0,8), (0,9), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (1,8), (1,9),(2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (2,8), (2,9),(3,0), (3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (3,7), (3,8), (3,9),(4,0), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (4,7), (4,8), (4,9),(5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7), (5,8), (5,9),(6,0), (6,1), (6,2), (6,3), (6,4), (6,5), (6,6), (6,7), (6,8), (6,9),(7,0), (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), (7,7), (7,8), (7,9),(8,0), (8,1), (8,2), (8,3), (8,4), (8,5), (8,6), (8,7), (8,8), (8,9),(9,0), (9,1), (9,2), (9,3), (9,4), (9,5), (9,6), (9,7), (9,8), (9,9)]

    random.shuffle(startav)
    start = startav[0]

    if (length == 5):
        if (dir == 'r'):
          if ((available.count(start) > 0) and (available.count((start[0]+1, start[1])) > 0) and (available.count((start[0]+2, start[1])) > 0) and (available.count((start[0]+3, start[1])) > 0) and (available.count((start[0]+4, start[1])) > 0)):
 
                                        shiplocarray = [start, (start[0]+1, start[1]), (start[0]+2, start[1]), (start[0]+3, start[1]), (start[0]+4, start[1])]
                                        available.remove(start)
                                        available.remove((start[0]+1, start[1]))
                                        available.remove((start[0]+2, start[1]))
                                        available.remove((start[0]+3, start[1]))
                                        available.remove((start[0]+4, start[1]))
                                        return shiplocarray
          else:
                                        startav.remove(start)
                                        return assignship(length, dir)
                    

        if (dir == 'd'):
          if ((available.count(start) > 0) and (available.count((start[0], start[1]+1)) > 0) and (available.count((start[0], start[1]+2)) > 0) and (available.count((start[0], start[1]+3)) > 0) and (available.count((start[0], start[1]+4)) > 0)):

                                        shiplocarray = [start, (start[0], start[1]+1), (start[0], start[1]+2), (start[0], start[1]+3), (start[0], start[1]+4)]
                                        available.remove(start)
                                        available.remove((start[0], start[1]+1))
                                        available.remove((start[0], start[1]+2))
                                        available.remove((start[0], start[1]+3))
                                        available.remove((start[0], start[1]+4))
                                        return shiplocarray
          else:
                                        startav.remove(start)
                                        return assignship(length, dir)

    if (length == 4):
     if (dir == 'r'):
      if ((available.count(start) > 0) and (available.count((start[0]+1, start[1])) > 0) and (available.count((start[0]+2, start[1])) > 0) and (available.count((start[0]+3, start[1])) > 0)):

                                    shiplocarray = [start, (start[0]+1, start[1]), (start[0]+2, start[1]), (start[0]+3, start[1])]
                                    available.remove(start)
                                    available.remove((start[0]+1, start[1]))
                                    available.remove((start[0]+2, start[1]))
                                    available.remove((start[0]+3, start[1]))
                                    return shiplocarray
      else:
                                    startav.remove(start)
                                    return assignship(length, dir)
                

     if (dir == 'd'):
      if ((available.count(start) > 0) and (available.count((start[0], start[1]+1)) > 0) and (available.count((start[0], start[1]+2)) > 0) and (available.count((start[0], start[1]+3)) > 0)):

                                    shiplocarray = [start, (start[0], start[1]+1), (start[0], start[1]+2), (start[0], start[1]+3)]
                                    available.remove(start)
                                    available.remove((start[0], start[1]+1))
                                    available.remove((start[0], start[1]+2))
                                    available.remove((start[0], start[1]+3))
                                    return shiplocarray
      else:
                                    startav.remove(start)
                                    return assignship(length, dir)

    if (length == 3):
     if (dir == 'r'):
      if ((available.count(start) > 0) and (available.count((start[0]+1, start[1])) > 0) and (available.count((start[0]+2, start[1])) > 0)):

                                    shiplocarray = [start, (start[0]+1, start[1]), (start[0]+2, start[1])]
                                    available.remove(start)
                                    available.remove((start[0]+1, start[1]))
                                    available.remove((start[0]+2, start[1]))
                                    return shiplocarray
      else:
                                    startav.remove(start)
                                    return assignship(length, dir)
                

     if (dir == 'd'):
      if ((available.count(start) > 0) and (available.count((start[0], start[1]+1)) > 0) and (available.count((start[0], start[1]+2)) > 0)):

                                    shiplocarray = [start, (start[0], start[1]+1), (start[0], start[1]+2)]
                                    available.remove(start)
                                    available.remove((start[0], start[1]+1))
                                    available.remove((start[0], start[1]+2))
                                    return shiplocarray
      else:
                                    startav.remove(start)
                                    return assignship(length, dir)

    if (length == 2):
     if (dir == 'r'):
      if ((available.count(start) > 0) and (available.count((start[0]+1, start[1])) > 0)):
                                    shiplocarray = [start, (start[0]+1, start[1])]
                                    available.remove(start)
                                    available.remove((start[0]+1, start[1]))
                                    return shiplocarray
      else:
                                    startav.remove(start)
                                    return assignship(length, dir)
                

     if (dir == 'd'):
      if ((available.count(start) > 0) and (available.count((start[0], start[1]+1)) > 0)):

                                    shiplocarray = [start, (start[0], start[1]+1)]
                                    available.remove(start)
                                    available.remove((start[0], start[1]+1))
                                    return shiplocarray
      else:
                                    startav.remove(start)
                                    return assignship(length, dir)

def assignailoc():
    global available

    available = copy.deepcopy(available_bk)

    cadirection = random.choice('dr')
    badirection = random.choice('dr')
    sudirection = random.choice('dr')
    crdirection = random.choice('dr')
    dedirection = random.choice('dr')

    ca = assignship(5, cadirection)
    ba = assignship(4, badirection)
    su = assignship(3, sudirection)
    cr = assignship(3, crdirection)
    de = assignship(2, dedirection)

    result = []
    result.append(Ship(t='Carrier', coords=ca))
    result.append(Ship(t='Battleship', coords=ba))
    result.append(Ship(t='Submarine', coords=su))
    result.append(Ship(t='Cruiser', coords=cr))
    result.append(Ship(t='Destroyer', coords=de))
    # dict = {'Carrier':ca, 'Battleship':ba, 'Submarine':su, 'Cruiser':cr, 'Destroyer':de}
    # print (dict)
    return result

# assignailoc()
