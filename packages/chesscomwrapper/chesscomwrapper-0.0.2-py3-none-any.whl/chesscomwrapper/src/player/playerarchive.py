# from src.chesscomhandlers.playerhandler import PlayerHandler

# from src.chesscomhandlers.playerhandler import PlayerHandler


from ..chesscomhandlers.archivehandler import ArchiveHandler


class PlayerArchive(object):
    def __init__(self,username, year, month) -> None:
        self.username = username
        self.year = year
        self.month = month

    def getGames(self):
        self.games = ArchiveHandler().getGames(self.username, self.year, self.month)
    
    def getPGN(self):
        self.pgn = ArchiveHandler().getPGN(self.username, self.year, self.month)