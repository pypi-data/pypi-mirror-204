from .handlers.chesscomhandlers.streamerhandler import StreamerHandler
from .models.streamer.chessstreamerinfo import ChessStreamerInfo


class ChessStreamer(object):

    @staticmethod
    def _getStreamersInfo(self):
        """Gets a list of streamers"""
        return StreamerHandler().getStreamersInfo()

