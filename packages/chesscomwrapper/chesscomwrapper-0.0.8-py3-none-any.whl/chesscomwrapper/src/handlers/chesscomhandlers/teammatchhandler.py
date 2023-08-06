from ..chesscomhandler import ChesscomHandler
from ..errorhandlers.noneerrorhandler import NoneErrorHandler
from ..requesthandlers.singletonrequesthandler import SingletonRequestHandler
from ...models.teammatch.teammatchinfo import TeamMatchInfo


class TeamMatchHandler(ChesscomHandler):
    
    def __init__(self):
        """Initializes a RoundHandler object"""
        self.errorHandler = NoneErrorHandler()
        self.requestHandler = SingletonRequestHandler()
        pass


    def getInfo(self, url):
        """Returns player's monthly archives"""
        response = self.doRequest(url)
        if response is None:
            return None
        roundinfo = TeamMatchInfo(response.json())
        return roundinfo