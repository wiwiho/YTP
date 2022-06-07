import cv2
import os
import Config
import shutil

class _FileManager:

    def __init__(self, root) -> None:
        self.root = root
        if os.path.exists(root) and os.path.isdir(root):
            shutil.rmtree(root)
        os.makedirs(root, exist_ok=True)

    def write(self, file, image):
        cv2.imwrite(self.root + file, image)
    
    def wirteFolder(self, folder, file, image):
        path = self.root + folder + '/'
        os.makedirs(path, exist_ok=True)
        # print('ok', path + file)
        cv2.imwrite(path + file, image)

FileManager = _FileManager(Config.tempFilePath)

