from .chesscomhandlers.leaderboardshandler import LeaderboardsHandler
from .leaderboards.leaderboardsinfo import LeaderboardsInfo


class ChessLeaderboards(object):
    # def __init__(self, info: LeaderboardsInfo) -> None:
    #     self.info = info 
    #     pass

    @staticmethod
    def getLeaderboards(self) -> LeaderboardsInfo:
        """Gets all the leaderboards from Chess.com"""
        return LeaderboardsHandler().getLeaderboards()