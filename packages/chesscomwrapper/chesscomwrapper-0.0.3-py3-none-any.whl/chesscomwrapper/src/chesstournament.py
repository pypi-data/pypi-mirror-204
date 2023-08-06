from .chesscomhandlers.tournamenthandler import TournamentHandler


class Tournament(object):
    def __init__(self, id):
        self.id = id
        
    def getInfo(self):
        self.info = TournamentHandler().getInfo(self.id)

    def getRounds(self):
        self.rounds = TournamentHandler().getRounds(self.id)



