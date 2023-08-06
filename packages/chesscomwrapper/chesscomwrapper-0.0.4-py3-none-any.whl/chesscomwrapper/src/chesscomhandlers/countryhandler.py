from ..chessclub import Club
from ..chessplayer import ChessPlayer
from ..country.countryinfo import CountryInfo
from ..apimanager import API
from ..chesscomhandler import ChesscomHandler
from ..errorhandlers.noneerrorhandler import NoneErrorHandler
from ..requesthandlers.singletonrequesthandler import SingletonRequestHandler


class CountryHandler(ChesscomHandler):
    
    def __init__(self):
        """Initializes a RoundHandler object"""
        self.errorHandler = NoneErrorHandler()
        self.requestHandler = SingletonRequestHandler()
        pass


    def getInfo(self, code):
        """Returns player's monthly archives"""
        response = self.doRequest(API.BASE_URL + API.COUNTRY + code)
        if response is None:
            return None
        countryinfo = CountryInfo(response.json())
        return countryinfo
    
    def getPlayers(self, code):
        """Returns country's players"""
        response = self.doRequest(API.BASE_URL + API.COUNTRY + code + "/" + API.PLAYERS)
        if response is None:
            return None
        players = [ChessPlayer(player) for player in response.json()['players']]
        return players
    
    def getClubs(self, code):
        """Returns country's clubs"""
        response = self.doRequest(API.BASE_URL + API.COUNTRY + code + "/" + API.CLUBS)
        if response is None:
            return None

        clubs = [Club(club.split("/")[-1]) for club in response.json()['clubs']]
        return clubs
    