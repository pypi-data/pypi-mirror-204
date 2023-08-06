from .chesscomhandlers.countryhandler import CountryHandler


class ChessCountry(object):
    def __init__(self, abbr) -> None:
        self.code = abbr
    
    def getInfo(self) -> None:
        self.info = CountryHandler().getInfo(self.code)

    def getPlayers(self) -> None:
        self.players = CountryHandler().getPlayers(self.code)
    
    def getClubs(self) -> None:
        self.clubs = CountryHandler().getClubs(self.code)