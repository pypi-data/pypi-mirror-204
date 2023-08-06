from typing import Optional

from .models.player.titledcategory import TitledCategory

from .models.player.playerclub import PlayerClub

from .models.player.playertournament import PlayerTournaments
from .lazy_decorator import lazy_property
from .playerarchive import PlayerArchive
from .handlers.chesscomhandlers.playerhandler import PlayerHandler
from .models.player.chessplayerstats import ChessPlayerStats
from .models.player.chessplayerprofile import ChessPlayerProfile
from .models.player.playergames import ChesscomGame, ChesscomGameToMove
# from chesswrapper.chessplayerstats import ChessPlayerStats
# from chessplayerprofile import ChessPlayerProfile
import functools


    


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
  

  @functools.cached_property
  def profile(self):
    return self._getProfile()

  @functools.cached_property
  def stats(self):
    return self._getStats()

  @functools.cached_property
  def games(self):
    return self._getPlayerGames()

  @functools.cached_property
  def gamesToMove(self):
    return self._getPlayerGamesToMove()

  @functools.cached_property
  def tournaments(self):
    return self._getPlayerTournaments()

  @functools.cached_property
  def clubs(self):
    return self._getPlayerClubs() 

  @functools.cached_property
  def archives(self):
    return self._getPlayerArchives() 

  

  def _getProfile(self) -> Optional[ChessPlayerProfile]:
    """Returns a dictionary of a player's profile"""
    
    return PlayerHandler().getPlayerProfile(self.username)
    
  
  def _getStats(self) -> Optional[ChessPlayerStats]:
    """Returns player's stats"""
    return PlayerHandler().getPlayerStats(self.username)
    
  def _getPlayerGames(self) -> Optional[list[ChesscomGame]]:
    """Returns player's games"""
    return PlayerHandler().getPlayerGames(self.username)

  def _getPlayerGamesToMove(self) -> Optional[list[ChesscomGameToMove]]:
    """Returns player's games"""
    return PlayerHandler().getPlayerGamesToMove(self.username)
  
  def _getPlayerArchives(self) -> Optional[list[PlayerArchive]]:
    """Returns player's archives"""
    return PlayerHandler().getPlayerArchives(self.username)
  
  def _getPlayerTournaments(self) -> Optional[PlayerTournaments]:
    """Returns player's tournaments"""
    return PlayerHandler().getPlayerTournaments(self.username)

  def _getPlayerClubs(self) -> Optional[list[PlayerClub]]:
    """Returns player's clubs"""
    return PlayerHandler().getPlayerClubs(self.username)
  
  @staticmethod
  def _getTitledPlayers(self, category: TitledCategory):
    """Returns titled players"""

    return list(map(lambda player: ChessPlayer(player),PlayerHandler().getTitledPlayers(category)))
