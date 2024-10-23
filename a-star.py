from collections import defaultdict, deque
from copy import deepcopy

# Priority Queue for the open list
class PQ:
    def __init__(self):
        self.data = [None] * 5001
        self.data[4999] = 0
        self.data[5000] = 100000

    def add(self, my_path, new_cost):
        self.data[4999] += 1
        self.data[5000] = min(self.data[5000], new_cost)
        if not self.data[new_cost]:
            self.data[new_cost] = []
        self.data[new_cost].append(my_path)

    def lowest_cost(self, start):
        if self.data[4999] == 0:
            return 100000
        else:
            i = start
            while not self.data[i]:
                i += 1
            return i

    def remove(self):
        old_cost = self.data[5000]
        if self.data[4999] == 0:
            return None
        ans = self.data[old_cost].pop(0)
        self.data[4999] -= 1
        self.data[5000] = self.lowest_cost(old_cost)
        return ans

    def peek(self):
        old_cost = self.data[5000]
        return None if self.data[4999] == 0 else self.data[old_cost][0]

    def empty(self):
        return self.data[4999] == 0

# Hash table for the closed list
class MyHT:
    def __init__(self, size):
        self.size = size
        self.data = defaultdict(list)

    def hash_fn(self, s):
        def hash_helper(start, l):
            return start if not l else hash_helper(l[0] + start * 65559, l[1:])
        
        ans = 0
        for item in s:
            ans = hash_helper(ans, item)
        return ans

    def remove(self, key):
        hash_val = self.hash_fn(key) % self.size
        self.data[hash_val] = [kv for kv in self.data[hash_val] if kv[0] != key]

    def add(self, key, value):
        hash_val = self.hash_fn(key) % self.size
        self.data[hash_val].append((key, value))

    def get(self, key):
        hash_val = self.hash_fn(key) % self.size
        for k, v in self.data[hash_val]:
            if k == key:
                return v
        return None

# A* implementation
class MyPath:
    def __init__(self, state, previous=None, cost_so_far=0, total_cost=0):
        self.state = state
        self.previous = previous
        self.cost_so_far = cost_so_far
        self.total_cost = total_cost

    def states(self):
        if not self:
            return []
        return [self.state] + MyPath.states(self.previous)

expanded = 0
generated = 1

def astar(start_state, goal_p, successors, cost_fn, remaining_cost_fn):
    global expanded, generated
    expanded, generated = 0, 1
    open_list = PQ()
    closed_list = MyHT(1000000)
    open_list.add(MyPath(start_state), 0)
    while not open_list.empty():
        if goal_p(open_list.peek().state):
            return list(reversed(MyPath.states(open_list.peek())))
        my_path = open_list.remove()
        state = my_path.state
        new_val = my_path.total_cost
        hash_val = closed_list.hash_fn(state)
        closed_val = closed_list.get(state)
        if not closed_val or new_val < closed_val:
            expanded += 1
            if closed_val:
                closed_list.remove(state)
            closed_list.add(state, new_val)
            for state2 in successors(state):
                cost = my_path.cost_so_far + cost_fn(state, state2)
                cost2 = remaining_cost_fn(state2)
                total_cost = cost + cost2
                generated += 1
                open_list.add(MyPath(state2, my_path, cost, total_cost), total_cost)

# The rest of the code for testing and other purposes would go here

'''
Content Integer ASCII
Blank       0  ‘ ‘  (space)
Wall        1  ‘#’
Box         2  ‘$’
Keeper      3  ‘@’
Goal        4  ‘.’
Box/goal    5  ‘*’
Keeper/goal 6  ‘+’
'''
# helper class to convert id to chars
class square:
    types = ['blank', 'wall', 'box', 'keeper', 'goal', 'box/goal', 'keeper/goal']
    chars = [' ', '#', '$', '@', '.', '*', '+']
    def __init__(self, id):
        self.type = self.types[id]
        self.char = self.chars[id]
        self.id = id


def cost(s1, s2):
    # print('cost fun', s1, s2)
    return 1

#dont' think this will work just replace huristic in astar call.
# def rcost(state, h):
#     if h == 0: return h0(state)
#     elif h == 1: return h1(state)
#     elif h == 2 return hUID(state)

#     print('invalid huristic, using trivial option.')
#     return 0

#3 h0
def h0(state):
    return 0

#4 h1
def h1(state):
    n = 0
    for l in state:
        for i in l:
            if i != 4: n += 1
    return n

#5 TODO: implement huristic for A*
def h303673583(state):
    n = 0
    g = 0
    for l in state:
        for i in l:
            if i != 4: n += 1
            if i == 5: g += 1
    r = n - g*3
    # give 'weight' to boxes in goals.
    return r if r > 0 else 0


