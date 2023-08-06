import functools
from typing import Optional
from .handlers.chesscomhandlers.roundhandler import RoundHandler
from .models.tournament.tournamnetroundinfo import TournamentRoundInfo


class TournamentRound(object):
    def __init__(self, url, lazy = True):
        self.url = url
        if lazy == False:
            self.info

    @functools.cached_property
    def info(self):
        return self._getInfo()
    
    def _getInfo(self) -> Optional[TournamentRoundInfo]:
        return RoundHandler().getInfo(self.url)

    