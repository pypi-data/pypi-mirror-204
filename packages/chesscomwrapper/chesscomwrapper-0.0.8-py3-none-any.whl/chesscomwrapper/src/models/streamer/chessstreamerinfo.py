class ChessStreamerInfo(object):
    def __init__(self, data) -> None:
        self.username = data.get('username', None)
        self.avatar = data.get('avatar', None)
        self.twitch_url = data.get('twitch_url', None)
        self.url = data.get('url', None)
        self.is_live = data.get('is_live', None)
        self.is_community_streamer = data.get('is_community_streamer', None)
        pass
    
    