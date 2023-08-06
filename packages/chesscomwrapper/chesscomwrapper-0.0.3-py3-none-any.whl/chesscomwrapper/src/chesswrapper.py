import sys


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
  


  def getPlayer(self,username, lazy=True):
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
  
  def getTitledPlayers(self):
    """Returns titled players"""
    return list(map(lambda player: ChessPlayer(player), ChessPlayer.getTitledPlayers(self,"GM")))
    
  def getCountry(self, countryCode):
    """Returns a country"""
    return ChessCountry(countryCode)
  
  def getDailyPuzzle(self):
    """Returns the daily puzzle"""
    return PuzzleFactory().getDaily()
  
  def getRandomPuzzle(self):
    """Returns a random puzzle"""
    return PuzzleFactory().getRandomPuzzle()
  
  def getStreamers(self):
    """Returns a list of streamers"""
    return ChessStreamer.getStreamers(self)
  
  def getLeaderboards(self):
    """Returns a list of streamers"""
    return ChessLeaderboards().getLeaderboards(self)

