from .handlers.chesscomhandlers.streamerhandler import StreamerHandler
from .models.streamer.chessstreamerinfo import ChessStreamerInfo


class ChessStreamer(object):
    def __init__(self, info: ChessStreamerInfo) -> None:
        self.info = info 
        pass

    @staticmethod
    def _getStreamersInfo(self):
        """Gets a list of streamers"""
        return StreamerHandler().getStreamersInfo()

