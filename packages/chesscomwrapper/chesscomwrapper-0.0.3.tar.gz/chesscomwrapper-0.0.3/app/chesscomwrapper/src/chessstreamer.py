# "username": "lularobs",
#             "avatar": "https://images.chesscomfiles.com/uploads/v1/user/101229188.3e34f836.50x50o.9ca43d70d5a8.jpeg",
#             "twitch_url": "https://twitch.tv/lularobs",
#             "url": "https://www.chess.com/member/lularobs",
#             "is_live": true,
#             "is_community_streamer": false

from .chesscomhandlers.streamerhandler import StreamerHandler
from .streamer.chessstreamerinfo import ChessStreamerInfo


class ChessStreamer(object):
    def __init__(self, info: ChessStreamerInfo) -> None:
        self.info = info 
        pass

    @staticmethod
    def getStreamers(self):
        """Gets a list of streamers"""
        return [ChessStreamer(info) for info in StreamerHandler().getStreamersInfo()]

