from .handlers.chesscomhandlers.roundhandler import RoundHandler
from .models.tournament.tournamnetroundinfo import TournamentRoundInfo


class TournamentRound(object):
    def __init__(self, url):
        self.url = url
    
    def getInfo(self):
        self.info: TournamentRoundInfo = RoundHandler().getInfo(self.url)

    