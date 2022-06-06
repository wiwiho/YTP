class Edge:

    def __init__(self, originPoints, edgePoints, interpolation, rotate, scale):
        self.originPoints = originPoints
        self.edgePoints = edgePoints
        self.interpolation = interpolation
        self.rotate = rotate
        self.scale = scale

class Piece:
    
    def __init__(self, image, id, contour, corners, edges, pixels):
        self.image = image
        self.id = id
        self.contour = contour
        self.corners = corners
        self.edges = edges
        self.pixels = pixels
        pass