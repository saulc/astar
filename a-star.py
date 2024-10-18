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
