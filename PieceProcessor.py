import cv2
import numpy as np
from FileManager import FileManager
from PieceManager import PieceManager
from ImageManager import ImageManager
from Vector import *
import math
from Piece import *
import EdgeComparator
from Util import *
import Config

class _PieceProcessor:

    def __init__(self, contour, originImage):
        self.contour = contour
        self.originImage = originImage

    def getNextPoint(self, convexHull, id, diff, ori):
        size = convexHull.shape[0]

        lst = convexHull[id][0]
        now = 0.0
        for i in range(1, size + 1):
            nxt = (id + i * ori + size) % size
            p = convexHull[nxt][0]
            if now + vectorLength(p - lst) < diff:
                now += vectorLength(p - lst)
                lst = p
                continue
            lst = interpolate(lst, p, diff - now)
            lst = p
            break
        p1 = lst
        return p1

    def findCorners(self):
        convexHull = cv2.convexHull(self.contour)
        size = convexHull.shape[0]
        totalLen = 0.0

        for i in range(0, size):
            lst = convexHull[i - 1][0]
            p = convexHull[i][0]
            totalLen += vectorLength(p - lst)

        diff = totalLen * Config.cornerSampling
        sep = totalLen * Config.cornerMinDistance
        corners = []

        for i in range(0, size):
            p = convexHull[i][0]
            p1 = self.getNextPoint(convexHull, i, diff, -1)
            p2 = self.getNextPoint(convexHull, i, diff, 1)
            angle = calcAngle(p, p1, p2)
            corners.append([angle, i, p, p1, p2])
            # print([angle, i, p, p1, p2])

        self.corners = []
        finalCorners = []
        corners = sorted(corners, key=lambda x: x[0])

        for i in corners:
            flag = True
            for j in finalCorners:
                dis = vectorLength(i[2] - j[2])
                if dis < sep:
                    flag = False
                    break
            if flag:
                finalCorners.append(i)
            if len(finalCorners) > 4:
                finalCorners.pop()
        
        for i in finalCorners:
            self.corners.append(i)

        self.corners = sorted(self.corners, key=lambda x: x[1])
        return self.corners

    def processEdge(self, id):
        size = self.contour.shape[0]
        p1 = self.corners[id][2]
        p2 = self.corners[(id + 1) % 4][2]

        for i in range(0, size):
            if np.array_equal(self.contour[i][0], p1):
                id1 = i
            if np.array_equal(self.contour[i][0], p2):
                id2 = i

        p2relativep1 = p2 - p1
        p2relativep1 = cartesianToPolar(p2relativep1)

        originPoints = []
        edgePoints = []

        i = id1
        while True:
            p = self.contour[i][0]
            originPoints.append(p)
            rp = p - p1
            rp = cartesianToPolar(rp)
            rp = (rp[0], rp[1] - p2relativep1[1])
            rp = polarToCartesian(rp)
            rp = (rp[0] / p2relativep1[0], rp[1] / p2relativep1[0])
            edgePoints.append(np.array([rp[0], rp[1]]))
            if i == id2:
                break
            i = i - 1 + size
            i = i % size
        
        edge = Edge(
            originPoints=originPoints, 
            edgePoints=edgePoints, 
            interpolation=None, 
            rotate=-p2relativep1[1], 
            scale=1.0 / p2relativep1[0]
            )
        interpolation = EdgeComparator.getMiddlePoints(edge)
        edge.interpolation = interpolation
        return edge
    
    def getPixels(self):
        dx, dy, minX, minY = getContourSize(self.contour)
        # print(dx, dy, minX, minY)

        mask = np.zeros((dy, dx, 3), np.uint8)
        temp = shiftContour(self.contour, minX, minY)
        cv2.drawContours(mask, [temp], 0, (255, 255, 255), -1)
        pixels = []
        for i in range(0, dx):
            for j in range(0, dy):
                if not np.array_equal(mask[j][i],(255, 255, 255)):
                    continue
                pixels.append([minX + i, minY + j, self.originImage[minY + j][minX + i]])
        return pixels

    def drawPiece(self):
        gap = 10

        dx, dy, minX, minY = getContourSize(self.contour)
        image = np.full((dy + 2 * gap, dx + 2 * gap, 3), 255, np.uint8)
        # print(dx, dy, minX, minY)
        for i in self.piece.pixels:
            # print(i[0] - minX, i[1] - minY, i[2])
            image[gap + i[1] - minY][gap + i[0] - minX] = i[2]
        color = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255)]
        cnt = 0
        for e in self.piece.edges:
            tmp = pointArrayToContour(e.originPoints)
            tmp = shiftContour(tmp, minX - gap, minY - gap)
            cv2.drawContours(image, tmp, -1, color[cnt], 2)
            cnt += 1
        for p in self.piece.corners:
            cv2.circle(image, [p[0] - minX + gap, p[1] - minY + gap], 5, (0, 0, 0), -1)
        FileManager.wirteFolder('piece', 'piece-' + str(self.piece.id) + '.png', image)

    def process(self) -> int:
        self.findCorners()
        corners = []
        edges = []
        for i in range(0, 4):
            corners.append(self.corners[i][2])
            edges.append(self.processEdge(i))
        pixels = self.getPixels()
        self.piece = Piece(
            image=ImageManager.size(),
            id=PieceManager.size(),
            contour=self.contour, 
            corners=corners, 
            edges=edges,
            pixels=pixels
            )
        self.drawPiece()
        return PieceManager.addPiece(self.piece)

def processPiece(contour, originImage):
    pieceProcessor = _PieceProcessor(contour, originImage)
    return pieceProcessor.process()