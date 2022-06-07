from EdgeComparator import *

class _SolvingManager:

    def __init__(self):
        self.counter = []
        self.todo = []

    def get(self, slotId):
        while len(self.counter) <= slotId:
            self.counter.append(-1)
        return self.counter[slotId]
    
    def next(self, slotId):
        while len(self.counter) <= slotId:
            self.counter.append(-1)
        self.counter[slotId] += 1
        self.counter[slotId] = min(self.counter[slotId], len(self.getTodo(slotId)) - 1)
        return self.counter[slotId]
    
    def last(self, slotId):
        while len(self.counter) <= slotId:
            self.counter.append(-1)
        self.counter[slotId] -= 1
        self.counter[slotId] = max(self.counter[slotId], 0)
        return self.counter[slotId]

    def now(self, slotId):
        while len(self.counter) <= slotId:
            self.counter.append(-1)
        return self.counter[slotId]
    
    def reset(self, slotId):
        while len(self.counter) <= slotId:
            self.counter.append(-1)
        while len(self.todo) <= slotId:
            self.todo.append(None)
        self.counter[slotId] = -1
        self.todo[slotId] = None

    def getTodo(self, slotId):
        while len(self.todo) <= slotId:
            self.todo.append(None)
        if self.todo[slotId] is None:
            self.todo[slotId] = findClosestPieces(slotId)
        return self.todo[slotId]

SolvingManager = _SolvingManager()