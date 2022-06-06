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

    def setPiece(self, slot, pieceId, bottomLeft):
        componentId, x, y = self.slots[slot]
        component = self.get(componentId)
        component.setPiece(pieceId, bottomLeft, x, y)
        while len(self.pieces) <= pieceId:
            self.pieces.append(-1)
        self.pieces[pieceId] = [componentId, x, y, bottomLeft]


ComponentManager = _ComponentManager()