from ..apimanager import API
from ..chesscomhandler import ChesscomHandler, NoneErrorHandler, SingletonRequestHandler
from ..player.playergames import ChesscomGame


class ArchiveHandler(ChesscomHandler):
    
    def __init__(self):
        """Initializes a ArchiveHandler object"""
        self.errorHandler = NoneErrorHandler()
        self.requestHandler = SingletonRequestHandler()
        pass


    def getGames(self, username, year, month):
        """Returns player's monthly archives"""
        response = self.doRequest(API.PLAYER_BASE + username + "/" + API.GAMES + year + "/" + month)
        if response is None:
            return None
        games = list(map(lambda game: ChesscomGame(game), response.json()['games']))
        return games
        
    def getPGN(self, username, year, month):
        """Returns player's monthly archives"""
        response = self.doRequest(API.PLAYER_BASE + username + API.GAMES + year + "/" + month + "/" + API.PGN)
        if response is None:
            return None
        pgn = response.data
        return pgn




  # def getPGN(self):
  #       self.pgn = PlayerHandler().getPlayerMonthlyArchivePGN(self)
