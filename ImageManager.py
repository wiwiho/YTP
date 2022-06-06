class _ImageManager:

    def __init__(self) -> None:
        self.image = []

    def addImage(self, image):
        self.image.append(image)

    def get(self, num):
        return self.image[num]
    
    def size(self):
        return len(self.image)

ImageManager = _ImageManager()