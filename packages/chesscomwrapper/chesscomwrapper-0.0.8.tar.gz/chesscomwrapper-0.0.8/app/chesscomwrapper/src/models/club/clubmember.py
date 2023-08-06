from ...chessplayer import ChessPlayer


class ClubMember(object):
    def __init__(self, username, joined) -> None:
        self.player = ChessPlayer(username)
        self.joined = joined
