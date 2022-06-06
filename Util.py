import cv2
import numpy as np
import math
from Vector import *
import time

def findContourCenter(contour):
    M = cv2.moments(contour)
    cX = int(M['m10'] / M['m00'])
    cY = int(M['m01'] / M['m00'])
    return (cX, cY)

def putTextCenter(text, pos, img, color):
    font = cv2.FONT_HERSHEY_SIMPLEX
    textsize = cv2.getTextSize(text, font, 0.6, 2)[0]
    textX = pos[0] - textsize[0] // 2
    textY = pos[1] + textsize[1] // 2
    cv2.putText(img, text, (textX, textY), font, 0.6, color, 2)

def putTextWithCircle(text, pos, img, textColor, circleColor):
    cv2.circle(img, pos, 20, circleColor, thickness=-1)
    putTextCenter(text, pos, img, textColor)

def getContourSize(contour):
    minX = 1000000
    maxX = 0
    minY = 1000000
    maxY = 0
    for i in contour:
        minX = min(minX, i[0][0])
        maxX = max(maxX, i[0][0])
        minY = min(minY, i[0][1])
        maxY = max(maxY, i[0][1])
    dx = maxX - minX + 1
    dy = maxY - minY + 1
    return (dx, dy, minX, minY)

def getPixelsSize(pixels):
    minX = 1000000
    maxX = -1000000
    minY = 1000000
    maxY = -1000000
    for i in pixels:
        minX = min(minX, i[0])
        maxX = max(maxX, i[0])
        minY = min(minY, i[1])
        maxY = max(maxY, i[1])
    dx = maxX - minX + 1
    dy = maxY - minY + 1
    return (dx, dy, minX, minY)

def shiftContour(contour, ox, oy):
    ans = []
    for i in contour:
        ans.append([[i[0][0] - ox, i[0][1] - oy]])
    ans = np.array(ans)
    return ans

def pointArrayToContour(arr):
    ans = []
    for i in arr:
        ans.append([i])
    ans = np.array(ans)
    return ans

def transformPoint(p, o1, t1, o2, t2):
    polarOrigin = cartesianToPolar(o2 - o1)
    polarNew = cartesianToPolar(t2 - t1)

    rotate = polarNew[1] - polarOrigin[1]
    stretch = polarNew[0] / polarOrigin[0]

    x, y = p[0], p[1]
    x -= o1[0]
    y -= o1[1]
    r = math.sqrt(x * x + y * y)
    r *= stretch
    t = math.atan2(y, x)
    t += rotate
    x = r * math.cos(t)
    y = r * math.sin(t)
    x = t1[0] + x
    y = t1[1] + y
    return np.array([int(x), int(y)])

def transformPixels(pixels, o1, t1, o2, t2):
    newPixels = []

    polarOrigin = cartesianToPolar(o2 - o1)
    polarNew = cartesianToPolar(t2 - t1)

    rotate = polarNew[1] - polarOrigin[1]
    stretch = polarNew[0] / polarOrigin[0]

    for p in pixels:
        x, y, color = p
        x -= o1[0]
        y -= o1[1]
        r = math.sqrt(x * x + y * y)
        r *= stretch
        t = math.atan2(y, x)
        t += rotate
        x = r * math.cos(t)
        y = r * math.sin(t)
        x = t1[0] + x
        y = t1[1] + y
        newPixels.append([math.floor(x), math.floor(y), color])
        newPixels.append([math.floor(x), math.ceil(y), color])
        newPixels.append([math.ceil(x), math.floor(y), color])
        newPixels.append([math.ceil(x), math.ceil(y), color])
    return newPixels

def showImage(name, image):
    cv2.imshow(name, image)
    while True:
        if cv2.waitKey(1) == ord('q'):
            break
        if cv2.getWindowProperty(name, cv2.WND_PROP_VISIBLE) < 1:        
            break
        time.sleep(0.1)
    cv2.destroyAllWindows()