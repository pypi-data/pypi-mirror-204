from .handlers.chesscomhandlers.leaderboardshandler import LeaderboardsHandler
from .models.leaderboards.leaderboardsinfo import LeaderboardsInfo


class ChessLeaderboards(object):
    
    @staticmethod
    def getLeaderboards() -> LeaderboardsInfo:
        """Gets all the leaderboards from Chess.com"""
        return LeaderboardsHandler().getLeaderboards()