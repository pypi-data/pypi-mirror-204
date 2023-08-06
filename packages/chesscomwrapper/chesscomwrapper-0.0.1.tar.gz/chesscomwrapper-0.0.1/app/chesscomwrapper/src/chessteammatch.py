from .chesscomhandlers.teammatchhandler import TeamMatchHandler


class TeamMatch(object):
    def __init__(self, urlId) -> None:
        self.urlId = urlId
    
    def getInfo(self):
        self.info = TeamMatchHandler().getInfo(self.urlId)
    

