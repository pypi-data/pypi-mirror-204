
class ClubProfile(object):
    def __init__(self, data: dict):
        self.idUrl = data.get('@id', None)
        self.name = data.get('name', None)
        self.club_id = data.get('club_id', None)
        self.country = data.get('country', None)
        self.average_daily_rating = data.get('average_daily_rating', None)
        self.members_count = data.get('members_count', None)
        self.created = data.get('created', None)
        self.last_activity = data.get('last_activity', None)
        self.admin = data.get('admin', None)
        self.visibility = data.get('visibility', None)
        self.join_request = data.get('join_request', None)
        self.icon = data.get('icon', None)
        self.description = data.get('description', None)
        self.url = data.get('url', None)