import functools
from typing import Optional

from .models.teammatch.teammatchboardinfo import TeamMatchBoardInfo
from .handlers.chesscomhandlers.teammatchboardhandler import TeamMatchBoardHandler


class TeamMatchBoard(object):
    def __init__(self, boardUrl, lazy = True):

        self.boardUrl = boardUrl
        if lazy == False:
            self.info
    
    @functools.cached_property
    def info(self):
        return self._getInfo()

    def _getInfo(self) -> Optional[TeamMatchBoardInfo]:
        return TeamMatchBoardHandler().getInfo(self.boardUrl)


