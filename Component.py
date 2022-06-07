from Util import *
from PieceManager import PieceManager
import numpy as np

class Component:

    def __init__(self, pieceId, edgeId=0) -> None:
        self.pieces = dict()
        self.pieces[(0, 0)] = [pieceId, edgeId]
        piece = PieceManager.get(pieceId)

        o1 = piece.corners[edgeId]
        o2 = piece.corners[(edgeId + 1) % 4]
        t1 = np.array([0, 0])
        t2 = np.array([100, 0])

        self.corners = dict()
        self.corners[(0, 0)] = transformPoint(piece.corners[edgeId], o1, t1, o2, t2)
        self.corners[(1, 0)] = transformPoint(piece.corners[(edgeId + 1) % 4], o1, t1, o2, t2)
        self.corners[(1, 1)] = transformPoint(piece.corners[(edgeId + 2) % 4], o1, t1, o2, t2)
        self.corners[(0, 1)] = transformPoint(piece.corners[(edgeId + 3) % 4], o1, t1, o2, t2)

        self.slots = dict()

    def setPiece(self, pieceId, bottomLeft, x, y):
        piece = PieceManager.get(pieceId)

        corner = [(0, 0), (1, 0), (1, 1), (0, 1)]
        dir = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for i in range(0, 4):
            dx, dy = dir[i]
            if (x + dx, y + dy) in self.pieces:
                o1 = piece.corners[(bottomLeft + i) % 4]
                o2 = piece.corners[(bottomLeft + i + 1) % 4]
                cx, cy = corner[i]
                t1 = self.corners[(x + cx, y + cy)]
                cx2, cy2 = corner[(i + 1) % 4]
                t2 = self.corners[(x + cx2, y + cy2)]
        for i in range(0, 4):
            cx, cy = corner[i]
            now = piece.corners[(bottomLeft + i) % 4]
            self.corners[(x + cx, y + cy)] = transformPoint(now, o1, t1, o2, t2)
        
        self.pieces[(x, y)] = [pieceId, bottomLeft]

    def getBox(self, x, y):
        corner = [(0, 0), (1, 0), (1, 1), (0, 1)]
        points = [None] * 4
        
        for i in range(0, 4):
            cx, cy = corner[i]
            cx = x + cx
            cy = y + cy
            if not (cx, cy) in self.corners:
                continue
            points[i] = self.corners[(cx, cy)]
        
        minX = 1000000
        maxX = -1000000
        minY = 1000000
        maxY = -1000000

        for i in points:
            if i is None:
                continue
            # print('owo')
            minX = min(minX, i[0])
            maxX = max(maxX, i[0])
            minY = min(minY, i[1])
            maxY = max(maxY, i[1])

        dx = maxX - minX
        dy = maxY - minY

        if (points[0] is None and points[1] is None) or (points[2] is None and points[3] is None):
            # print('dy=dx')
            dy = dx
        elif (points[0] is None and points[3] is None) or (points[1] is None and points[2] is None):
            # print('dx=dy')
            dx = dy
        
        if points[0] is None:
            minX = maxX - dx
            minY = maxY - dy
        elif points[2] is None:
            maxX = minX + dx
            maxY = minY + dy
        
        # print('box', x, y, minX, minY, maxX, maxY, points)
        return minX, minY, maxX, maxY


        