from ..chesscomhandlers.teammatchboardhandler import TeamMatchBoardHandler


class TeamMatchBoard(object):
    def __init__(self, boardUrl) -> None:
        self.boardUrl = boardUrl

    def getInfo(self):
        self.info = TeamMatchBoardHandler().getInfo(self.boardUrl)


