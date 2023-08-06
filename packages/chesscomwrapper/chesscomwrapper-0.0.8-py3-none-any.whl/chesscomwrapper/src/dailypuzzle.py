from .handlers.chesscomhandlers.dailypuzzlehandler import PuzzleHandler, PuzzleInfo


class PuzzleFactory(object):
    

    def __init__(self) -> None:
        self.puzzleHandler = PuzzleHandler()
        pass

    def getDaily(self):
        return Puzzle(self.puzzleHandler.getDaily())

    def getRandomPuzzle(self):
        return Puzzle(self.puzzleHandler.getRandomPuzzle())

class Puzzle(object):
    def __init__(self, info: PuzzleInfo) -> None:
        self.info = info
    
