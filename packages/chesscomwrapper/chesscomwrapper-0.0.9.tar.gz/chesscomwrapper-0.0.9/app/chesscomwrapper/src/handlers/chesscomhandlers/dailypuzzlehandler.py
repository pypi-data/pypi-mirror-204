from ...models.puzzle.puzzleinfo import PuzzleInfo
from ...apimanager import API
from ..chesscomhandler import ChesscomHandler
from ..errorhandlers.noneerrorhandler import NoneErrorHandler
from ..requesthandlers.singletonrequesthandler import SingletonRequestHandler


class PuzzleHandler(ChesscomHandler):
    def __init__(self) -> None:
        self.errorHandler = NoneErrorHandler()
        self.requestHandler = SingletonRequestHandler()
        pass
    
    def getDaily(self):
        """Returns dailyPuzzleInfo object"""
        response = self.doRequest(API.BASE_URL + API.PUZZLE)
        if response is None:
            return None
        dailyPuzzleInfo = PuzzleInfo(response.json())
        return dailyPuzzleInfo
    
    def getRandomPuzzle(self):
        """Returns a random PuzzleInfo object"""
        response = self.doRequest(API.BASE_URL + API.PUZZLE + API.RANDOM)
        if response is None:
            return None
        puzzleInfo = PuzzleInfo(response.json())
        return puzzleInfo