# from src.player.playerarchive import PlayerArchive
# from src.chessplayer import ChessPlayer
from ..player.playertournament import PlayerTournaments
from ..player.playerclub import PlayerClub
from ..apimanager import API
from ..player.playerarchive import PlayerArchive
from ..player.playergames import ChesscomGame
from ..chesscomhandler import ChesscomHandler, NoneErrorHandler, SingletonRequestHandler

from ..player.chessplayerprofile import ChessPlayerProfile
from ..player.chessplayerstats import ChessPlayerStats


class PlayerHandler(ChesscomHandler):
    """ Handles requests for player data """
    
    def __init__(self):
        """Initializes a PlayerHandler object"""
        self.errorHandler = NoneErrorHandler()
        self.requestHandler = SingletonRequestHandler()
        pass

    def getPlayerProfile(self, username) -> ChessPlayerProfile:
        """Returns a dictionary of a player's info"""
        response = self.doRequest(API.PLAYER_BASE + username)
        if response is None:
            return None
        profile = ChessPlayerProfile(response.json())
        return profile
    
    def getPlayerStats(self, username) -> ChessPlayerStats:
        """Returns a dictionary of a player's stats"""

        response = self.doRequest(API.PLAYER_BASE + username + "/" + API.STATS)

        if response is None:
            return None
        stats = ChessPlayerStats(response.json())
        return stats
    
    def getPlayerGames(self, username):
        """Returns a dictionary of a player's games"""
        response = self.doRequest(API.PLAYER_BASE + username + "/" + API.GAMES)
        if response is None:
            return None
        games = list(map(lambda game: ChesscomGame(game), response.json()['games']))
        return games
    
    def getPlayerGamesToMove(self, username):
        """Returns a dictionary of a player's games"""
        response = self.doRequest(API.PLAYER_BASE + username + "/" + API.GAMES_TO_MOVE)
        if response is None:
            return None
        games = list(map(lambda game: ChesscomGame(game), response.json()['games']))
        return games
    
    def getPlayerArchives(self, username):
        """Returns a dictionary of a player's archives"""
        response = self.doRequest(API.PLAYER_BASE + username + "/" + API.GAMES_ARCHIVES)
        if response is None:
            return None
        archives = []
        print(response.json())
        for archive in response.json()["archives"]:
            # take last element of the list
            archive = archive.split("/")
            year = archive.pop()
            month = archive.pop()
            archives.append(PlayerArchive(username, month, year))
        return archives
    
    def getPlayerClubs(self, username) -> list[PlayerClub]:
        """Returns player's clubs"""
        response = self.doRequest(API.PLAYER_BASE + username + "/" + API.CLUBS)
        if response is None:
            return None
        playerClubs = list(map(lambda club: PlayerClub(club["name"], club["joined"]), response.json()['clubs']))
        return playerClubs
    
    def getPlayerTournaments(self, username) -> PlayerTournaments:
        """Returns player's tournaments"""
        response = self.doRequest(API.PLAYER_BASE + username + "/" + API.TOURNAMENTS)
        if response is None:
            return None
        tournaments = PlayerTournaments(response.json())

        return tournaments

    def getTitledPlayers(self, category):
        """Returns a dictionary of titled players"""
        response = self.doRequest(API.BASE_URL + API.TITLED_PLAYERS + category)
        if response is None:
            return None
        players = response.json()["players"]
        return players