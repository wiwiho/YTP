import cv2
import numpy as np
import math

path = '/media/wiwiho/DATA/YTP/'
# file = path + 'Zolver-master/resources/jigsaw-samples/van-gogh.png'
file = path + 'orz.png'
print(file)
tempFilePath = path

binaryImage = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
cv2.imwrite(tempFilePath + 'binarized.png', binaryImage)

def image_preprocess():
    global binaryImage
    ret, binaryImage = cv2.threshold(binaryImage, 250, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite(tempFilePath + 'threshold.png', binaryImage)
    kernel = np.ones((3, 3), np.uint8)
    # maybe clean dirty edges
    binaryImage = cv2.morphologyEx(binaryImage, cv2.MORPH_CLOSE, kernel)                
    cv2.imwrite(tempFilePath + "morph1.png", binaryImage)
    binaryImage = cv2.morphologyEx(binaryImage, cv2.MORPH_OPEN, kernel)
    cv2.imwrite(tempFilePath + "morph2.png", binaryImage)
    # there is only very slight difference
image_preprocess()

# fill all contours in the image
def fill_holes():
    global binaryImage
    # They are sorted by their numbers of points now
    # I think they should be sorted by area
    contour, _ = cv2.findContours(binaryImage, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contour:
        cv2.drawContours(binaryImage, [cnt], 0, 255, -1)
    cv2.imwrite(tempFilePath + "fill.png", binaryImage)
fill_holes()

contours, hier = cv2.findContours(binaryImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

originImage = cv2.imread(file, cv2.COLOR_BGR2GRAY)

def small_contour_filter():
    global contours
    contours = sorted(np.array(contours), key=lambda x: x.shape[0], reverse=True)
    max = contours[0].shape[0]
    contours = np.array([elt for elt in contours if elt.shape[0] > max / 3])
small_contour_filter()

cv2.drawContours(originImage, contours, -1, (0, 255, 0), 2)
for contour in contours:
    convexHull = cv2.convexHull(contour)
    cv2.drawContours(originImage, convexHull, -1, (255, 0, 0), 2)
    
cv2.imwrite(tempFilePath + 'contours.png', originImage)

def lineLength(a):
    x = a[0]
    y = a[1]
    return x * x + y * y

def calcAngle(a, b, c): # angle BAC
    v1 = b - a
    v2 = c - a
    dot = v1[0] * v2[0] + v1[1] * v2[1]
    ans = dot / lineLength(v1) / lineLength(v2)
    return math.acos(ans)

tmpImage = originImage.copy()

def process_piece(contour):
    global tmpImage
    convexHull = cv2.convexHull(contour)
    len = cv2.arcLength(convexHull, True)
    minSep = 0.05 * len
    minSep = minSep * minSep
    size = convexHull.shape[0]
    assert(size >= 4)
    points = []
    for i in range(0, size):
        thisImage = tmpImage.copy()
        a = None
        b = None
        p1 = convexHull[i][0]
        for j in range(1, size):
            k = (i + j) % size
            p2 = convexHull[k][0]
            if lineLength(p1 - p2) >= minSep:
                a = p2
                break
        for j in range(1, size):
            k = (i - j + size) % size
            p2 = convexHull[k][0]
            if lineLength(p1 - p2) >= minSep:
                b = p2
                break
        cv2.circle(thisImage, p1, 5, (0, 0, 255))
        cv2.circle(thisImage, a, 5, (0, 255, 255))
        cv2.circle(thisImage, b, 5, (0, 255, 255))
        points.append([calcAngle(p1, a, b), p1])
        print('angle-' + str(i) + ' ' + str(calcAngle(p1, a, b)))
        cv2.imwrite(tempFilePath + 'angle-' + str(i) + '.png', thisImage)
    points = sorted(points, key=lambda x: x[0])
    corner = []
    for i in range(0, 4):
        corner.append(points[i][1])

    return corner


for contour in contours:
    corner = process_piece(contour)
    corner = np.array(corner)
    print(corner)
    for i in corner:
        cv2.circle(originImage, i, 10, (0, 0, 255))

cv2.imwrite(tempFilePath + 'corner.png', originImage)