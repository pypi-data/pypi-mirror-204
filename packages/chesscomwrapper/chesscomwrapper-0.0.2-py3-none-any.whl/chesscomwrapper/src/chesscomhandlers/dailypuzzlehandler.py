from ..apimanager import API
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
    

class PuzzleInfo(object):
    def __init__(self, data):
        self.title = data.get("title", None)
        self.url = data.get("url", None)
        self.publishTime = data.get("publish_time", None)
        self.fen = data.get("fen", None)
        self.pgn = data.get("pgn", None)
        self.image = data.get("image", None)