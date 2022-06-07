from Piece import Edge
from Vector import *
from PieceManager import PieceManager
import numpy as np
from ComponentManager import ComponentManager

def edgeLength(e: Edge):
    len = 0
    first = True
    for i in e.edgePoints:
        if first:
            lst = i
            first = False
            continue
        len += vectorLength(i - lst)
        lst = i
    return len

def getMiddlePoints(e: Edge):

    sum = edgeLength(e)
    N = 100
    sep = sum / N

    totalLen = 0.0
    first = True
    points = []
    eps = 1e-9
    id = 0
    while id < len(e.edgePoints):
        if id == 0:
            lst = e.edgePoints[id]
            points.append(lst)
            nxtPos = sep
            id += 1
            continue
        p = e.edgePoints[id]
        nowLen = vectorLength(p - lst)
        if totalLen + nowLen + eps >= nxtPos:
            lst = interpolate(lst, p, nxtPos - totalLen)
            points.append(lst)
            totalLen = nxtPos
            nxtPos += sep
        else:
            totalLen += nowLen
            lst = p
            id += 1

    return points

def compareEdge(e1, e2):
    ps1 = getMiddlePoints(e1)
    ps2 = getMiddlePoints(e2)
    N = 100
    ps2.reverse()

    total = 0
    for i in range(0, N + 1):
        p1 = ps1[i]
        p2 = ps2[i]
        p2 = np.array([1.0 - p2[0], -p2[1]])
        total += vectorLength(p1 - p2)
    
    return total

def findClosestEdges(pieceId, edgeId):
    piece = PieceManager.get(pieceId)
    edge = piece.edges[edgeId]
    
    all = []
    for i in range(0, PieceManager.size()):
        if i == pieceId:
            continue
        nowPiece = PieceManager.get(i)
        for j in range(0, 4):
            nowEdge = nowPiece.edges[j]
            all.append([compareEdge(edge, nowEdge), i, j])
    
    all = sorted(all, key=lambda x: x[0])
    return all

def checkUsage(pieceId, edgeId):
    componentId, x, y, bottomLeft = ComponentManager.findPiece(pieceId)
    component = ComponentManager.get(componentId)
    dir = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    id = (edgeId - bottomLeft + 4) % 4
    dx, dy = dir[id]
    return (x + dx, y + dy) in component.pieces

def calcSlotScore(slotId, pieceId, edgeId):
    componentId, x, y = ComponentManager.getSlotPos(slotId)
    component = ComponentManager.get(componentId)
    dir = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    adj = [2, 3, 0, 1]

    total = 0.0
    for i in range(0, 4):
        dx, dy = dir[i]
        nx = x + dx
        ny = y + dy
        if not (nx, ny) in component.pieces:
            continue
        adjPiece, adjEdge = component.pieces[(nx, ny)]
        adjEdge = (adjEdge + adj[i]) % 4 
        nowEdge = (edgeId + i) % 4
        total += compareEdge(PieceManager.getEdge(pieceId, nowEdge), PieceManager.getEdge(adjPiece, adjEdge))
    return total
    
def findClosestPieces(slotId):
    componentId, _, _ = ComponentManager.getSlotPos(slotId)
    all = []
    for pieceId in range(0, PieceManager.size()):
        if not PieceManager.available(pieceId):
            continue
        if ComponentManager.findPiece(pieceId)[0] == componentId:
            continue
        for edgeId in range(0, 4):
            if checkUsage(pieceId, edgeId):
                continue
            all.append([calcSlotScore(slotId, pieceId, edgeId), pieceId, edgeId])
    all = sorted(all, key=lambda x: x[0])
    # print('findClosestPieces', all)
    return all

        