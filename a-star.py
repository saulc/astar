from collections import defaultdict, deque

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

r = 90
def rcost(state):
    global r
    # print('rcost', state, r)
    r -= 1

    return r if r > 0 else 0

#h0
def h0(state):
    return 0

#h1
def h1(state):
    n = 0
    for l in state:
        for i in l:
            if i != 4: n += 1
    return n

# TODO: implement huristic for A*
def hUID(state):
    pass


#goal test #1
def goal(state):
    # print('goal test')
    #if box/goal > 0 and goal/keeper == 0 and box == goal == 0
    # and keeper == 1 assuming goals == boxes then gameover! win.
    a = [0] * 5 
    for l in state:
        for i in l:
            if i == 5: a[0] +=1
            elif i == 6: a[1] += 1
            elif i == 2: a[2] += 1
            elif i == 4: a[3] += 1
            elif i == 3: a[4] += 1
    # print(a)
    return  a[0] > 0 and a[1] == 0 and a[2] == 0 and a[3] == 0 and a[4] == 1
    

#next-states #2
def msuccessors(state):
    print('successors')
    printState(state)
    s = []  #4 directions
    for i in range(4):
        t = trymove(state, i)
        # print(i, t)
        if t != None: 
            s.append(t)
            printState(t)
    # print(s)
    return s

#suggested helper functions
def getsq(state, r, c):
    if r >= len(state) or c >= len(state[r]): return 1
    return state[r][c]

def setsq(state, r, c, v):
    s = state.copy()
    s[r][c] = v
    return s

def trymove(state, dir):
    x, y = findme(state)
    c = checksq(state, dir)
    if c == 0 or c == 4:
        return makemove(state, dir, x, y)
    elif c == 2 or c == 5:
        if checkpush(state,dir):
            return makemove(state, dir, x, y)
    return None

def checksq(state, dir):
    x, y = findme(state)
    # print('starting at:', x, y)
    # check the other side of the box
    if dir == 0: y += 1
    elif dir == 1: x += 1
    elif dir == 2: y -= 1
    elif dir == 3: x -= 1
    # print('checking: ', x, y)
    return getsq(state, x, y)

def checkpush(state, dir):
    x, y = findme(state)
    # check the other side of the box
    if dir == 0: y += 2
    elif dir == 1: x += 2
    elif dir == 2: y -= 2
    elif dir == 3: x -= 2
    return getsq(state, x,y) == 0


def makemove(state, dir, x, y):
    s = None
    c = 0

    if dir == 0: #down
        s = setsq(state, x, y+1, 3)
        s = setsq(state, x, y, c)
    elif dir == 1: #right
        s = setsq(state, x+1, y, 3)
        s = setsq(state, x, y, c)
    elif dir == 2: #up
        s = setsq(state, x, y-1, 3)
        s = setsq(state, x, y, c)
    elif dir == 3: #left
        s = setsq(state, x-1, y, 3)
        s = setsq(state, x, y, c)
    return s


def findme(state):
    x = -1
    y = x
    for i in range(len(state)):
        for j in range(len(state[i])):
            c = getsq(state, i, j)
            if c == 3:
                return i, j


def printState(state, printer=True):
    p = []
    for l in state:
        t = ''
        for i in l:
            t += square(i).char + ' '
        if(printer): print(t)
        p.append(t)
    return p

# data = [None] * 5001
# print('test')
# print(len(data))
# print(data[0:11])
# if not data[4]:
#     print('not')
# print('data')

# s = [[0,0,0,0,4]]
s = [[0 ,0 ,1 ,1 ,1 ,1 ,0 ,0 ,0],
[1 ,1 ,1 ,0 ,0 ,1 ,1 ,1 ,1],
[1 ,0 ,0 ,0 ,0 ,0 ,2 ,0 ,1],
[1 ,0 ,1 ,0 ,0 ,1 ,2 ,0 ,1],
[1 ,0 ,4 ,0 ,4 ,1 ,3 ,0 ,1],
[1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 , 1]]

# goal test
gt = [[0 ,0 ,1 ,1 ,1 ,1 ,0 ,0 ,0],
[1 ,1 ,1 ,0 ,0 ,1 ,1 ,1 ,1],
[1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1],
[1 ,0 ,1 ,0 ,0 ,1 ,0 ,0 ,1],
[1 ,0 ,5 ,0 ,5 ,1 ,3 ,0 ,1],
[1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 , 1]]
 
path = MyPath(s)
# one = h1(path.state)
# print(one)
# printState(path.state)
astar(path.state, goal, msuccessors, cost, rcost)



