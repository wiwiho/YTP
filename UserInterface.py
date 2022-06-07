from EdgeComparator import *
from matplotlib import pyplot as plt
from Util import *
from ComponentManager import ComponentManager
from Component import Component

def showEdgeCompare(piece1, edge1, piece2, edge2):
    e1 = PieceManager.get(piece1).edges[edge1]
    e2 = PieceManager.get(piece2).edges[edge2]

    ps1 = getMiddlePoints(e1)
    ps2 = getMiddlePoints(e2)

    newPs2 = []
    N = 100

    total = 0
    for i in range(0, N + 1):
        p1 = ps1[i]
        p2 = ps2[N - i]
        p2 = np.array([1.0 - p2[0], -p2[1]])
        newPs2.append(p2)
        total += vectorLength(p1 - p2)

    print('# showEdgeCompare')
    print('total distance:', total)

    x1 = []
    y1 = []
    x2 = []
    y2 = []
    for i in ps1:
        x1.append(i[0])
        y1.append(i[1])
    for i in newPs2:
        x2.append(i[0])
        y2.append(i[1])

    fig, ax = plt.subplots()
    ax.plot(x1, y1, color='blue')
    ax.plot(x2, y2, color='red')
    ax.set_aspect(1)

    plt.show()

def showClosestEdges(pieceId, edgeId, max=5):
    ans = findClosestEdges(pieceId, edgeId)
    for i in range(0, len(ans)):
        if i > max and max != -1:
            break
        print(i, '. ', ans[i][1], ':', ans[i][2], sep='')
        
def showClosestPieces(slotId, max=5):
    ans = findClosestPieces(slotId)
    for i in range(0, len(ans)):
        if i > max and max != -1:
            break
        print(i, '. ', ans[i][1], ':', ans[i][2], sep='')

def previewConnectEdges(pieceId1, edgeId1, pieceId2, edgeId2):

    width = 100

    piece1 = PieceManager.get(pieceId1)
    piece2 = PieceManager.get(pieceId2)

    o1 = piece1.corners[edgeId1]
    o2 = piece1.corners[(edgeId1 + 1) % 4]
    t1 = np.array([0, 0])
    t2 = np.array([width, 0])
    
    pixels = transformPixels(piece1.pixels, o1, t1, o2, t2)

    o1 = piece2.corners[(edgeId2 + 1) % 4]
    o2 = piece2.corners[edgeId2]

    pixels += transformPixels(piece2.pixels, o1, t1, o2, t2)

    dx, dy, minX, minY = getPixelsSize(pixels)
    # print(dx, dy, minX, minY)

    image = np.full((dy, dx, 3), 255, np.uint8)
    for i in pixels:
        image[i[1] - minY][i[0] - minX] = i[2]
    cv2.circle(image, t1 - np.array([minX, minY]), 5, [0, 0, 255], -1)
    cv2.circle(image, t2 - np.array([minX, minY]), 5, [0, 0, 255], -1)

    showImage('preview', image)

