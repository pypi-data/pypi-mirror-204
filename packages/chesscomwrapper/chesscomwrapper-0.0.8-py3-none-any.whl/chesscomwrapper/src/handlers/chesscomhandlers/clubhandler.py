# from src.player.playerclub import ClubMember, PlayerClub
from ...models.club.clubprofile import ClubProfile
from ...models.club.clubmember import ClubMember
from ...apimanager import API
from ..chesscomhandler import ChesscomHandler
from ..errorhandlers.noneerrorhandler import NoneErrorHandler
from ..requesthandlers.singletonrequesthandler import SingletonRequestHandler


class ClubHandler(ChesscomHandler):
    
    def __init__(self):
        """Initializes a ArchiveHandler object"""
        self.errorHandler = NoneErrorHandler()
        self.requestHandler = SingletonRequestHandler()
        pass

        
    def getMembers(self, clubname) -> list[ClubMember]:
        """Returns player's monthly archives"""
        response = self.doRequest(API.BASE_URL + API.CLUB + clubname + "/" + "members")
        if response is None:
            return None
        members = list(map(lambda mem: ClubMember(mem["username"], mem["joined"]), response.json()['all_time']))
        return members
    
    def getProfile(self, clubname):
        """Returns player's monthly archives"""
        response = self.doRequest(API.BASE_URL + API.CLUB + clubname)
        if response is None:
            return None
        profile = ClubProfile(response.json())
        return profile