#goal test #1
def goal(state):
    # print('goal test')
    #if box/goal > 0 and   boxes == 0 and keeper exists
    # since goals != boxes
    #made the rules too strict at first.
    a = [0] * 5 
    for l in state:
        for i in l:
            if i == 5: a[0] +=1
            # elif i == 6: a[1] += 1
            elif i == 2: a[2] += 1
            # elif i == 4: a[3] += 1
            elif i == 3 or i == 6: a[4] += 1
    # print(a)
    g =  a[0] > 0 and a[2] == 0 and a[4] == 1
    # print('goal: ', g)
    return g
    

#next-states #2
def msuccessors(state):
    # print('current state')
    # printState(state) 
    s = []  #4 directions
    for i in range(4): 
        t = trymove(state, i)
        if t != None: 
            s.append(t)
            # print(i)
            # printState(t)
    
    # print('successors')
    # printStates(s) 
    #print the states side by side
    # print(s)
    return s

#suggested helper functions
# 1 b
def getsq(state, r, c):
    if r >= len(state) or c >= len(state[r]) or r < 0 or c < 0: 
        print('out of bounds, return wall value')
        return 1
    return state[r][c]

# 2 b
def setsq(state, r, c, v):
    #was stuck for 2 days because of copy instead of deepcopy.
    s = deepcopy(state)
    s[r][c] = v
    return s

# 3 b check if the direction is possible return the state from that move
def trymove(state, dd):
    # print( dd, 'trying move from state: ') 
    # printState(state)
    x, y = findme(state)
    c = checksq(state,  dd, x, y) 
    # print('checking: ', x, y, c)
    if c == 0 or c == 4: 
        return makemove(state,  dd, x, y, c)
    elif c == 2 or c == 5:
        p , q = checkpush(state, dd, x, y)
        # print(p, q)
        if p:
            # print('moving box')
            return push(state,  dd, x, y, c, q)

    # print('try move failed')
    return None

#check the value of the next sqaure in the direction of dd
def checksq(state,  dd, x, y): 
    # print('starting at:', x, y,  dd) 
    a = x
    b = y
    # print(type( dd))
    if  dd == 0: 
        b += 1
        # print('right')
    elif  dd == 1: 
        a += 1
        # print('down')
    elif  dd == 2: 
        b -= 1
        # print('left')
    elif  dd == 3: 
        a -= 1
        # print('up')
    else: print('direction invalid')
    # print('checking: ', a, b)
    return getsq(state, a, b)

#found a box, return if it can be moved and what is the other side  
def checkpush(state,  dd, x, y): 
    # check the other side of the box
    a = x
    b = y 
    if  dd == 0: b += 2
    elif  dd == 1: a += 2
    elif  dd == 2: b -= 2
    elif  dd == 3: a -= 2
    q = getsq(state, a,b) 
    # print('checkpush', q)
    # only push a box if the space is empty or a goal.
    return q == 0 or q == 4 , q

#move a box a set the new vaules, return a copy of the state with changes
def push(state,  dd, x, y, c, q):
    # moving a box actually has alot of weird cases to deal with
    s = state 
    # print('push')
    # printState(s)
    b = 3
    m = getsq(s, x, y)

    # print(c, b, q)
    if c == 5:  #box in a goal in the direction of move
        b = 6   #keeper move into goal
        if m == 3: c = 0
        elif m == 6: 
            c = 4
            b = 6
    elif c == 6: c = 4
    else: c = 0

    # a goal on the other side of a box.
    if q == 4: q = 5
    elif q == 0: #or a blank space
        q = 2
        if m == 6: c = 4
        # b = 3

    #keep track of 3 boxes and make needed changes
    
    # if b == 2 : b = 0
    # elif b == 6: b = 3
    # print('b', b)

    if  dd == 0: 
        s = setsq(s, x, y+2, q)
        s = setsq(s, x, y+1, b)
        s = setsq(s, x, y, c)
    elif  dd == 1: 
        s = setsq(s, x+2, y, q)
        s = setsq(s, x+1, y, b)
        s = setsq(s, x, y, c)
    elif  dd == 2: 
        s = setsq(s, x, y-2, q)
        s = setsq(s, x, y-1, b)
        s = setsq(s, x, y, c)
    elif  dd == 3: 
        s = setsq(s, x-2, y, q)
        s = setsq(s, x-1, y, b)
        s = setsq(s, x, y, c)
    return s

#a bit of repeated logic between push/makemove but it works... 
#make a move that is not moving a box
def makemove(state,  dd, x, y, c):
    s = state
    # print('move')
    # printState(s)
    d = 0

    m = getsq(s, x, y)
    # if the next square is a global
    if c == 4: c = 6
    else: c = 3

    # if keeper is on a goal
    if m == 6: 
        if c != 6:
            c = 3 
        d = 4

    if  dd == 0: 
        s = setsq(s, x, y+1, c)
        s = setsq(s, x, y, d)
    elif  dd == 1: 
        s = setsq(s, x+1, y, c)
        s = setsq(s, x, y, d)
    elif  dd == 2: 
        s = setsq(s, x, y-1, c) 
        s = setsq(s, x, y, d)
    elif  dd == 3: 
        s = setsq(s, x-1, y, c)
        s = setsq(s, x, y, d)
    else: print('invalid move')
     
    # print('made a move.')
    return s

