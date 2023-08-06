from .player.playerarchive import PlayerArchive
from .chesscomhandlers.playerhandler import PlayerHandler
from .player.chessplayerstats import ChessPlayerStats
from .player.chessplayerprofile import ChessPlayerProfile
from .player.playergames import ChesscomGame
# from chesswrapper.chessplayerstats import ChessPlayerStats
# from chessplayerprofile import ChessPlayerProfile


    
def lazy_property(fn):
    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazy_property

class ChessPlayer(object):
  """A class to represent a chess.com player"""

  def __init__(self, username, lazy=True):
    """Initializes a ChessPlayer object"""
    
    self.username = username
    if lazy == False:
      self.profile
      self.stats
      self.games
      self.gamesToMove
      self.tournaments
      self.clubs
    
    
    
    
    
    pass

  @lazy_property
  def profile(self):
    return self.getProfile()

  @lazy_property
  def stats(self):
    return self.getStats()

  @lazy_property
  def games(self):
    return self.getPlayerGames()

  @lazy_property
  def gamesToMove(self):
    return self.getPlayerGamesToMove()

  @lazy_property
  def tournaments(self):
    return self.getPlayerTournaments()

  @lazy_property
  def clubs(self):
    return self.getPlayerClubs() 


  

  def getProfile(self):
    """Returns a dictionary of a player's profile"""
    
    return PlayerHandler().getPlayerProfile(self.username)
    
  
  def getStats(self):
    """Returns player's stats"""
    return PlayerHandler().getPlayerStats(self.username)
    
  def getPlayerGames(self):
    """Returns player's games"""
    return PlayerHandler().getPlayerGames(self.username)

  def getPlayerGamesToMove(self):
    """Returns player's games"""
    return PlayerHandler().getPlayerGamesToMove(self.username)
  
  def getPlayerArchives(self):
    """Returns player's archives"""
    return PlayerHandler().getPlayerArchives(self.username)
  
  def getPlayerTournaments(self):
    """Returns player's tournaments"""
    return PlayerHandler().getPlayerTournaments(self.username)

  def getPlayerClubs(self):
    """Returns player's clubs"""
    return PlayerHandler().getPlayerClubs(self.username)
  
  @staticmethod
  def getTitledPlayers(self, category):
    """Returns titled players"""
    return PlayerHandler().getTitledPlayers(category)
