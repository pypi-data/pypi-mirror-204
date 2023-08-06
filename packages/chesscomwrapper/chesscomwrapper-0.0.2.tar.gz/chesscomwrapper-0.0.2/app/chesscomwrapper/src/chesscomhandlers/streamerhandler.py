
from ..apimanager import API
from ..streamer.chessstreamerinfo import ChessStreamerInfo
from ..chesscomhandler import ChesscomHandler
from ..errorhandlers.noneerrorhandler import NoneErrorHandler
from ..requesthandlers.singletonrequesthandler import SingletonRequestHandler


class StreamerHandler(ChesscomHandler):
    
    def __init__(self):
        """Initializes a RoundHandler object"""
        self.errorHandler = NoneErrorHandler()
        self.requestHandler = SingletonRequestHandler()
        pass


    def getStreamersInfo(self):
        """Returns player's monthly archives"""
        response = self.doRequest(API.BASE_URL + API.STREAMERS)
        if response is None:
            return None
        streamers =  list(map(lambda streamer: ChessStreamerInfo(streamer), response.json()['streamers']))
        return streamers