#return the location of the keeper
def findme(state):
    for i in range(len(state)):
        for j in range(len(state[i])):
            c = getsq(state, i, j)
            if c == 3 or c == 6:
                return i, j
    print('no keeper found')
    return -1, -1

#print the encoded states side by side
def printStates(states, printer=True):
    if len(states) < 1: return None
     
    r = []
    i = 0
    print('solved in: ',len(states), 'steps')
    while len(states) > i :

        t = states[i:i+4]  #suprisingly this just works?
        
        s = [] #reset!!! lost an hour for placing out of loop.
        i += 4
        # cut up the list
        for k in t:
            a = printState(k, False)
            s.append(a)

        # get the encoded version as a list 
        for z in range(len(s[0])):
            x = ''
            # combine each line for each state in list section 4 wide
            for k in range(len(t)): 
                x += s[k][z] + '   '
            r.append(x) #save it to return
            if printer: print(x)
        if printer: print()
    return r

# print a single encoded state
def printState(state, printer=True):
    p = []
    for l in state:
        t = ''
        for i in l:
            t += square(i).char + ' '
            # t += str(i) + ' '
        if(printer): print(t)
        p.append(t)
    return p

# a playable game loop for testing
# returns the states(moves) made
def gameloop(state):
    s = state
    moves = [s]
    while True:
        # s = state

        print('--Acme Sokoban--')
        printState(s)
        # printStates(msuccessors(s))
        if goal(s): 
            print('You did it.')
            break
        d = input('enter a direction (0-3): ')
        if len(d) > 0:
           d = int(d)
           if d > 3: print(' 0 - Right, 1 - down, 2 - left, 3 - up')
        print(d)
        t = trymove(s, d)
        if t != None: 
            moves.append(t)
            s = t
        else: print('invalid move.')

    printStates(moves)
    # for t in moves:
    #     printState(t) 
    return moves


# figuring out the input types for astar
# data = [None] * 5001
# print('test')
# print(len(data))
# print(data[0:11])
# if not data[4]:
#     print('not')
# print('data')

# s = [[0,0,0,0,4]]
 

s2 = [
[1  ,1  ,1  ,1  ,1],
[1  ,0  ,0  ,4  ,1],
[1  ,0  ,2  ,3  ,1],
[1  ,0  ,0  ,0  ,1],
[1  ,0  ,0  ,0  ,1],
[1  ,1  ,1  ,1  ,1]
]

s3 = [
[1  ,1  ,1  ,1  ,1],
[1  ,0  ,0  ,6  ,1],
[1  ,0  ,2  ,0  ,1],
[1  ,0  ,0  ,0  ,1],
[1  ,0  ,0  ,0  ,1],
[1  ,1  ,1  ,1  ,1] ]

s4 = [
[1  ,1  ,1  ,1  ,1],
[1  ,4  ,2  ,0  ,1],
[1  ,0  ,0  ,0  ,1],
[1  ,0  ,0  ,0  ,1],
[1  ,0  ,5  ,3  ,1],
[1  ,1  ,1  ,1  ,1],
]

# p1 example
s = [
[0 ,0 ,1 ,1 ,1 ,1 ,0 ,0 ,0],
[1 ,1 ,1 ,0 ,0 ,1 ,1 ,1 ,1],
[1 ,0 ,0 ,0 ,0 ,0 ,2 ,0 ,1],
[1 ,0 ,1 ,0 ,0 ,1 ,2 ,0 ,1],
[1 ,0 ,4 ,4 ,0 ,1 ,3 ,0 ,1],
[1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1] ]

# slighty differnt example(goal moved) with surprising moves/solution
s = [
[0 ,0 ,1 ,1 ,1 ,1 ,0 ,0 ,0],
[1 ,1 ,1 ,0 ,0 ,1 ,1 ,1 ,1],
[1 ,0 ,0 ,0 ,0 ,0 ,2 ,0 ,1],
[1 ,0 ,1 ,0 ,0 ,1 ,2 ,0 ,1],
[1 ,0 ,0 ,4 ,4 ,1 ,3 ,0 ,1],
[1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1] ]

# some easy test levels
ss = [
[1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1],
[1 ,0 ,0 ,4 ,4 ,0,2 ,3 ,1],
[1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1]
]

sss = [
[1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1],
[1 ,0 ,4 ,2 ,3 ,2 ,4 ,0 ,1],
[1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1]
]
 
# set to True to play the game
# False to run astar and show the solution
game = False 

#just store the state (gameboard) to start with
start = s

# msuccessors(s)
if not game:
    print('--Acme Sokoban Solver--')
    print('Start State: ')
    printState(start)
    r = astar(start, goal, msuccessors, cost, h1)

    # break r into 4s and use printState
    printStates(r) 

else:
    gameloop(start)

