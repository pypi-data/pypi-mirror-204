from .handlers.chesscomhandlers.roundinfohandler import RoundInfoHandler


class TournamentRoundGroup(object):
    def __init__(self, url) -> None:
        self.url = url

    def getInfo(self):
        self.info = RoundInfoHandler().getRoundGroupInfo(self.url)

        pass