class PuzzleInfo(object):
    def __init__(self, data):
        self.title = data.get("title", None)
        self.url = data.get("url", None)
        self.publishTime = data.get("publish_time", None)
        self.fen = data.get("fen", None)
        self.pgn = data.get("pgn", None)
        self.image = data.get("image", None)