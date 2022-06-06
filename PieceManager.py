from Piece import *

class _PieceManager:

    def __init__(self) -> None:
        self.pieces = []
        self.disable = []

    def addPiece(self, piece) -> int:
        self.pieces.append(piece)
        self.disable.append(False)
        return len(self.pieces) - 1

    def size(self) -> int:
        return len(self.pieces)

    def get(self, num) -> Piece:
        assert(not self.disable[num])
        return self.pieces[num]

    def getEdge(self, num, e) -> Edge:
        return self.get(num).edges[e]

    def delete(self, num):
        self.disable[num] = True
    
PieceManager = _PieceManager()