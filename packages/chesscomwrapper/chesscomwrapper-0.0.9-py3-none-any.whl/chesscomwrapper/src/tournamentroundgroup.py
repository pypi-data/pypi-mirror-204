import functools
from typing import Optional

from .models.tournament.tournamentroundgroupinfo import TournamentRoundGroupInfo
from .handlers.chesscomhandlers.roundinfohandler import RoundInfoHandler


class TournamentRoundGroup(object):
    def __init__(self, url, lazy = True) -> None:
        self.url = url
        if lazy == False:
            self.info

    @functools.cached_property
    def info(self) -> Optional[TournamentRoundGroupInfo]:
        return self._getInfo()
    
    def _getInfo(self):
        return RoundInfoHandler().getRoundGroupInfo(self.url)