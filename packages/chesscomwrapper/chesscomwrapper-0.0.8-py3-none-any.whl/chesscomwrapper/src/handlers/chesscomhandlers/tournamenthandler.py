from ...models.tournament.tournamnetroundinfo import TournamentRoundInfo
from ...apimanager import API
from ..chesscomhandler import ChesscomHandler
from ..errorhandlers.noneerrorhandler import NoneErrorHandler
from ..requesthandlers.singletonrequesthandler import SingletonRequestHandler
from ...models.tournament.tournamentinfo import TournamentInfo


class TournamentHandler(ChesscomHandler):
    
    def __init__(self):
        """Initializes a ArchiveHandler object"""
        self.errorHandler = NoneErrorHandler()
        self.requestHandler = SingletonRequestHandler()
        pass

    
    def getInfo(self, tournamentId):
        """Returns player's monthly archives"""
        response = self.doRequest(tournamentId)
        if response is None:
            return None
        info = TournamentInfo(response.json())
        return info
    
    def getRoundInfo(self, tournamentId, round):
        """Returns tournament rounds info"""
        response = self.doRequest(tournamentId + "/" + round)
        if response is None:
            return None
        roundInfo = TournamentRoundInfo(response.json())
        return roundInfo

    def getRoundGroupInfo():
        pass

    # def getGames(self, username, year, month):
    #     """Returns player's monthly archives"""
    #     response = self.doRequest(API.PLAYER_BASE + username + "/" + API.GAMES + year + "/" + month)
    #     if response is None:
    #         return None
    #     games = list(map(lambda game: ChesscomGame(game), response.json()['games']))
    #     return games
        
    # def getMembers(self, clubname) -> list[ClubMember]:
    #     """Returns player's monthly archives"""
    #     response = self.doRequest(API.BASE_URL + API.CLUB + clubname + "/" + "members")
    #     if response is None:
    #         return None
    #     members = list(map(lambda mem: ClubMember(mem["username"], mem["joined"]), response.json()['all_time']))
    #     return members
    
    # def getProfile(self, clubname):
    #     """Returns player's monthly archives"""
    #     response = self.doRequest(API.BASE_URL + API.CLUB + clubname)
    #     if response is None:
    #         return None
    #     profile = ClubProfile(response.json())
    #     return profile