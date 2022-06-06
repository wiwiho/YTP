import cv2
import numpy as np
from FileManager import FileManager
from PieceManager import PieceManager
from ImageManager import ImageManager
from Vector import *
from PieceProcessor import processPiece
from Image import Image
from Util import *
import math

class _ImageProcessor:

    def __init__(self, path: str):
        self.image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        self.originImage = cv2.imread(path, cv2.COLOR_BGR2GRAY)

    def preprocess(self):
        ret, self.image = cv2.threshold(self.image, 250, 255, cv2.THRESH_BINARY_INV)
        kernel = np.ones((3, 3), np.uint8)
        self.image = cv2.morphologyEx(self.image, cv2.MORPH_CLOSE, kernel)                
        self.image = cv2.morphologyEx(self.image, cv2.MORPH_OPEN, kernel)

    def fill_holes(self):
        contour, _ = cv2.findContours(self.image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contour:
            cv2.drawContours(self.image, [cnt], 0, 255, -1)

    def small_contour_filter(self):
        self.contours = sorted(np.array(self.contours), key=lambda x: x.shape[0], reverse=True)
        max = self.contours[0].shape[0]
        self.contours = np.array([elt for elt in self.contours if elt.shape[0] > max / 3])

    def process(self):
        self.preprocess()
        self.fill_holes()
        self.contours, _ = cv2.findContours(self.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        self.small_contour_filter()

        showImage = self.originImage.copy()

        cv2.drawContours(showImage, self.contours, -1, (0, 255, 0), 2)
            
        FileManager.wirteFolder('image', 'image-' + str(ImageManager.size()) + '-contours.png', showImage)

        showImage = self.originImage.copy()
        pieces = []
        for contour in self.contours:
            piece = processPiece(contour, self.originImage)
            pieces.append(piece)
            piece = PieceManager.get(piece)
            for i in range(0, 4):
                edge = piece.edges[i]
                temp = []
                for j in edge.originPoints:
                    temp.append([j])
                temp = np.array(temp)
                color = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255)]
                cv2.drawContours(showImage, temp, -1, color[i], 2)
            for i in range(0, 4):
                cv2.circle(showImage, piece.corners[i], 5, (0, 0, 0), thickness=-1)
        
        FileManager.wirteFolder('image', 'image-' + str(ImageManager.size()) + '-corners.png', showImage)

        for id in pieces:
            piece = PieceManager.get(id)
            cX, cY = findContourCenter(piece.contour)
            putTextCenter(str(id), (cX, cY), showImage, (0, 0, 0))
            putTextWithCircle(str(id), (cX, cY), showImage, (255, 255, 255), (100, 0, 0))

        FileManager.wirteFolder('image', 'image-' + str(ImageManager.size()) + '-number.png', showImage)

        image = Image(self.originImage, pieces)
        return ImageManager.addImage(image)
    
def processImage(path):
    processor = _ImageProcessor(path)
    processor.process()