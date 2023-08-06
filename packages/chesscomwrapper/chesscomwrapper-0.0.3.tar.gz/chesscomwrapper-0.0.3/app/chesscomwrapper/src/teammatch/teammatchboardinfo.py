from ..player.playergames import ChesscomGame


class TeamMatchBoardInfo(object):
    def __init__(self, data):
        self.board_scores = BoardScores(data.get('board_scores', None))
        self.games = [ChesscomGame(game) for game in data.get('games', [])]

class BoardScores(object):
    def __init__(self, data):
        # get the value of the first key
        self.player1 = list(data.keys())[0]
        self.player1Score = data.get(list(data.keys())[0], None)
        self.player2 = list(data.keys())[1]
        self.player2Score = data.get(list(data.keys())[1], None)
        self.result = f'{self.player1Score}-{self.player2Score}'

