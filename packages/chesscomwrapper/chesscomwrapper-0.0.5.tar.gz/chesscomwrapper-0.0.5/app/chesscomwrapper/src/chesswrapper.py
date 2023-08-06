import sys

from .models.streamer.chessstreamerinfo import ChessStreamerInfo

from .models.player.titledcategory import TitledCategory


from .chessstreamer import ChessStreamer






sys.path.append("/Users/nicolapanozzo/unibo/Kaunas Courses/Component Based Software Engineering/chesscom_api_wrapper")

from .chessclub import Club
from .chessplayer import ChessPlayer 
from .chesstournament import Tournament
from .chessteammatch import TeamMatch
from .chesscountry import ChessCountry
from .dailypuzzle import PuzzleFactory

from .chessleaderboards import ChessLeaderboards
class ChessWrapper(object):
  """A class to wrap the chess.com API"""
  
  def __init__(self):
    pass
  


  def getPlayer(self,username, lazy=True) -> ChessPlayer:
    """Returns a chess player"""
    player = ChessPlayer(username, lazy)

    return player
  
  def getClub(self, clubname):
    """Returns a Club"""
    club = Club(clubname)
    return club
  
  def getTournament(self, tournamentId):
    """Returns a tournament"""
    tournament = Tournament(tournamentId)
    return tournament
  
  def getTeamMatch(self, matchUrl):
    """Returns a team match"""
    teamMatch = TeamMatch(matchUrl)
    return teamMatch
  
  def getTitledPlayers(self, category: TitledCategory) -> list[ChessPlayer]:
    """Returns titled players"""
    return ChessPlayer._getTitledPlayers(self, category)
    
  def getCountry(self, countryCode):
    """Returns a country"""
    return ChessCountry(countryCode)
  
  def getDailyPuzzle(self):
    """Returns the daily puzzle"""
    return PuzzleFactory().getDaily()
  
  def getRandomPuzzle(self):
    """Returns a random puzzle"""
    return PuzzleFactory().getRandomPuzzle()
  
  def getStreamersInfo(self) -> list[ChessStreamerInfo]:
    """Returns a list of streamers"""
    return ChessStreamer._getStreamersInfo(self)
  
  def getLeaderboards(self):
    """Returns a list of streamers"""
    return ChessLeaderboards().getLeaderboards()
  


