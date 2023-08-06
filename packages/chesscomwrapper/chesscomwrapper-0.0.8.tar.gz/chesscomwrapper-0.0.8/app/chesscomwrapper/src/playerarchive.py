import functools
from .handlers.chesscomhandlers.archivehandler import ArchiveHandler


class PlayerArchive(object):
    def __init__(self,username, year, month, lazy = True) -> None:
        self.username = username
        self.year = year
        self.month = month
        if lazy == False:
            self.games
            self.pgn
    
    @functools.cached_property
    def games(self):
        return self._getGames()
    
    @functools.cached_property
    def pgn(self):
        return self._getPGN()

    def _getGames(self):
        return ArchiveHandler().getGames(self.username, self.year, self.month)
    
    def _getPGN(self):
        return ArchiveHandler().getPGN(self.username, self.year, self.month)