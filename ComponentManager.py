from Component import Component
from PieceManager import PieceManager
from Util import getPixelsSize, putTextWithCircle, transformPixels
import numpy as np
import cv2

class _ComponentManager:

    def __init__(self):
        self.components = []
        self.slots = []
        self.pieces = []

    def newSlot(self, componentId, x, y):
        self.slots.append([componentId, x, y])
        return len(self.slots) - 1

    def get(self, num) -> Component:
        component = self.components[num]
        return component
    
    def newComponent(self, pieceId):
        self.components.append(Component(pieceId))
        return len(self.components) - 1

    def getSlot(self, componentId, x, y):
        component = self.get(componentId)
        if (x, y) in component.pieces:
            return -1
        dir = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        ok = False
        for dx, dy in dir:
            if (x + dx, y + dy) in component.pieces:
                ok = True
        if not ok:
            return -1
        if not (x, y) in component.slots:
            component.slots[(x, y)] = self.newSlot(componentId, x, y)
        return component.slots[(x, y)]
    
    def getSlotPos(self, slotId):
        if slotId >= len(self.slots):
            return None
        componentId, x, y = self.slots[slotId]
        if self.getSlot(componentId, x, y) == -1:
            return None
        return self.slots[slotId]
        
    def updateSlots(self, componentId):
        component = self.get(componentId)
        dir = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for x, y in component.pieces:
            for dx, dy in dir:
                self.getSlot(componentId, x + dx, y + dy)

    def findPiece(self, pieceId):
        while len(self.pieces) <= pieceId:
            self.pieces.append(-1)
        if self.pieces[pieceId] == -1:
            self.pieces[pieceId] = [self.newComponent(pieceId), 0, 0, 0]
        return self.pieces[pieceId]

    def setPiecePos(self, componentId, x, y, pieceId, bottomLeft):
        component = self.get(componentId)
        # print('owo', x, y)
        component.setPiece(pieceId, bottomLeft, x, y)
        while len(self.pieces) <= pieceId:
            self.pieces.append(-1)
        self.pieces[pieceId] = [componentId, x, y, bottomLeft]

    def setPiece(self, slot, pieceId, edgeId):
        componentId, x, y = self.slots[slot]
        pieceComponentId, px, py, bottomLeft = self.findPiece(pieceId)
        return self.connectComponent(componentId, pieceComponentId, x, y, px, py, (edgeId - bottomLeft + 4) % 4)

    def slotAvailable(self, slotId):
        return not self.getSlotPos(slotId) is None

    def connectComponent(self, componentId1, componentId2, ox, oy, tx, ty, ori):
        assert(componentId1 != componentId2)
        if ori == 0:
            trans = [[1, 0], [0, 1]]
        elif ori == 1:
            trans = [[0, 1], [-1, 0]]
        elif ori == 2:
            trans = [[-1, 0], [0, -1]]
        else:
            trans = [[0, -1], [1, 0]]

        todo = []
        component1 = self.get(componentId1)
        component2 = self.get(componentId2)
        for x, y in component2.pieces:
            pieceId, edgeId = component2.pieces[(x, y)]
            x = x - tx
            y = y - ty
            nx = trans[0][0] * x + trans[0][1] * y + ox
            ny = trans[1][0] * x + trans[1][1] * y + oy
            if (ox, oy) in component1.pieces:
                return False
            todo.append([nx, ny, pieceId, (edgeId + ori) % 4])
        for i in todo:
            self.setPiecePos(componentId1, i[0], i[1], i[2], i[3])
        self.components[componentId2] = None
        return True

ComponentManager = _ComponentManager()