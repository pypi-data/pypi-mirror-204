class ChessPlayerStats:
    def __init__(self, data):
        if not data:
            return None
        """Initializes a ChessPlayerStats object"""

        self.chess_daily = ChessVariant(data.get("chess_daily", None))
        self.chess960_daily = ChessVariant(data.get("chess960_daily", None))
        self.chess_rapid = ChessVariant(data.get("chess_rapid", None))
        self.chess_bullet = ChessVariant(data.get("chess_bullet", None))
        self.chess_blitz = ChessVariant(data.get("chess_blitz", None))
        self.fide = data.get("fide", None)
        self.tactics = Tactics(data.get("tactics", None))
        self.puzzle_rush = PuzzleRush(data.get("puzzle_rush", None))
        self.puzzle_rush_daily = PuzzleRush(data.get("puzzle_rush_daily", None))

class ChessVariant:
    def __init__(self, data):
        if not data:
            return None
        self.last = ChessRating(data.get("last"))
        self.best = ChessBest(data.get("best"))
        self.record = ChessRecord(data.get("record"))
        self.tournament = ChessTournament(data.get("tournament"))

class ChessRating:
    def __init__(self, data):
        if not data:
            return None
        self.rating = data.get("rating", None)
        self.date = data.get("date", None)
        self.rd = data.get("rd", None)

class ChessBest:
    def __init__(self, data):
        if not data:
            return None
        self.rating = data.get("rating", None)
        self.date = data.get("date", None)
        self.game = data.get("game", None)

class ChessRecord:
    def __init__(self, data):
        if not data:
            return None
        self.win = data.get("win", None)
        self.loss = data.get("loss", None)
        self.draw = data.get("draw", None)
        self.time_per_move = data.get("time_per_move", None)
        self.timeout_percent = data.get("timeout_percent", None)

class ChessTournament:
    def __init__(self, data):
        if not data:
            return None
        self.points = data.get("points", None)
        self.withdraw = data.get("withdraw", None)
        self.count = data.get("count", None)
        self.highest_finish = data.get("highest_finish", None)

class Tactics:
    def __init__(self, data):
        if not data:
            return None
        self.highest = TacticsRating(data.get("highest", None))
        self.lowest = TacticsRating(data.get("lowest", None))

class TacticsRating:
    def __init__(self, data):
        if not data:
            return None
        self.rating = data.get("rating", None)
        self.date = data.get("date", None)

class PuzzleRush:
    def __init__(self, data):
        if not data:
            return None
        self.best = PuzzleRushScore(data.get("best", None))

class PuzzleRushScore:
    def __init__(self, data):
        if not data:
            return None
        self.total_attempts = data.get("total_attempts", None)
        self.score = data.get("score", None)