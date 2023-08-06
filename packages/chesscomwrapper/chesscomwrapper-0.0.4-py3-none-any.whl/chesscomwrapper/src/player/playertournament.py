class PlayerTournaments(object):

    def __init__(self, data):
        self.finished = list(map(lambda finishedData: PlayerTournamentFinished(finishedData), data.get('finished', None)))
        self.inProgress = list(map(lambda registeredData: PlayerTournamentInProgress(registeredData), data.get('in_progress', None)))
        self.registered = list(map(lambda registeredData: PlayerTournamentRegistered(registeredData), data.get('registered', None)))

class PlayerResult(object):
    def __init__(self, data):
        self.wins = data.get('wins', None)
        self.losses = data.get('losses', None)
        self.draws = data.get('draws', None)
        self.points_awarded = data.get('points_awarded', None)
        self.placement = data.get('placement', None)
        self.status = data.get('status', None)
        self.total_players = data.get('total_players', None)



class PlayerTournamentRegistered(object):
    def __init__(self, data):
        self.id = data.get('@id', None)
        self.url = data.get('url', None)
        self.status = data.get('status', None)


class PlayerTournamentInProgress(object):
    def __init__(self, data):
        self.id = data.get('@id', None)
        self.url = data.get('url', None)
        self.status = data.get('status', None)
        self.totalPlayers = data.get('total_players', None)
        self.wins = data.get('wins', None)
        self.losses = data.get('losses', None)
        self.draws = data.get('draws', None)


class PlayerTournamentFinished(object):
    def __init__(self, data):
        self.id = data.get('@id', None)
        self.url = data.get('url', None)
        self.status = data.get('status', None)
        self.totalPlayers = data.get('total_players', None)
        self.placement = data.get('placement', None)
        self.wins = data.get('wins', None)
        self.losses = data.get('losses', None)
        self.draws = data.get('draws', None)
        self.pointsAwarded = data.get('points_awarded', None)