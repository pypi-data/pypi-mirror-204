class LeaderboardsInfo(object):
    """A class to represent a leaderboardsInfo object"""
    def __init__(self, data):
        """Initializes a LeaderboardsInfo object"""
        self.json = data
        # print(data)
        self.daily = [LeaderboardInfo(info) for info in data['daily']]
        self.daily960 = [LeaderboardInfo(info) for info in data['daily960']]
        self.live_rapid = [LeaderboardInfo(info) for info in data['live_rapid']]
        self.live_blitz = [LeaderboardInfo(info) for info in data['live_blitz']]
        self.live_bullet = [LeaderboardInfo(info) for info in data['live_bullet']]
        self.live_bughouse = [LeaderboardInfo(info) for info in data['live_bughouse']]
        self.live_blitz960 = [LeaderboardInfo(info) for info in data['live_blitz960']]
        self.live_threecheck = [LeaderboardInfo(info) for info in data['live_threecheck']]
        self.live_crazyhouse = [LeaderboardInfo(info) for info in data['live_crazyhouse']]
        self.live_kingofthehill = [LeaderboardInfo(info) for info in data['live_kingofthehill']]
        self.tactics = [LeaderboardInfo(info) for info in data['tactics']]
        self.rush = [LeaderboardInfo(info) for info in data['rush']]
        self.battle = [LeaderboardInfo(info) for info in data['battle']]
        pass




class TrendScore(object):
    """A class to represent a trendScore object"""
    def __init__(self, data) -> None:
        """Initializes a TrendScore object"""
        if data is None:
            return None
        self.direction = data.get('direction', None)
        self.delta = data.get('delta', None)
        pass

class TrendRank(object):
    """A class to represent a trendRank object"""
    def __init__(self, data) -> None:
        """Initializes a TrendRank object"""
        if data is None:
            return None
        self.direction = data.get('direction', None)
        self.delta = data.get('delta', None)
        pass



class LeaderboardInfo(object):
    """A class to represent a liveRapidInfo object"""
    def __init__(self, data) -> None:
        
        """Initializes a LiveRapidInfo object"""
        if data is None:
            return None
        self.player_id = data.get('player_id', None)
        self.id = data.get('@id', None)
        self.url = data.get('url', None)
        self.username = data.get('username', None)
        self.name = data.get('name', None)
        self.score = data.get('score', None)
        self.rank = data.get('rank', None)
        self.country = data.get('country', None)
        self.title = data.get('title', None)
        self.status = data.get('status', None)
        self.avatar = data.get('avatar', None)
        self.trend_score = TrendScore(data.get('trend_score', None))
        self.trend_rank = TrendRank(data.get('trend_rank', None))
        self.flair_code = data.get('flair_code', None)
        self.win_count = data.get('win_count', None)
        self.loss_count = data.get('loss_count', None)
        self.draw_count = data.get('draw_count', None)
        pass

