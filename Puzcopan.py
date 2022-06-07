from ComponentManager import ComponentManager
from SolvingManager import SolvingManager
import UserInterface
from PieceManager import PieceManager
from ImageProcessor import processImage

solving = -1

def image(path):
    print('Image: Process image', path)
    processImage(path)
    print('Image: Done')

def resetSolving():
    global solving
    solving = -1

def solve(slotId):
    global solving
    if not ComponentManager.slotAvailable(slotId):
        print('Slot', slotId, 'is not available')
        return
    solving = slotId
    print('Now solving slot ', solving, ', use next() to get recommended solution', sep='')

def resetSolve(slotId):
    if not ComponentManager.slotAvailable(slotId):
        print('Slot', slotId, 'is not available')
        return
    SolvingManager.reset(slotId)

def updateSolving():
    global solving
    if not ComponentManager.slotAvailable(solving):
        solving = -1

def preview(slotId, pieceId, edgeId):
    if not ComponentManager.slotAvailable(slotId):
        print('Slot', slotId, 'is not available')
        return
    if not PieceManager.available(pieceId):
        print('Piece', pieceId, 'is not available')
        return
    if edgeId < 0 or 4 <= edgeId:
        print('Edge number', edgeId, 'is not available')
        return
    print('Preview: Piece ', pieceId, ':', edgeId, ' at slot ', slotId, sep='')
    UserInterface.previewSlot(slotId, pieceId, edgeId)
    print('Preview: Done')

def next():
    updateSolving()
    if solving == -1:
        print('Use solve(slotId) to choose a slot')
        return
    num = SolvingManager.next(solving)
    todo = SolvingManager.getTodo(solving)
    score, pieceId, edgeId = todo[num]
    print('Next: Show next (#', num ,') recommended solution at slot ', solving, ': ', pieceId, ':', edgeId, sep='')
    preview(solving, pieceId, edgeId)
    print('Next: Done')

def last():
    updateSolving()
    if solving == -1:
        print('Use solve(slotId) to choose a slot')
        return
    num = SolvingManager.last(solving)
    todo = SolvingManager.getTodo(solving)
    score, pieceId, edgeId = todo[num]
    print('Next: Show next (#', num ,') recommended solution at slot ', solving, ': ', pieceId, ':', edgeId, sep='')
    preview(solving, pieceId, edgeId)
    print('Next: Done')

def component(pieceId):
    if not PieceManager.available(pieceId):
        print('Piece', pieceId, 'is not available')
        return
    componentId, x, y, bottomLeft = ComponentManager.findPiece(pieceId)
    print('Component: Show piece ', pieceId, ' at component ', componentId, sep='')
    UserInterface.showComponent(componentId, number=True, slot=True)
    print('Component: Done')

def now():
    updateSolving()
    if solving == -1:
        print('Use solve(slotId) to choose a slot')
        return
    num = SolvingManager.now(solving)
    todo = SolvingManager.getTodo(solving)
    score, pieceId, edgeId = todo[num]
    print('Now: Show previous (#', num ,') recommended solution at slot ', solving, ': ', pieceId, ':', edgeId, sep='')
    preview(solving, pieceId, edgeId)
    print('Now: Done')


def ok(slotId=-1, pieceId=-1, edgeId=-1):
    if slotId == -1:
        updateSolving()
        if solving == -1:
            print('OK: No previous previewing solution')
            return
        slotId = solving
    if not ComponentManager.slotAvailable(slotId):
        print('Slot', slotId, 'is not available')
        return
    if pieceId == -1:
        num = SolvingManager.now(solving)
        todo = SolvingManager.getTodo(solving)
        if num == -1:
            print('OK: No previous previewing solution')
            return
        _, pieceId, edgeId = todo[num]
    if not PieceManager.available(pieceId):
        print('Piece', pieceId, 'is not available')
        return
    if edgeId < 0 or 4 <= edgeId:
        print('Edge number', edgeId, 'is not available')
        return

    print('OK: Put piece ', pieceId, ':', edgeId, ' at slot ', slotId, sep='')
    if not ComponentManager.setPiece(slotId, pieceId, edgeId):
        print('Merge components failed')
        return
    print('OK: success')
    component(pieceId)
    print('OK: Done')
        