def showComponent(componentId, number=False, slot=False):
    if slot:
        ComponentManager.updateSlots(componentId)

    gap = 50
    
    component = ComponentManager.get(componentId)
    pixels = []
    for x, y in component.pieces:
        pieceId, bottomLeft = component.pieces[(x, y)]
        piece = PieceManager.get(pieceId)
        t1 = component.corners[(x, y)]
        t2 = component.corners[(x + 1, y)]
        o1 = piece.corners[bottomLeft]
        o2 = piece.corners[(bottomLeft + 1) % 4]
        pixels += transformPixels(piece.pixels, o1, t1, o2, t2)

    dx, dy, minX, minY = getPixelsSize(pixels)
    maxX = minX + dx - 1
    maxY = minY + dy - 1

    if slot:
        slotPoints = []
        for x, y in component.slots:
            # print('slot', x, y)
            id = ComponentManager.getSlot(componentId, x, y)
            if id == -1:
                continue
            x1, y1, x2, y2 = component.getBox(x, y)
            mx = (x1 + x2) // 2
            my = (y1 + y2) // 2
            slotPoints.append([mx, my, id])
            minX = min(minX, x1, x2)
            maxX = max(maxX, x1, x2)
            minY = min(minY, y1, y2)
            maxY = max(maxY, y1, y2)
    dx = maxX - minX + 1
    dy = maxY - minY + 1

    image = np.full((dy + 2 * gap, dx + 2 * gap, 3), 255, np.uint8)
    for x, y, color in pixels:
        image[gap + y - minY][gap + x - minX] = color
    for tx, ty in component.corners:
        x, y = component.corners[(tx, ty)]
        x -= minX
        y -= minY
        cv2.circle(image, (gap + x, gap + y), 5, (0, 0, 0), -1)

    if number:
        for x, y in component.pieces:
            pieceId, _ = component.pieces[(x, y)]
            x1, y1, x2, y2 = component.getBox(x, y)
            # print(x1, y1, x2, y2)
            mx = (x1 + x2) // 2 - minX
            my = (y1 + y2) // 2 - minY
            putTextWithCircle(str(pieceId), (gap + mx, gap + my), image, (255, 255, 255), (100, 0, 0))

    if slot:
        for i in slotPoints:
            x, y, id = i
            putTextWithCircle(str(id), (gap + x - minX, gap + y - minY), image, (255, 255, 255), (0, 0, 100))

    showImage('component', image)

def showComponent2(component, number=True, border=True):
    gap = 50
    
    pixels = []
    for x, y in component.pieces:
        pieceId, bottomLeft = component.pieces[(x, y)]
        piece = PieceManager.get(pieceId)
        t1 = component.corners[(x, y)]
        t2 = component.corners[(x + 1, y)]
        o1 = piece.corners[bottomLeft]
        o2 = piece.corners[(bottomLeft + 1) % 4]
        pixels += transformPixels(piece.pixels, o1, t1, o2, t2)

    dx, dy, minX, minY = getPixelsSize(pixels)
    maxX = minX + dx - 1
    maxY = minY + dy - 1

    image = np.full((dy + 2 * gap, dx + 2 * gap, 3), 255, np.uint8)
    for x, y, color in pixels:
        image[gap + y - minY][gap + x - minX] = color

    if border:
        pieceId, bottomLeft = component.pieces[(0, 0)]
        piece = PieceManager.get(pieceId)
        t1 = component.corners[(0, 0)]
        t2 = component.corners[(1, 0)]
        o1 = piece.corners[bottomLeft]
        o2 = piece.corners[(bottomLeft + 1) % 4]
        color = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255)]
        for i in range(0, 4):
            edge = piece.edges[i]
            tmp = []
            for p in edge.originPoints:
                p = transformPoint(p, o1, t1, o2, t2)
                tmp.append([[p[0] - minX + gap, p[1] - minY + gap]])
            tmp = np.array(tmp)
            cv2.drawContours(image, tmp, -1, color[i], 2)

    for tx, ty in component.corners:
        x, y = component.corners[(tx, ty)]
        x -= minX
        y -= minY
        cv2.circle(image, (gap + x, gap + y), 5, (0, 0, 0), -1)

    if number:
        for x, y in component.pieces:
            pieceId, _ = component.pieces[(x, y)]
            x1, y1, x2, y2 = component.getBox(x, y)
            # print(x1, y1, x2, y2)
            mx = (x1 + x2) // 2 - minX
            my = (y1 + y2) // 2 - minY
            putTextWithCircle(str(pieceId), (gap + mx, gap + my), image, (255, 255, 255), (100, 0, 0))

    showImage('component', image)

def previewSlot(slotId, pieceId, edgeId):
    componentId, x, y = ComponentManager.getSlotPos(slotId)
    component = ComponentManager.get(componentId)
    newComponent = Component(pieceId, edgeId)
    # print(x, y)
    tmp = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for i, j in tmp:
        if not (x + i, y + j) in component.pieces:
            continue
        nowPiece, nowEdge = component.pieces[(x + i, y + j)]
        newComponent.setPiece(nowPiece, nowEdge, i, j)
    showComponent2(newComponent)