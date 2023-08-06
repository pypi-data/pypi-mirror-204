# "groups": [
#         "https://api.chess.com/pub/tournament/-33rd-chesscom-quick-knockouts-1401-1600/4/1"
#     ],
# "players": [
#     {
#         "username": "chicken_forever",
#         "is_advancing": true
#     },
#     {
#         "username": "drooo82",
#         "is_advancing": false
#     }
# ]


from ..chesscomhandlers.roundhandler import RoundHandler
from ..tournament.tournamnetroundinfo import TournamentRoundInfo


class TournamentRound(object):
    def __init__(self, url):
        self.url = url
    
    def getInfo(self):
        self.info: TournamentRoundInfo = RoundHandler().getInfo(self.url)

    