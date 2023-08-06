class ChesscomGame:
    def __init__(self, data):
        # refactor previus code using .get() method with None as default value
        self.url = data.get("url", None)
        self.move_by = data.get("move_by", None)
        self.pgn = data.get("pgn", None)
        self.time_control = data.get("time_control", None)
        self.last_activity = data.get("last_activity", None)
        self.rated = data.get("rated", None)
        self.turn = data.get("turn", None)
        self.fen = data.get("fen", None)
        self.start_time = data.get("start_time", None)
        self.time_class = data.get("time_class", None)
        self.rules = data.get("rules", None)
        self.white = data.get("white", None).split("/")[-1]
        self.black = data.get("black", None).split("/")[-1]
        self.end_time = data.get("end_time", None)
        self.accuracies = data.get("accuracies", None)
        self.tcn = data.get("tcn", None)
        self.uuid = data.get("uuid", None)
        self.initial_setup = data.get("initial_setup", None)

class ChesscomGameArchived:
    def __init__(self, data):
        # refactor previus code using .get() method with None as default value
        self.url = data.get("url", None)
        self.pgn = data.get("pgn", None)
        self.time_control = data.get("time_control", None)
        self.rated = data.get("rated", None)
        self.fen = data.get("fen", None)
        self.start_time = data.get("start_time", None)
        self.time_class = data.get("time_class", None)
        self.rules = data.get("rules", None)
        self.white = GamePlayer(data.get("white", None))
        self.black = GamePlayer(data.get("black", None))
        self.end_time = data.get("end_time", None)
        self.accuracies = data.get("accuracies", None)
        self.tcn = data.get("tcn", None)
        self.uuid = data.get("uuid", None)
        self.initial_setup = data.get("initial_setup", None)


class ChesscomGameToMove(object):
    def __init__(self, data):
        if data is None:
            return None
        self.url = data.get("url", None)
        self.move_by = data.get("move_by", None)
        self.last_activity = data.get("last_activity", None)

class GamePlayer(object):
    def __init__(self, data):
        if data is None:
            return None
        self.rating = data.get("rating", None)
        self.result = data.get("result", None)
        self.id = data.get("@id", None)
        self.username = data.get("username", None)
        self.uuid = data.get("uuid", None)
    