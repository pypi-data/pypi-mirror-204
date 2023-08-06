class ChessPlayerProfile:
    def __init__(self, data):
        """Initializes a ChessPlayerProfile object"""
        
        self.avatar = data.get('avatar', None)
        self.player_id = data.get('player_id', None)
        self.id = data.get('@id', None)
        self.url = data.get('url', None)
        self.name = data.get('name', None)
        self.username = data.get('username', None)
        self.followers = data.get('followers', None)
        self.country = data.get('country', None)
        self.location = data.get('location', None)
        self.last_online = data.get('last_online', None)
        self.joined = data.get('joined', None)
        self.status = data.get('status', None)
        self.is_streamer = data.get('is_streamer', None)
        self.verified = data.get('verified', None)
        self.league = data.get('league', None)
        pass