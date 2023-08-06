import functools
from .handlers.chesscomhandlers.teammatchhandler import TeamMatchHandler


class TeamMatch(object):
    def __init__(self, urlId, lazy = True) -> None:
        self.urlId = urlId
        if lazy == False:
            self.info

    @functools.cached_property
    def info(self):
        return self._getInfo()
    
    def _getInfo(self):
        return TeamMatchHandler().getInfo(self.urlId)
    

