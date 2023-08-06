class TournamentPlayer(object):
    def __init__(self, data) -> None:
        self.username = data.get('username', None)
        self.status = data.get('status', None)